#!/usr/bin/env python3
"""
AI 大脑模块 - 多模型管理和调用
v1.2 - 修复 bug，增强错误处理
"""

import asyncio
import logging
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class ModelProvider(str, Enum):
    """模型提供商"""
    OPENAI = "openai"
    ALIYUN = "aliyun"
    ZHIPU = "zhipu"
    BAIDU = "baidu"
    OLLAMA = "ollama"
    LLAMACPP = "llamacpp"


class ModelType(str, Enum):
    """模型类型"""
    CLOUD = "cloud"
    LOCAL = "local"
    HYBRID = "hybrid"


class AIModel:
    """AI 模型数据类"""
    def __init__(self, name: str, provider: ModelProvider, model_type: ModelType, endpoint: str = ""):
        self.id = str(uuid.uuid4())
        self.name = name
        self.provider = provider
        self.model_type = model_type
        self.endpoint = endpoint
        self.created_at = datetime.now()
        self.is_active = False


class AIBrain:
    """AI 大脑 - 管理多个 AI 模型"""
    
    def __init__(self):
        """初始化 AI 大脑"""
        self.models: List[AIModel] = []
        self.current_model: Optional[AIModel] = None
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 100
        logger.info("✓ AI 大脑已初始化")
    
    def add_model(self, name: str, provider: str, model_type: str, endpoint: str = "") -> bool:
        """添加 AI 模型"""
        try:
            provider_enum = ModelProvider(provider.lower())
            type_enum = ModelType(model_type.lower())
            
            model = AIModel(name=name, provider=provider_enum, model_type=type_enum, endpoint=endpoint)
            self.models.append(model)
            
            if not self.current_model:
                self.current_model = model
                model.is_active = True
            
            logger.info(f"✓ 添加模型: {name} ({provider})")
            return True
        except (ValueError, Exception) as e:
            logger.error(f"✗ 添加模型失败: {e}")
            return False
    
    def list_models(self) -> List[str]:
        """获取模型列表"""
        return [f"{m.name} ({m.provider.value})" for m in self.models]
    
    def select_model(self, model_name: str) -> bool:
        """选择模型"""
        for model in self.models:
            if model.name.lower() == model_name.lower():
                if self.current_model:
                    self.current_model.is_active = False
                self.current_model = model
                model.is_active = True
                logger.info(f"✓ 已切换到模型: {model_name}")
                return True
        
        logger.warning(f"✗ 找不到模型: {model_name}")
        return False
    
    def get_current_model(self) -> Optional[str]:
        """获取当前模型"""
        if self.current_model:
            return f"{self.current_model.name} ({self.current_model.provider.value})"
        return None
    
    async def call_model(self, prompt: str, **kwargs) -> Optional[str]:
        """调用当前模型"""
        if not self.current_model:
            logger.error("✗ 未选择模型")
            return None
        
        try:
            logger.info(f"调用模型: {self.current_model.name}")
            # 这里实现实际的 API 调用
            response = await self._call_api(self.current_model, prompt, **kwargs)
            
            # 添加到对话历史
            self.conversation_history.append({
                "role": "user",
                "content": prompt
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            # 限制历史记录长度
            if len(self.conversation_history) > self.max_history:
                self.conversation_history = self.conversation_history[-self.max_history:]
            
            return response
        except Exception as e:
            logger.error(f"✗ 调用模型失败: {e}")
            return None
    
    async def _call_api(self, model: AIModel, prompt: str, **kwargs) -> str:
        """调用 API (实现占位符)"""
        # 实现各个提供商的 API 调用
        if model.provider == ModelProvider.OPENAI:
            return await self._call_openai(model, prompt, **kwargs)
        elif model.provider == ModelProvider.OLLAMA:
            return await self._call_ollama(model, prompt, **kwargs)
        else:
            return "模型调用未实现"
    
    async def _call_openai(self, model: AIModel, prompt: str, **kwargs) -> str:
        """调用 OpenAI API"""
        # 实现占位符
        await asyncio.sleep(0.1)
        return f"OpenAI 响应: {prompt}"
    
    async def _call_ollama(self, model: AIModel, prompt: str, **kwargs) -> str:
        """调用 Ollama 本地模型"""
        # 实现占位符
        await asyncio.sleep(0.1)
        return f"Ollama 响应: {prompt}"
    
    def clear_history(self) -> None:
        """清除对话历史"""
        self.conversation_history.clear()
        logger.info("✓ 对话历史已清除")
    
    def get_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.conversation_history.copy()
