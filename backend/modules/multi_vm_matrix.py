#!/usr/bin/env python3
"""
多虚拟机矩阵管理 - 管理多个虚拟机
v1.1 - 修复非法换行符转义
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


class VMRole(str, Enum):
    """虚拟机角色"""
    MASTER = "master"
    WORKER = "worker"
    BACKUP = "backup"
    MONITOR = "monitor"


class MultiVMMatrixManager:
    """多虚拟机矩阵管理器"""
    
    def __init__(self):
        """初始化多虚拟机矩阵管理器"""
        self.vms: Dict[str, Dict[str, Any]] = {}
        self.topology: Dict[str, List[str]] = {}  # VM 拓扑关系
        logger.info("✓ 多虚拟机矩阵管理器已初始化")
    
    async def register_vm(self, vm_id: str, role: VMRole) -> bool:
        """注册虚拟机
        
        Args:
            vm_id: 虚拟机 ID
            role: 虚拟机角色
        
        Returns:
            注册是否成功
        """
        try:
            self.vms[vm_id] = {
                "id": vm_id,
                "role": role.value,
                "registered_at": datetime.now().isoformat(),
                "status": "idle",
                "cpu_usage": 0,
                "memory_usage": 0,
                "network_io": 0
            }
            
            self.topology[vm_id] = []
            logger.info(f"✓ 虚拟机已注册: {vm_id} ({role.value})")
            return True
        except Exception as e:
            logger.error(f"✗ 注册虚拟机失败: {e}")
            return False
    
    async def unregister_vm(self, vm_id: str) -> bool:
        """注销虚拟机
        
        Args:
            vm_id: 虚拟机 ID
        
        Returns:
            注销是否成功
        """
        if vm_id not in self.vms:
            logger.error(f"虚拟机不存在: {vm_id}")
            return False
        
        try:
            del self.vms[vm_id]
            del self.topology[vm_id]
            logger.info(f"✓ 虚拟机已注销: {vm_id}")
            return True
        except Exception as e:
            logger.error(f"✗ 注销虚拟机失败: {e}")
            return False
    
    async def establish_connection(self, source_vm: str, target_vm: str) -> bool:
        """建立虚拟机间连接
        
        Args:
            source_vm: 源虚拟机 ID
            target_vm: 目标虚拟机 ID
        
        Returns:
            连接是否成功
        """
        if source_vm not in self.vms or target_vm not in self.vms:
            logger.error("虚拟机不存在")
            return False
        
        try:
            if target_vm not in self.topology[source_vm]:
                self.topology[source_vm].append(target_vm)
            logger.info(f"✓ 连接已建立: {source_vm} -> {target_vm}")
            return True
        except Exception as e:
            logger.error(f"✗ 建立连接失败: {e}")
            return False
    
    async def get_vm_status(self) -> Dict[str, Any]:
        """获取虚拟机矩阵状态
        
        Returns:
            矩阵状态字典
        """
        try:
            roles_count = {}
            for vm in self.vms.values():
                role = vm["role"]
                roles_count[role] = roles_count.get(role, 0) + 1
            
            return {
                "total_vms": len(self.vms),
                "roles": roles_count,
                "topology_connections": sum(len(v) for v in self.topology.values()),
                "vms": list(self.vms.values())
            }
        except Exception as e:
            logger.error(f"✗ 获取状态失败: {e}")
            return {"error": str(e)}
    
    async def update_vm_metrics(self, vm_id: str, metrics: Dict[str, float]) -> bool:
        """更新虚拟机指标
        
        Args:
            vm_id: 虚拟机 ID
            metrics: 指标字典 (cpu_usage, memory_usage, network_io)
        
        Returns:
            更新是否成功
        """
        if vm_id not in self.vms:
            logger.error(f"虚拟机不存在: {vm_id}")
            return False
        
        try:
            self.vms[vm_id].update(metrics)
            logger.debug(f"✓ 虚拟机指标已更新: {vm_id}")
            return True
        except Exception as e:
            logger.error(f"✗ 更新指标失败: {e}")
            return False
    
    async def get_statistics(self) -> Dict[str, Any]:
        """获取矩阵统计信息
        
        Returns:
            统计信息字典
        """
        if not self.vms:
            return {"total_vms": 0}
        
        total_cpu = sum(vm.get("cpu_usage", 0) for vm in self.vms.values())
        total_memory = sum(vm.get("memory_usage", 0) for vm in self.vms.values())
        
        return {
            "total_vms": len(self.vms),
            "average_cpu_usage": total_cpu / len(self.vms),
            "average_memory_usage": total_memory / len(self.vms),
            "topology_density": sum(len(v) for v in self.topology.values()) / max(len(self.vms), 1)
        }
