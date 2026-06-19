#!/usr/bin/env python3
"""
自我修改引擎 - 代码修改管理和禁区保护
v1.1 - 修复格式并完善功能
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import uuid

logger = logging.getLogger(__name__)


class ModificationType(str, Enum):
    """修改类型"""
    ADD = "add"
    REMOVE = "remove"
    MODIFY = "modify"
    PATCH = "patch"


class ForbiddenZone:
    """禁区定义"""
    def __init__(self, name: str, path: str, reason: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.path = path
        self.reason = reason
        self.created_at = datetime.now()
        self.protection_level = "critical"


class SelfModificationEngine:
    """自我修改引擎"""
    
    def __init__(self):
        """初始化自我修改引擎"""
        self.modification_history: List[Dict[str, Any]] = []
        self.forbidden_zones: Dict[str, ForbiddenZone] = {}
        self._init_default_forbidden_zones()
        logger.info("✓ 自我修改引擎已初始化")
    
    def _init_default_forbidden_zones(self) -> None:
        """初始化默认禁区"""
        default_zones = [
            ForbiddenZone(
                "Security Core",
                "/backend/security/",
                "安全核心模块 - 禁止修改"
            ),
            ForbiddenZone(
                "Database Layer",
                "/backend/database/",
                "数据库层 - 禁止修改"
            ),
            ForbiddenZone(
                "Permission System",
                "/backend/permissions/",
                "权限系统 - 禁止修改"
            ),
            ForbiddenZone(
                "Audit System",
                "/backend/audit/",
                "审计系统 - 禁止修改"
            )
        ]
        
        for zone in default_zones:
            self.forbidden_zones[zone.id] = zone
        
        logger.info(f"✓ 已初始化 {len(default_zones)} 个默认禁区")
    
    async def get_forbidden_zones(self) -> List[Dict[str, Any]]:
        """获取禁区列表
        
        Returns:
            禁区列表
        """
        return [
            {
                "id": zone.id,
                "name": zone.name,
                "path": zone.path,
                "reason": zone.reason,
                "protection_level": zone.protection_level,
                "created_at": zone.created_at.isoformat()
            }
            for zone in self.forbidden_zones.values()
        ]
    
    async def add_forbidden_zone(self, name: str, path: str, reason: str) -> bool:
        """添加禁区
        
        Args:
            name: 禁区名称
            path: 禁区路径
            reason: 禁止原因
        
        Returns:
            添加是否成功
        """
        try:
            zone = ForbiddenZone(name, path, reason)
            self.forbidden_zones[zone.id] = zone
            logger.info(f"✓ 禁区已添加: {name} ({path})")
            return True
        except Exception as e:
            logger.error(f"✗ 添加禁区失败: {e}")
            return False
    
    async def remove_forbidden_zone(self, zone_id: str) -> bool:
        """移除禁区
        
        Args:
            zone_id: 禁区 ID
        
        Returns:
            移除是否成功
        """
        if zone_id not in self.forbidden_zones:
            logger.error(f"禁区不存在: {zone_id}")
            return False
        
        try:
            zone = self.forbidden_zones[zone_id]
            del self.forbidden_zones[zone_id]
            logger.info(f"✓ 禁区已移除: {zone.name}")
            return True
        except Exception as e:
            logger.error(f"✗ 移除禁区失败: {e}")
            return False
    
    async def check_modification(self, file_path: str, modification_type: str) -> bool:
        """检查修改是否被允许
        
        Args:
            file_path: 文件路径
            modification_type: 修改类型
        
        Returns:
            是否允许修改
        """
        try:
            # 检查是否在禁区内
            for zone in self.forbidden_zones.values():
                if file_path.startswith(zone.path):
                    logger.warning(f"✗ 修改被禁止: {file_path} (在禁区: {zone.name})")
                    return False
            
            logger.info(f"✓ 修改被允许: {file_path}")
            return True
        except Exception as e:
            logger.error(f"✗ 检查修改失败: {e}")
            return False
    
    async def record_modification(self, file_path: str, modification_type: str, 
                                 description: str = "") -> bool:
        """记录修改历史
        
        Args:
            file_path: 文件路径
            modification_type: 修改类型
            description: 修改描述
        
        Returns:
            记录是否成功
        """
        try:
            record = {
                "id": str(uuid.uuid4()),
                "file_path": file_path,
                "modification_type": modification_type,
                "description": description,
                "timestamp": datetime.now().isoformat(),
                "allowed": await self.check_modification(file_path, modification_type)
            }
            
            self.modification_history.append(record)
            logger.info(f"✓ 修改已记录: {file_path}")
            return True
        except Exception as e:
            logger.error(f"✗ 记录修改失败: {e}")
            return False
    
    async def get_modification_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取修改历史
        
        Args:
            limit: 最多返回记录数
        
        Returns:
            修改历史列表
        """
        return self.modification_history[-limit:]
