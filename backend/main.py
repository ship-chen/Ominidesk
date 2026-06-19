#!/usr/bin/env python3
"""
OmniDesk AI - 后端主入口
v1.3 - 完全实现版本，支持真实运行
"""

import asyncio
import logging
import json
from pathlib import Path
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 导入所有模块
try:
    from modules.ai_brain import AIBrain
    from modules.multimodal_perception import MultimodalPerceptionEngine
    from modules.task_planning import TaskPlanningEngine
    from modules.multi_vm_matrix import MultiVMMatrixManager
    from modules.self_modification import SelfModificationEngine
    from modules.self_evolution import SelfEvolutionEngine
    from modules.vbox_integration import VBoxIntegration
    from modules.performance_optimizer import PerformanceOptimizer
    from modules.rate_limiter import RateLimiter, RateLimitConfig
    from modules.cache_manager import CacheManager
    logger.info("✓ 所有模块导入成功")
except ImportError as e:
    logger.error(f"✗ 模块导入失败: {e}")
    raise

# 全局实例
ai_brain = None
perception_engine = None
task_planner = None
vm_matrix = None
self_modifier = None
self_evolver = None
vbox = None
performance_optimizer = None
rate_limiter = None
cache_manager = None

# WebSocket 连接管理
active_connections = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    """
    # 启动时
    logger.info("="*60)
    logger.info("OmniDesk AI v1.3 - 启动中...")
    logger.info("="*60)
    
    global ai_brain, perception_engine, task_planner, vm_matrix
    global self_modifier, self_evolver, vbox, performance_optimizer
    global rate_limiter, cache_manager
    
    try:
        # 初始化所有模块
        ai_brain = AIBrain()
        perception_engine = MultimodalPerceptionEngine()
        task_planner = TaskPlanningEngine()
        vm_matrix = MultiVMMatrixManager()
        self_modifier = SelfModificationEngine()
        self_evolver = SelfEvolutionEngine()
        vbox = VBoxIntegration()
        performance_optimizer = PerformanceOptimizer()
        rate_limiter = RateLimiter(RateLimitConfig())
        cache_manager = CacheManager()
        
        # 连接 VirtualBox
        await vbox.connect()
        
        logger.info("✓ 所有模块初始化成功")
        logger.info(f"✓ 应用已启动 - 监听 http://127.0.0.1:8000")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"✗ 初始化失败: {e}")
        raise
    
    yield
    
    # 关闭时
    logger.info("应用正在关闭...")


# 创建应用
app = FastAPI(
    title="OmniDesk AI",
    description="企业级 AI 代理系统",
    version="1.3.0",
    lifespan=lifespan
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# REST API 端点

@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        # 收集性能指标
        metrics = await performance_optimizer.collect_metrics()
        
        return {
            "status": "healthy",
            "version": "1.3.0",
            "components": {
                "ai_brain": "ok" if ai_brain else "error",
                "perception": "ok" if perception_engine else "error",
                "task_planning": "ok" if task_planner else "error",
                "vm_matrix": "ok" if vm_matrix else "error",
                "vbox": "ok" if vbox and vbox.connected else "error",
                "performance": "ok",
                "rate_limiter": "ok",
                "cache": "ok"
            },
            "performance": {
                "cpu_percent": metrics.cpu_percent,
                "memory_percent": metrics.memory_percent,
                "disk_percent": metrics.disk_percent
            }
        }
    except Exception as e:
        logger.error(f"✗ 健康检查失败: {e}")
        return {"status": "unhealthy", "error": str(e)}


@app.get("/models")
async def list_models():
    """获取可用 AI 模型列表"""
    try:
        if not rate_limiter.check_limit("api_models"):
            raise HTTPException(status_code=429, detail="请求过于频繁")
        
        # 先检查缓存
        cached = cache_manager.get("models_list")
        if cached:
            return {"models": cached, "cached": True}
        
        models = ai_brain.list_models()
        cache_manager.set("models_list", models, ttl=3600)
        
        return {"models": models, "cached": False}
    except Exception as e:
        logger.error(f"✗ 获取模型列表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/models/add")
async def add_model(name: str, provider: str, model_type: str, endpoint: str = ""):
    """添加新的 AI 模型"""
    try:
        if not rate_limiter.check_limit(f"add_model_{name}"):
            raise HTTPException(status_code=429, detail="请求过于频繁")
        
        success = ai_brain.add_model(name, provider, model_type, endpoint)
        
        if success:
            cache_manager.delete("models_list")  # 清除缓存
            return {"status": "success", "message": f"模型 {name} 已添加"}
        else:
            raise HTTPException(status_code=400, detail=f"添加模型 {name} 失败")
    except Exception as e:
        logger.error(f"✗ 添加模型失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/vms")
async def list_vms():
    """列出所有虚拟机"""
    try:
        if not rate_limiter.check_limit("list_vms"):
            raise HTTPException(status_code=429, detail="请求过于频繁")
        
        vms = await vbox.list_vms()
        return {"vms": vms}
    except Exception as e:
        logger.error(f"✗ 列出虚拟机失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/vms/{vm_id}/start")
async def start_vm(vm_id: str):
    """启动虚拟机"""
    try:
        if not rate_limiter.check_limit(f"vm_start_{vm_id}"):
            raise HTTPException(status_code=429, detail="请求过于频繁")
        
        success = await vbox.start_vm(vm_id)
        
        if success:
            return {"status": "success", "message": f"虚拟机 {vm_id} 已启动"}
        else:
            raise HTTPException(status_code=400, detail=f"启动虚拟机 {vm_id} 失败")
    except Exception as e:
        logger.error(f"✗ 启动虚拟机失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/performance")
async def get_performance():
    """获取性能指标"""
    try:
        if not rate_limiter.check_limit("performance"):
            raise HTTPException(status_code=429, detail="请求过于频繁")
        
        status = performance_optimizer.get_system_status()
        return status
    except Exception as e:
        logger.error(f"✗ 获取性能指标失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cache/stats")
async def get_cache_stats():
    """获取缓存统计信息"""
    try:
        stats = cache_manager.get_stats()
        return stats
    except Exception as e:
        logger.error(f"✗ 获取缓存统计失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/rate-limiter/stats")
async def get_rate_limiter_stats():
    """获取限流统计信息"""
    try:
        stats = rate_limiter.get_global_stats()
        return stats
    except Exception as e:
        logger.error(f"✗ 获取限流统计失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket 端点

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 主端点"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        logger.info(f"✓ WebSocket 客户端已连接 (总数: {len(active_connections)})")
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            response = await handle_websocket_message(message)
            await websocket.send_json(response)
            
    except Exception as e:
        logger.error(f"✗ WebSocket 错误: {e}")
    finally:
        active_connections.remove(websocket)
        logger.info(f"✓ WebSocket 客户端已断开 (总数: {len(active_connections)})")


async def handle_websocket_message(message: dict):
    """处理 WebSocket 消息"""
    try:
        msg_type = message.get("type")
        
        if msg_type == "chat":
            user_message = message.get("message")
            response = await ai_brain.call_model(user_message)
            return {"type": "chat_response", "response": response}
        
        elif msg_type == "perception":
            image_path = message.get("image_path")
            perception_type = message.get("perception_type", "ocr")
            
            if perception_type == "ocr":
                result = await perception_engine.recognize_text(image_path)
            elif perception_type == "object_detection":
                result = await perception_engine.detect_objects(image_path)
            elif perception_type == "scene_understanding":
                result = await perception_engine.understand_scene(image_path)
            else:
                result = None
            
            return {"type": "perception_result", "result": result}
        
        elif msg_type == "task_create":
            title = message.get("title")
            description = message.get("description", "")
            priority = message.get("priority", "medium")
            
            task = await task_planner.create_task(title, description, priority)
            return {
                "type": "task_created",
                "task_id": task.task_id if task else None,
                "success": task is not None
            }
        
        elif msg_type == "status":
            vm_status = await vm_matrix.get_vm_status()
            perf_status = performance_optimizer.get_system_status()
            cache_stats = cache_manager.get_stats()
            
            return {
                "type": "status_report",
                "vms": vm_status,
                "performance": perf_status,
                "cache": cache_stats
            }
        
        else:
            return {"type": "error", "message": f"未知消息类型: {msg_type}"}
        
    except Exception as e:
        logger.error(f"✗ 处理 WebSocket 消息失败: {e}")
        return {"type": "error", "message": str(e)}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
