#!/usr/bin/env python3
"""
日志系统模块 - 统一日志管理
v1.0 - 完全实现版本
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional
from datetime import datetime


class LoggerSetup:
    """日志系统设置"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerSetup, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._setup_logging()
            LoggerSetup._initialized = True
    
    def _setup_logging(self):
        """设置日志系统"""
        # 创建日志目录
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 获取根日志记录器
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        # 文件处理器（轮转）
        log_file = log_dir / f"omnidesk_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=10,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        
        # 错误文件处理器
        error_log_file = log_dir / f"omnidesk_error_{datetime.now().strftime('%Y%m%d')}.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file,
            maxBytes=10*1024*1024,
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        root_logger.addHandler(error_handler)
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """获取日志记录器
        
        Args:
            name: 记录器名称
        
        Returns:
            日志记录器
        """
        return logging.getLogger(name)


# 初始化日志系统
_logger_setup = LoggerSetup()

# 提供便利函数
def get_logger(name: str) -> logging.Logger:
    """获取日志记录器
    
    Args:
        name: 记录器名称
    
    Returns:
        日志记录器
    """
    return LoggerSetup.get_logger(name)
