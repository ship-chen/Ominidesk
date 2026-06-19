# OmniDesk AI - 原点·本地云电脑

一个模块化原生 Windows 桌面应用，将 AI 全权控制的 Windows 虚拟机置于本地。

## 项目概述

**OmniDesk AI** 是一个企业级的 AI 代理系统，具有以下特点：

- **原生 Windows 应用**：基于 Electron + React 前端，Python 后端
- **虚拟机集成**：通过 VirtualBox 集成，支持多虚拟机管理
- **AI 全权控制**：支持多模型（云端/本地），智能任务规划与执行
- **三层感知体系**：结构层（UI 元素）、文字层（OCR）、语义层（VL 模型）
- **安全隔离**：虚拟机内安全策略、宿主机权限管理、完整审计日志
- **极简美学**：Claude 桌面端风格，零干扰用户界面

## 技术栈

### 前端
- **Electron 28+** - 原生窗口框架
- **React 19** - UI 框架
- **TypeScript** - 类型安全
- **Tailwind CSS** - 样式系统

### 后端
- **Python 3.11+** - 核心语言
- **FastAPI** - WebSocket 服务
- **VirtualBox SDK** - 虚拟机控制
- **PaddleOCR** - 文字识别
- **PyInstaller** - 打包为 EXE

### 虚拟化
- **VirtualBox 7.x** - 虚拟机管理
- **Windows API** - 窗口嵌入（SetParent）

### AI 模型
- **OpenAI API** - 云端模型
- **Ollama / llama.cpp** - 本地模型
- 支持国产模型：智谱、通义千问、文心等

## 项目结构

```
omnidesk-windows/
├── frontend/                    # 前端（Electron + React）
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.jsx             # 主应用
│   │   ├── App.css             # 样式
│   │   └── components/         # 组件库
│   │       ├── Sidebar.jsx     # 侧边栏
│   │       ├── ChatPanel.jsx   # 聊天面板
│   │       ├── VMEmbed.jsx     # 虚拟机嵌入
│   │       ├── HostPermissionDialog.jsx
│   │       ├── AgentTimeline.jsx
│   │       ├── SecurityPanel.jsx
│   │       └── Settings.jsx
│   ├── main.js                 # Electron 主进程
│   └── preload.js              # 预加载脚本
│
├── backend/                     # 后端（Python）
│   ├── main.py                 # 入口
│   ├── modules/                # 核心模块
│   │   ├── vbox_controller.py      # VirtualBox 控制
│   │   ├── ai_brain.py             # AI 大脑
│   │   ├── perception_engine.py    # 感知引擎
│   │   ├── agent_engine.py         # 任务代理
│   │   └── security_audit.py       # 安全审计
│   └── requirements.txt
│
├── launcher/                    # 启动器（C++）
├── updater/                     # 更新组件（C++）
├── vbox-service/                # VirtualBox 服务（C++）
├── model-runner/                # 本地模型服务（Python）
├── skills/                      # 技能库
├── docs/                        # 文档
└── config/                      # 配置文件
```

## 快速开始

### 环境要求

- Windows 10/11 64 位
- Python 3.11+
- Node.js 18+
- VirtualBox 7.x
- 内存：24GB（云端）/ 32GB（本地模型）

### 安装依赖

```bash
# 安装前端依赖
cd frontend
npm install

# 安装后端依赖
cd ../backend
pip install -r requirements.txt
```

### 开发运行

```bash
# 启动前端开发服务器
cd frontend
npm run dev

# 在另一个终端启动后端
cd backend
python main.py
```

### 构建打包

```bash
# 构建前端
cd frontend
npm run build

# 打包为 EXE
npm run package
```

## 核心功能

### Phase 1 - MVP（v1.0）
- ✅ 单虚拟机嵌入与控制
- ✅ AI 对话与任务执行
- ✅ 三层感知引擎
- ✅ 文件隔离
- ✅ 宿主机权限管理
- ✅ 应用自愈
- ✅ 语音输入
- ✅ 本地模型支持

### Phase 2 - 增强版（v1.5）
- ⬜ 多虚拟机矩阵
- ⬜ 技能编辑器
- ⬜ 开发环境自动搭建
- ⬜ 项目脚手架

### Phase 3 - 完整版（v2.0）
- ⬜ 技能市场
- ⬜ 插件 API
- ⬜ 高级网络安全
- ⬜ WinPE 修复

## 配置说明

### 后端配置

编辑 `config/backend.config.yaml`：

```yaml
# WebSocket 服务
backend:
  host: 127.0.0.1
  port: 8000

# VirtualBox 配置
virtualbox:
  path: "C:\\Program Files\\Oracle\\VirtualBox"
  default_memory: 6144
  default_disk: 50

# AI 模型配置
models:
  default: "gpt-4"
  cloud:
    openai:
      api_key: "sk-xxx"
      endpoint: "https://api.openai.com/v1"
  local:
    ollama:
      endpoint: "http://127.0.0.1:11434"
```

### 前端配置

编辑 `frontend/.env`：

```env
REACT_APP_BACKEND_URL=http://127.0.0.1:8000
REACT_APP_WS_URL=ws://127.0.0.1:8000/ws
```

## API 文档

### WebSocket 通信协议

#### 认证

```json
{
  "type": "auth",
  "token": "session_token"
}
```

#### 聊天请求

```json
{
  "type": "chat",
  "message": "用户输入",
  "model": "gpt-4"
}
```

#### 虚拟机控制

```json
{
  "type": "vm_control",
  "action": "click|type|screenshot|start|stop",
  "params": {
    "vm_id": "vm_id",
    "x": 100,
    "y": 100
  }
}
```

#### 权限请求

```json
{
  "type": "permission_request",
  "action": "open_application",
  "resource": "notepad.exe",
  "description": "打开记事本应用"
}
```

## 安全特性

### 虚拟机内安全
- 命令白名单与黑名单
- 操作规则过滤
- 快照恢复机制

### 宿主机安全
- 权限白名单
- 单次授权机制
- 30秒超时自动拒绝

### 审计日志
- 所有操作记录
- 加密存储
- 可视化查看

## 故障排除

### 后端连接失败

```bash
# 检查后端服务是否运行
python backend/main.py

# 检查端口是否被占用
netstat -ano | findstr :8000
```

### VirtualBox 集成问题

```bash
# 检查 VirtualBox 安装
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" --version

# 启用 VT-x/AMD-V
# 需要在 BIOS 中启用虚拟化
```

### 内存占用过高

```bash
# 减少虚拟机内存分配
# 编辑 config/backend.config.yaml
# 修改 default_memory 值
```

## 开发指南

### 添加新模块

1. 在 `backend/modules/` 中创建新文件
2. 实现模块类
3. 在 `backend/main.py` 中导入并初始化
4. 通过 WebSocket 暴露 API

### 添加新组件

1. 在 `frontend/src/components/` 中创建新文件
2. 实现 React 组件
3. 在 `App.jsx` 中导入并使用
4. 添加样式文件

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

- 项目主页：https://github.com/omnidesk-ai/omnidesk-windows
- 问题反馈：https://github.com/omnidesk-ai/omnidesk-windows/issues

---

**OmniDesk AI v1.0.0** - 原点·本地云电脑
