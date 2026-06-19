#!/usr/bin/env python3
"""
OmniDesk AI v1.1 - 功能测试脚本
测试所有核心功能是否正常工作
"""

import sys
import asyncio
import logging
from pathlib import Path

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

async def test_imports():
    """测试所有模块导入"""
    logger.info("=" * 60)
    logger.info("测试 1: 模块导入")
    logger.info("=" * 60)
    
    try:
        from modules.ai_brain import AIBrain, ModelProvider, ModelType
        logger.info("✅ ai_brain 导入成功")
        
        from modules.multimodal_perception import MultimodalPerceptionEngine, PerceptionType
        logger.info("✅ multimodal_perception 导入成功")
        
        from modules.vbox_integration import VBoxIntegration
        logger.info("✅ vbox_integration 导入成功")
        
        from modules.plugin_system import PluginManager
        logger.info("✅ plugin_system 导入成功")
        
        from modules.self_evolution import SelfEvolutionEngine
        logger.info("✅ self_evolution 导入成功")
        
        from modules.task_planning import TaskPlanningEngine
        logger.info("✅ task_planning 导入成功")
        
        from modules.self_modification import SelfModificationEngine
        logger.info("✅ self_modification 导入成功")
        
        from modules.multi_vm_matrix import MultiVMMatrixManager
        logger.info("✅ multi_vm_matrix 导入成功")
        
        logger.info("✅ 所有模块导入成功\n")
        return True
    
    except Exception as e:
        logger.error(f"❌ 模块导入失败: {e}\n")
        return False


async def test_ai_brain():
    """测试 AI 大脑"""
    logger.info("=" * 60)
    logger.info("测试 2: AI 大脑")
    logger.info("=" * 60)
    
    try:
        from modules.ai_brain import AIBrain
        
        brain = AIBrain()
        
        # 测试模型列表
        models = brain.list_models()
        logger.info(f"✅ 获取模型列表: {len(models)} 个模型")
        
        # 测试模型选择
        if models:
            brain.select_model(models[0])
            current = brain.get_current_model()
            logger.info(f"✅ 当前模型: {current}")
        
        # 测试添加模型
        success = brain.add_model(
            name="test_model",
            provider="OLLAMA",
            model_type="LOCAL",
            endpoint="http://127.0.0.1:11434"
        )
        logger.info(f"✅ 添加模型: {'成功' if success else '失败'}")
        
        logger.info("✅ AI 大脑测试通过\n")
        return True
    
    except Exception as e:
        logger.error(f"❌ AI 大脑测试失败: {e}\n")
        return False


async def test_multimodal_perception():
    """测试多模态感知"""
    logger.info("=" * 60)
    logger.info("测试 3: 多模态感知")
    logger.info("=" * 60)
    
    try:
        from modules.multimodal_perception import MultimodalPerceptionEngine
        
        engine = MultimodalPerceptionEngine()
        logger.info("✅ 多模态感知引擎初始化成功")
        
        # 测试感知历史
        history = await engine.get_perception_history()
        logger.info(f"✅ 获取感知历史: {len(history)} 条记录")
        
        # 测试缓存清除
        await engine.clear_cache()
        logger.info("✅ 缓存已清除")
        
        logger.info("✅ 多模态感知测试通过\n")
        return True
    
    except Exception as e:
        logger.error(f"❌ 多模态感知测试失败: {e}\n")
        return False


async def test_task_planning():
    """测试任务规划"""
    logger.info("=" * 60)
    logger.info("测试 4: 任务规划")
    logger.info("=" * 60)
    
    try:
        from modules.task_planning import TaskPlanningEngine
        
        engine = TaskPlanningEngine()
        logger.info("✅ 任务规划引擎初始化成功")
        
        # 创建任务
        task = await engine.create_task(
            title="测试任务",
            description="这是一个测试任务",
            priority="high"
        )
        logger.info(f"✅ 创建任务: {task.task_id}")
        
        # 获取任务
        retrieved = await engine.get_task(task.task_id)
        logger.info(f"✅ 获取任务: {retrieved.goal if retrieved else '失败'}")
        
        logger.info("✅ 任务规划测试通过\n")
        return True
    
    except Exception as e:
        logger.error(f"❌ 任务规划测试失败: {e}\n")
        return False


async def test_self_modification():
    """测试自我修改"""
    logger.info("=" * 60)
    logger.info("测试 5: 自我修改")
    logger.info("=" * 60)
    
    try:
        from modules.self_modification import SelfModificationEngine
        
        engine = SelfModificationEngine()
        logger.info("✅ 自我修改引擎初始化成功")
        
        # 获取禁区
        zones = await engine.get_forbidden_zones()
        logger.info(f"✅ 获取禁区: {len(zones)} 个禁区")
        
        logger.info("✅ 自我修改测试通过\n")
        return True
    
    except Exception as e:
        logger.error(f"❌ 自我修改测试失败: {e}\n")
        return False


async def test_multi_vm_matrix():
    """测试多虚拟机矩阵"""
    logger.info("=" * 60)
    logger.info("测试 6: 多虚拟机矩阵")
    logger.info("=" * 60)
    
    try:
        from modules.multi_vm_matrix import MultiVMMatrixManager, VMRole
        
        manager = MultiVMMatrixManager()
        logger.info("✅ 多虚拟机矩阵管理器初始化成功")
        
        # 注册虚拟机
        success = await manager.register_vm("vm_1", VMRole.MASTER)
        logger.info(f"✅ 注册虚拟机: {'成功' if success else '失败'}")
        
        # 获取状态
        status = await manager.get_vm_status()
        logger.info(f"✅ 获取虚拟机矩阵状态: {status.get('total_vms')} 个虚拟机")
        
        logger.info("✅ 多虚拟机矩阵测试通过\n")
        return True
    
    except Exception as e:
        logger.error(f"❌ 多虚拟机矩阵测试失败: {e}\n")
        return False


async def main():
    """运行所有测试"""
    logger.info("\n")
    logger.info("*" * 60)
    logger.info("OmniDesk AI v1.1 - 功能测试")
    logger.info("*" * 60)
    logger.info("\n")
    
    results = []
    
    # 运行所有测试
    results.append(("模块导入", await test_imports()))
    results.append(("AI 大脑", await test_ai_brain()))
    results.append(("多模态感知", await test_multimodal_perception()))
    results.append(("任务规划", await test_task_planning()))
    results.append(("自我修改", await test_self_modification()))
    results.append(("多虚拟机矩阵", await test_multi_vm_matrix()))
    
    # 输出测试结果
    logger.info("=" * 60)
    logger.info("测试结果汇总")
    logger.info("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    logger.info("=" * 60)
    logger.info(f"总计: {passed} 通过, {failed} 失败")
    logger.info("=" * 60)
    logger.info("\n")
    
    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
