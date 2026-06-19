#!/usr/bin/env python3
"""
任务规划引擎 - 任务分解和规划
v1.1 - 修复 f-string 错误
"""

import asyncio
import logging
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime
import uuid
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class TaskPriority(str, Enum):
    """任务优先级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class Task:
    """任务数据类"""
    task_id: str
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    subtasks: List[str] = field(default_factory=list)
    goal: Optional[str] = None
    reasoning_chain: List[str] = field(default_factory=list)


class TaskPlanningEngine:
    """任务规划引擎"""
    
    def __init__(self):
        """初始化任务规划引擎"""
        self.tasks: Dict[str, Task] = {}
        self.task_dependencies: Dict[str, List[str]] = {}  # 任务依赖关系
        logger.info("✓ 任务规划引擎已初始化")
    
    async def create_task(self, title: str, description: str = "", 
                         priority: str = "medium") -> Optional[Task]:
        """创建任务
        
        Args:
            title: 任务标题
            description: 任务描述
            priority: 优先级
        
        Returns:
            创建的任务或 None
        """
        try:
            task_id = str(uuid.uuid4())
            priority_enum = TaskPriority(priority.lower())
            
            task = Task(
                task_id=task_id,
                title=title,
                description=description,
                priority=priority_enum,
                goal=description
            )
            
            self.tasks[task_id] = task
            self.task_dependencies[task_id] = []
            
            logger.info(f"✓ 创建任务: {title} ({task_id})")
            return task
        except Exception as e:
            logger.error(f"✗ 创建任务失败: {e}")
            return None
    
    async def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务
        
        Args:
            task_id: 任务 ID
        
        Returns:
            任务对象或 None
        """
        if task_id not in self.tasks:
            logger.warning(f"任务不存在: {task_id}")
            return None
        
        return self.tasks[task_id]
    
    async def update_task_status(self, task_id: str, status: str) -> bool:
        """更新任务状态
        
        Args:
            task_id: 任务 ID
            status: 新状态
        
        Returns:
            更新是否成功
        """
        if task_id not in self.tasks:
            logger.error(f"任务不存在: {task_id}")
            return False
        
        try:
            status_enum = TaskStatus(status.lower())
            task = self.tasks[task_id]
            task.status = status_enum
            task.updated_at = datetime.now()
            logger.info(f"✓ 任务状态已更新: {task.title} -> {status}")
            return True
        except Exception as e:
            logger.error(f"✗ 更新任务状态失败: {e}")
            return False
    
    async def decompose_task(self, task_id: str, subtasks: List[str]) -> bool:
        """分解任务为子任务
        
        Args:
            task_id: 任务 ID
            subtasks: 子任务列表
        
        Returns:
            分解是否成功
        """
        if task_id not in self.tasks:
            logger.error(f"任务不存在: {task_id}")
            return False
        
        try:
            task = self.tasks[task_id]
            task.subtasks = subtasks
            logger.info(f"✓ 任务已分解: {task.title} -> {len(subtasks)} 个子任务")
            return True
        except Exception as e:
            logger.error(f"✗ 分解任务失败: {e}")
            return False
    
    async def add_reasoning_chain(self, task_id: str, reasoning: List[str]) -> bool:
        """添加推理链
        
        Args:
            task_id: 任务 ID
            reasoning: 推理步骤列表
        
        Returns:
            添加是否成功
        """
        if task_id not in self.tasks:
            logger.error(f"任务不存在: {task_id}")
            return False
        
        try:
            task = self.tasks[task_id]
            task.reasoning_chain = reasoning
            logger.info(f"✓ 推理链已添加: {len(reasoning)} 步")
            return True
        except Exception as e:
            logger.error(f"✗ 添加推理链失败: {e}")
            return False
    
    async def list_tasks(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出任务
        
        Args:
            status: 过滤状态 (可选)
        
        Returns:
            任务列表
        """
        result = []
        for task in self.tasks.values():
            if status and task.status.value != status:
                continue
            
            result.append({
                "task_id": task.task_id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority.value,
                "status": task.status.value,
                "created_at": task.created_at.isoformat(),
                "subtasks_count": len(task.subtasks)
            })
        
        return result
    
    async def get_statistics(self) -> Dict[str, Any]:
        """获取任务统计信息
        
        Returns:
            统计信息字典
        """
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED)
        running = sum(1 for t in self.tasks.values() if t.status == TaskStatus.RUNNING)
        failed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED)
        
        return {
            "total_tasks": total,
            "completed": completed,
            "running": running,
            "failed": failed,
            "pending": total - completed - running - failed,
            "completion_rate": f"{(completed / total * 100):.1f}%" if total > 0 else "0%"
        }
