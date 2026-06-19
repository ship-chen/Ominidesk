#!/bin/bash
# OmniDesk AI v1.1.0 - 集成版启动脚本
# 完整的前后端集成版本

echo "========================================"
echo " OmniDesk AI v1.1.0 - 集成版"
echo " 前后端完全对接"
echo "========================================"
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python"
    echo "请先安装 Python 3.9 或更高版本"
    exit 1
fi

echo "✓ Python 已安装"

# 检查 PyQt6 是否安装
python3 -c "import PyQt6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "正在安装 PyQt6..."
    pip3 install PyQt6 -q
    if [ $? -ne 0 ]; then
        echo "错误: PyQt6 安装失败"
        exit 1
    fi
fi

echo "✓ PyQt6 已安装"

# 检查其他依赖
echo "正在检查依赖..."
pip3 install -q fastapi uvicorn requests python-dotenv

# 启动应用
echo ""
echo "正在启动 OmniDesk AI (集成版)..."
echo ""

cd "$(dirname "$0")"

# 使用集成版前端
python3 frontend/app_integrated.py

if [ $? -ne 0 ]; then
    echo ""
    echo "应用启动失败"
    exit 1
fi
