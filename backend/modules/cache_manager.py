#!/usr/bin/env python3
"""
缓存管理器 - LRU 缓存 + TTL 支持
v1.0 - 新增功能
"""

import logging
from typing import Dict, Optional, Any, Callable
from datetime import datetime, timedelta
from collections import OrderedDict
import json
import hashlib

logger = logging.getLogger(__name__)


class CacheEntry:
    """缓存条目"""
    def __init__(self, key: str, value: Any, ttl: Optional[int] = None):
        self.key = key
        self.value = value
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()
        self.access_count = 1
        self.ttl = ttl  # 生存时间（秒）
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        if self.ttl is None:
            return False
        
        return (datetime.now() - self.created_at).total_seconds() > self.ttl
    
    def update_access(self) -> None:
        """更新访问信息"""
        self.last_accessed = datetime.now()
        self.access_count += 1


class CacheManager:
    """缓存管理器 - LRU 缓存策略"""
    
    def __init__(self, max_size: int = 1000, default_ttl: Optional[int] = None):
        """
        初始化缓存管理器
        
        Args:
            max_size: 最大缓存条目数
            default_ttl: 默认生存时间（秒）
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0
        }
        logger.info(f"✓ 缓存管理器已初始化 (最大容量: {max_size})")
    
    def _generate_key(self, key: str) -> str:
        """生成缓存键 (支持自定义哈希)"""
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值
        
        Args:
            key: 缓存键
        
        Returns:
            缓存值或 None
        """
        cache_key = self._generate_key(key)
        
        if cache_key not in self.cache:
            self.stats["misses"] += 1
            return None
        
        entry = self.cache[cache_key]
        
        # 检查是否过期
        if entry.is_expired():
            del self.cache[cache_key]
            self.stats["misses"] += 1
            return None
        
        # LRU: 将最近访问的条目移到末尾
        self.cache.move_to_end(cache_key)
        entry.update_access()
        self.stats["hits"] += 1
        
        return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 生存时间（秒），None 表示使用默认值
        """
        cache_key = self._generate_key(key)
        ttl = ttl or self.default_ttl
        
        # 如果键已存在，更新并移到末尾
        if cache_key in self.cache:
            self.cache[cache_key].value = value
            self.cache[cache_key].ttl = ttl
            self.cache.move_to_end(cache_key)
        else:
            # 检查容量
            if len(self.cache) >= self.max_size:
                # 删除最旧的条目（LRU）
                removed_key = next(iter(self.cache))
                del self.cache[removed_key]
                self.stats["evictions"] += 1
                logger.debug(f"缓存条目已清除: {removed_key}")
            
            # 添加新条目
            self.cache[cache_key] = CacheEntry(key, value, ttl)
    
    def delete(self, key: str) -> bool:
        """删除缓存项
        
        Args:
            key: 缓存键
        
        Returns:
            True 表示删除成功，False 表示键不存在
        """
        cache_key = self._generate_key(key)
        if cache_key in self.cache:
            del self.cache[cache_key]
            logger.debug(f"缓存项已删除: {key}")
            return True
        return False
    
    def clear(self) -> None:
        """清空所有缓存"""
        self.cache.clear()
        logger.info("✓ 所有缓存已清空")
    
    def cleanup_expired(self) -> int:
        """清理过期缓存
        
        Returns:
            清理的条目数
        """
        expired_keys = [
            key for key, entry in self.cache.items()
            if entry.is_expired()
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            logger.info(f"✓ 清理过期缓存: {len(expired_keys)} 条")
        
        return len(expired_keys)
    
    def get_stats(self) -> Dict[str, any]:
        """获取缓存统计信息"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (
            self.stats["hits"] / total_requests * 100
            if total_requests > 0 else 0
        )
        
        return {
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "evictions": self.stats["evictions"],
            "hit_rate": f"{hit_rate:.2f}%",
            "current_size": len(self.cache),
            "max_size": self.max_size,
            "memory_usage": self._estimate_memory_usage()
        }
    
    def _estimate_memory_usage(self) -> str:
        """估计内存使用量"""
        total_size = 0
        for entry in self.cache.values():
            try:
                total_size += len(json.dumps(entry.value).encode())
            except:
                total_size += 1024  # 默认估计 1KB
        
        if total_size < 1024:
            return f"{total_size} B"
        elif total_size < 1024 * 1024:
            return f"{total_size / 1024:.2f} KB"
        else:
            return f"{total_size / (1024 * 1024):.2f} MB"
