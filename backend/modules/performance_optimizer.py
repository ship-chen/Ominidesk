#!/usr/bin/env python3
"""
性能优化器 - 实时性能监控和优化
v1.0 - 新增功能
"""

import asyncio
import logging
import psutil
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
from collections import deque

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """性能指标数据类"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    memory_mb: float
    available_mb: float


class PerformanceOptimizer:
    """性能优化器"""
    
    def __init__(self, max_history: int = 1000, cpu_threshold: float = 80.0, 
                 memory_threshold: float = 85.0, disk_threshold: float = 90.0):
        """
        初始化性能优化器
        
        Args:
            max_history: 最大历史记录数
            cpu_threshold: CPU 告警阈值 (%)
            memory_threshold: 内存告警阈值 (%)
            disk_threshold: 磁盘告警阈值 (%)
        """
        self.max_history = max_history
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.disk_threshold = disk_threshold
        self.metrics_history: deque = deque(maxlen=max_history)
        self.alerts: List[str] = []
        logger.info("✓ 性能优化器已初始化")
    
    async def collect_metrics(self) -> PerformanceMetrics:
        """收集性能指标"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            metrics = PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                disk_percent=disk.percent,
                memory_mb=memory.used / (1024 * 1024),
                available_mb=memory.available / (1024 * 1024)
            )
            
            self.metrics_history.append(metrics)
            
            # 检查告警
            await self._check_alerts(metrics)
            
            return metrics
        except Exception as e:
            logger.error(f"✗ 收集性能指标失败: {e}")
            raise
    
    async def _check_alerts(self, metrics: PerformanceMetrics) -> None:
        """检查性能告警"""
        alerts = []
        
        if metrics.cpu_percent > self.cpu_threshold:
            alert = f"⚠️ CPU 使用率过高: {metrics.cpu_percent:.1f}%"
            alerts.append(alert)
            logger.warning(alert)
        
        if metrics.memory_percent > self.memory_threshold:
            alert = f"⚠️ 内存使用率过高: {metrics.memory_percent:.1f}%"
            alerts.append(alert)
            logger.warning(alert)
        
        if metrics.disk_percent > self.disk_threshold:
            alert = f"⚠️ 磁盘使用率过高: {metrics.disk_percent:.1f}%"
            alerts.append(alert)
            logger.warning(alert)
        
        if alerts:
            self.alerts.extend(alerts)
    
    def get_average_metrics(self, seconds: int = 60) -> Optional[Dict[str, float]]:
        """获取平均性能指标
        
        Args:
            seconds: 时间窗口（秒）
        
        Returns:
            平均指标字典或 None
        """
        if not self.metrics_history:
            return None
        
        now = datetime.now()
        cutoff_time = now.replace(second=now.second - seconds if now.second >= seconds else now.second - seconds + 60)
        
        relevant_metrics = [
            m for m in self.metrics_history 
            if m.timestamp >= cutoff_time
        ]
        
        if not relevant_metrics:
            return None
        
        return {
            "cpu_percent": sum(m.cpu_percent for m in relevant_metrics) / len(relevant_metrics),
            "memory_percent": sum(m.memory_percent for m in relevant_metrics) / len(relevant_metrics),
            "disk_percent": sum(m.disk_percent for m in relevant_metrics) / len(relevant_metrics),
        }
    
    def get_system_status(self) -> Dict[str, any]:
        """获取系统状态概览"""
        if not self.metrics_history:
            return {"status": "无数据"}
        
        latest = self.metrics_history[-1]
        avg = self.get_average_metrics(60)
        
        return {
            "latest": {
                "cpu_percent": latest.cpu_percent,
                "memory_percent": latest.memory_percent,
                "disk_percent": latest.disk_percent,
                "memory_mb": latest.memory_mb,
                "available_mb": latest.available_mb,
                "timestamp": latest.timestamp.isoformat()
            },
            "average_60s": avg or {},
            "alerts": self.alerts[-10:],  # 最后10条告警
            "status": "正常" if not self.alerts else "告警"
        }
    
    def clear_alerts(self) -> None:
        """清除告警列表"""
        self.alerts.clear()
        logger.info("✓ 告警已清除")
