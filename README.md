# Text2Map - 文本转思维导图工具

🧠 一个基于 AI 的智能文本转思维导图工具，使用 Streamlit 构建的 Web 应用，能够将长文本（如文章、会议记录、播客文稿等）自动转换为结构化的思维导图。

## ✨ 功能特点

- **智能转换**：基于 Google Gemini AI 模型，自动分析文本结构和关键信息
- **可视化展示**：使用交互式思维导图展示文本内容的层级关系
- **简洁界面**：基于 Streamlit 的简洁友好的 Web 界面
- **多格式支持**：支持 Markdown 格式的源码查看和复制
- **实时处理**：在线实时文本处理，无需本地安装复杂环境

## 🛠️ 技术栈

- **前端框架**：Streamlit
- **AI 模型**：Google Gemini 1.5 Flash
- **思维导图组件**：streamlit-markmap
- **编程语言**：Python 3.x

## 📋 系统要求

- Python 3.8+
- Google AI API Key（Gemini）

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/qingchejun/text2map.git
cd text2map
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

创建 `.env` 文件并添加你的 Google AI API Key：

```env
GOOGLE_API_KEY=your_google_ai_api_key_here
```

### 4. 运行应用

```bash
streamlit run streamlit_app.py
```

应用将在浏览器中自动打开，通常地址为：`http://localhost:8501`

## 📖 使用说明

1. **输入文本**：在文本框中粘贴或输入要转换的文本内容
2. **生成思维导图**：点击"生成思维导图"按钮
3. **查看结果**：系统将自动生成交互式思维导图
4. **查看源码**：可在下方展开区域查看生成的 Markdown 源码

## 📁 项目结构

```
text2map/
├── main.py              # 核心 AI 处理逻辑
├── streamlit_app.py     # Streamlit Web 应用
├── requirements.txt     # 项目依赖
├── README.md           # 项目说明文档
└── .env                # 环境变量配置（需自创建）
```

## 🔧 命令行使用

除了 Web 界面外，还支持命令行模式：

1. 创建 `input.txt` 文件，将要处理的文本内容放入其中
2. 运行命令：`python main.py`
3. 处理结果将保存到 `output.md` 文件中

## ⚠️ 注意事项

- 确保网络连接正常，需要访问 Google AI API
- API Key 请妥善保管，不要提交到公共代码仓库
- 处理大文本可能需要较长时间，请耐心等待
- 建议输入文本长度适中，过长可能影响生成质量

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 📄 许可证

MIT License

## 📞 联系方式

如有问题或建议，请通过 GitHub Issues 联系。
