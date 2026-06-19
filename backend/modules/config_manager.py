#!/usr/bin/env python3
"""
配置管理模块 - 加载和管理配置
v1.0 - 完全实现版本
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = None):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file or self._get_default_config_path()
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def _get_default_config_path(self) -> str:
        """获取默认配置文件路径"""
        # 查找项目根目录的 config 文件夹
        paths = [
            "config/config.json",
            "../config/config.json",
            "../../config/config.json"
        ]
        
        for path in paths:
            if Path(path).exists():
                return path
        
        # 如果没有找到，返回默认位置
        return "config/config.json"
    
    def load_config(self) -> bool:
        """加载配置文件
        
        Returns:
            加载是否成功
        """
        try:
            config_path = Path(self.config_file)
            
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                logger.info(f"✓ 配置已加载: {self.config_file}")
                return True
            else:
                # 使用默认配置
                logger.warning(f"✗ 配置文件不存在: {self.config_file}")
                self._create_default_config()
                return False
        
        except Exception as e:
            logger.error(f"✗ 加载配置失败: {e}")
            self._create_default_config()
            return False
    
    def _create_default_config(self) -> None:
        """创建默认配置"""
        self.config = {
            "backend": {
                "host": "127.0.0.1",
                "port": 8000,
                "debug": False
            },
            "virtualbox": {
                "path": "C:\\Program Files\\Oracle\\VirtualBox",
                "default_memory": 4096,
                "default_disk": 50
            },
            "models": {
                "default": "ollama",
                "cloud": {
                    "openai": {
                        "api_key": "",
                        "endpoint": "https://api.openai.com/v1"
                    }
                },
                "local": {
                    "ollama": {
                        "endpoint": "http://127.0.0.1:11434"
                    }
                }
            },
            "performance": {
                "cpu_threshold": 80,
                "memory_threshold": 85,
                "disk_threshold": 90
            },
            "cache": {
                "max_size": 5000,
                "default_ttl": 3600
            },
            "rate_limit": {
                "requests_per_minute": 100,
                "requests_per_hour": 5000
            }
        }
        
        logger.info("✓ 使用默认配置")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值
        
        Args:
            key: 配置键 (支持点号分割: "backend.host")
            default: 默认值
        
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """设置配置值
        
        Args:
            key: 配置键 (支持点号分割: "backend.host")
            value: 配置值
        
        Returns:
            设置是否成功
        """
        try:
            keys = key.split('.')
            config = self.config
            
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            config[keys[-1]] = value
            return True
        except Exception as e:
            logger.error(f"✗ 设置配置失败: {e}")
            return False
    
    def save(self) -> bool:
        """保存配置到文件
        
        Returns:
            保存是否成功
        """
        try:
            config_path = Path(self.config_file)
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✓ 配置已保存: {self.config_file}")
            return True
        except Exception as e:
            logger.error(f"✗ 保存配置失败: {e}")
            return False
    
    def reload(self) -> bool:
        """重新加载配置
        
        Returns:
            加载是否成功
        """
        return self.load_config()
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有配置
        
        Returns:
            配置字典
        """
        return self.config.copy()


# 全局配置实例
config_manager = ConfigManager()
