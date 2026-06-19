@echo off
REM OmniDesk AI v1.1.0 - 集成版启动脚本
REM 完整的前后端集成版本

setlocal enabledelayedexpansion

echo ========================================
echo  OmniDesk AI v1.1.0 - 集成版
echo  前后端完全对接
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python
    echo 请先安装 Python 3.9 或更高版本
    pause
    exit /b 1
)

echo ✓ Python 已安装

REM 检查 PyQt6 是否安装
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo 正在安装 PyQt6...
    pip install PyQt6 -q
    if errorlevel 1 (
        echo 错误: PyQt6 安装失败
        pause
        exit /b 1
    )
)

echo ✓ PyQt6 已安装

REM 检查其他依赖
echo 正在检查依赖...
pip install -q fastapi uvicorn requests python-dotenv

REM 启动应用
echo.
echo 正在启动 OmniDesk AI (集成版)...
echo.

cd /d "%~dp0"

REM 使用集成版前端
python frontend/app_integrated.py

if errorlevel 1 (
    echo.
    echo 应用启动失败
    pause
)

endlocal
