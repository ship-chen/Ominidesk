#!/usr/bin/env python3
"""
速率限制器 - API 防滥用保护
v1.0 - 新增功能
"""

import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio

logger = logging.getLogger(__name__)


class RateLimitConfig:
    """速率限制配置"""
    def __init__(self, requests_per_minute: int = 60, requests_per_hour: int = 1000, 
                 burst_size: int = 10):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.burst_size = burst_size


class ClientRateLimit:
    """客户端速率限制信息"""
    def __init__(self, client_id: str, config: RateLimitConfig):
        self.client_id = client_id
        self.config = config
        self.request_times: list = []  # 请求时间戳列表
        self.total_requests = 0
        self.blocked_until: Optional[datetime] = None
    
    def is_blocked(self) -> bool:
        """检查客户端是否被阻止"""
        if self.blocked_until and datetime.now() < self.blocked_until:
            return True
        return False
    
    def can_request(self) -> bool:
        """检查是否可以发起请求"""
        if self.is_blocked():
            return False
        
        now = datetime.now()
        
        # 清理过期的请求记录
        cutoff_time = now - timedelta(hours=1)
        self.request_times = [t for t in self.request_times if t > cutoff_time]
        
        # 检查每分钟限制
        minute_ago = now - timedelta(minutes=1)
        requests_this_minute = sum(1 for t in self.request_times if t > minute_ago)
        if requests_this_minute >= self.config.requests_per_minute:
            return False
        
        # 检查每小时限制
        requests_this_hour = len(self.request_times)
        if requests_this_hour >= self.config.requests_per_hour:
            return False
        
        return True
    
    def record_request(self) -> None:
        """记录请求"""
        self.request_times.append(datetime.now())
        self.total_requests += 1
    
    def block(self, duration_seconds: int = 300) -> None:
        """阻止客户端
        
        Args:
            duration_seconds: 阻止持续时间（秒）
        """
        self.blocked_until = datetime.now() + timedelta(seconds=duration_seconds)
        logger.warning(f"客户端 {self.client_id} 被阻止 {duration_seconds} 秒")


class RateLimiter:
    """速率限制器"""
    
    def __init__(self, default_config: Optional[RateLimitConfig] = None):
        """
        初始化速率限制器
        
        Args:
            default_config: 默认配置
        """
        self.default_config = default_config or RateLimitConfig()
        self.clients: Dict[str, ClientRateLimit] = defaultdict(lambda: ClientRateLimit(
            client_id="",
            config=self.default_config
        ))
        self.stats = {
            "total_requests": 0,
            "blocked_requests": 0,
            "active_clients": 0
        }
        logger.info("✓ 速率限制器已初始化")
    
    def check_limit(self, client_id: str) -> bool:
        """检查客户端是否超过限制
        
        Args:
            client_id: 客户端 ID
        
        Returns:
            True 表示可以请求，False 表示超过限制
        """
        if client_id not in self.clients:
            self.clients[client_id] = ClientRateLimit(
                client_id=client_id,
                config=self.default_config
            )
        
        client = self.clients[client_id]
        
        if not client.can_request():
            self.stats["blocked_requests"] += 1
            logger.warning(f"客户端 {client_id} 超过限制")
            return False
        
        client.record_request()
        self.stats["total_requests"] += 1
        self.stats["active_clients"] = len(self.clients)
        
        return True
    
    def get_client_stats(self, client_id: str) -> Optional[Dict[str, any]]:
        """获取客户端统计信息"""
        if client_id not in self.clients:
            return None
        
        client = self.clients[client_id]
        now = datetime.now()
        
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)
        
        requests_this_minute = sum(1 for t in client.request_times if t > minute_ago)
        requests_this_hour = sum(1 for t in client.request_times if t > hour_ago)
        
        return {
            "client_id": client_id,
            "total_requests": client.total_requests,
            "requests_this_minute": requests_this_minute,
            "requests_this_hour": requests_this_hour,
            "is_blocked": client.is_blocked(),
            "blocked_until": client.blocked_until.isoformat() if client.blocked_until else None,
            "limits": {
                "per_minute": self.default_config.requests_per_minute,
                "per_hour": self.default_config.requests_per_hour
            }
        }
    
    def get_global_stats(self) -> Dict[str, any]:
        """获取全局统计信息"""
        return {
            "total_requests": self.stats["total_requests"],
            "blocked_requests": self.stats["blocked_requests"],
            "active_clients": self.stats["active_clients"],
            "block_rate": (
                self.stats["blocked_requests"] / self.stats["total_requests"] * 100
                if self.stats["total_requests"] > 0 else 0
            )
        }
