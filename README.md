# Text2Map - 智能文本转思维导图工具

> **当前版本：V4.1 - 文件上传功能完成版** (2025-07-20)
>
> 项目已完成基础架构搭建，支持文本输入和文件上传功能，具备完整的思维导图生成能力。详细开发路线图请见 [`CLAUDE.md`](CLAUDE.md)。

🧠 一个基于 AI 的智能文本转思维导图工具，采用现代化前后端分离架构，能够将长文本（如文章、会议记录、播客文稿、字幕文件等）自动转换为结构化的交互式思维导图。

## ✨ 功能特点

- **🤖 智能分析**：基于 Google Gemini 1.5 Flash 模型，深度理解文本结构和逻辑关系
- **📊 可视化展示**：交互式思维导图，支持缩放、折叠和导航
- **🎨 现代界面**：基于 Next.js + Tailwind CSS 的美观 UI，支持亮色/暗色主题切换
- **📁 多格式支持**：支持 TXT、MD、DOCX、PDF、SRT 等多种文件格式
- **📤 文件上传**：拖拽式文件上传界面，智能解析文件内容
- **📱 响应式设计**：完美适配桌面和移动设备
- **⚡ 高性能**：前后端分离架构，快速响应和流畅交互

## 🛠️ 技术栈

### 前端 (Next.js)

- **框架**：Next.js 15.4.2 + React 19.1.0
- **样式**：Tailwind CSS 4.0
- **语言**：TypeScript
- **思维导图**：Markmap-view
- **图标**：Lucide React

### 后端 (FastAPI)

- **框架**：FastAPI
- **AI 模型**：Google Gemini 1.5 Flash
- **文档处理**：PyPDF2、python-docx、srt
- **语言**：Python 3.x

## 📋 系统要求

- Node.js 18+
- Python 3.8+
- Google AI API Key（Gemini）
- 现代浏览器（推荐 Chrome、Firefox、Safari）

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/qingchejun/text2map.git
cd text2map
```

### 2. 配置环境变量

创建 `.env` 文件并添加你的 Google AI API Key：

```env
GOOGLE_API_KEY=your_google_ai_api_key_here
```

### 3. 启动后端服务

```bash
# 进入后端目录
cd backend

# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动后端服务
python main.py
```

后端服务将在 `http://localhost:8000` 启动

### 4. 启动前端服务

```bash
# 新开一个终端，进入前端目录
cd frontend

# 安装依赖
npm install

# 启动前端服务
npm run dev
```

前端服务将在 `http://localhost:3000` 启动

## 📖 使用说明

### 🖥️ Web 界面操作

1. **📝 文本输入**：

   - 在文本框中直接输入或粘贴文本内容
   - 支持长文本，如文章、会议记录、学术论文等

2. **📁 文件上传**：

   - 点击"或者... 上传文件"区域选择文件
   - 支持格式：`.txt`、`.md`、`.docx`、`.pdf`、`.srt`
   - 文件大小限制：50MB
   - 选择文件后会显示文件名和大小

3. **🚀 生成思维导图**：

   - 点击"生成思维导图"按钮
   - 系统会自动判断使用文本输入还是文件上传
   - AI 将智能分析文本结构和关键信息

4. **🎯 查看和操作结果**：
   - 交互式思维导图支持缩放、拖拽和节点展开/折叠
   - 支持主题切换（亮色/暗色模式）

## 📁 项目结构

```
text2map/
├── backend/                  # 后端 FastAPI 应用
│   ├── main.py              # FastAPI 应用入口
│   ├── requirements.txt     # 后端依赖
│   └── venv/                # Python 虚拟环境
├── frontend/                # 前端 Next.js 应用
│   ├── src/
│   │   └── app/
│   │       └── page.tsx     # 主页面组件
│   ├── package.json         # 前端依赖
│   └── tailwind.config.ts   # Tailwind 配置
├── README.md               # 项目说明文档
├── CLAUDE.md              # 详细开发文档
└── .env                   # 环境变量配置（需自创建）
```

## 🔧 API 接口

### 后端 API 端点

- `GET /` - 健康检查
- `POST /generate` - 从文本生成思维导图
- `POST /generate-from-file` - 从文件生成思维导图

### 请求示例

**文本输入**：

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "你的文本内容"}'
```

**文件上传**：

```bash
curl -X POST http://localhost:8000/generate-from-file \
  -F "file=@your_file.txt"
```

## ⚠️ 注意事项

- **🔐 API 安全**：Google AI API Key 请妥善保管，不要提交到公共代码仓库
- **🌐 网络要求**：确保网络连接正常，需要访问 Google AI API 服务
- **⏱️ 处理时间**：处理大文本可能需要较长时间，请耐心等待
- **📝 文本长度**：建议单次处理文本长度在 50KB 以内
- **📁 文件大小**：文件上传限制为 50MB
- **🔄 重试机制**：如果生成失败，可以重新尝试
- **💻 浏览器兼容性**：推荐使用现代浏览器以获得最佳视觉效果

## 🎨 界面特色

- **现代设计**：采用卡片式布局，玻璃态效果和渐变背景
- **主题切换**：支持亮色/暗色主题，自动保存用户偏好
- **流畅动画**：悬浮效果、按钮动画和过渡效果
- **响应式布局**：完美适配桌面、平板和手机设备
- **文件上传**：拖拽式上传界面，直观的文件状态显示
- **交互反馈**：丰富的视觉反馈和状态提示

## 🗺️ 开发路线图

### ✅ 已完成 (V4.1)

- **后端**：FastAPI 架构，支持文本和文件处理
- **前端**：Next.js + Tailwind CSS，现代化 UI 设计
- **核心功能**：文本输入、文件上传、思维导图生成
- **用户体验**：主题切换、响应式设计、错误处理

### 🚧 进行中

- **数据库集成**：PostgreSQL + SQLAlchemy
- **用户系统**：注册、登录、使用记录

### 📋 计划中

- **商业化功能**：付费档位、支付流程
- **高级功能**：协作编辑、模板系统
- **性能优化**：缓存、CDN、负载均衡

> 详细开发计划请参考 [`CLAUDE.md`](CLAUDE.md) 文档。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。
