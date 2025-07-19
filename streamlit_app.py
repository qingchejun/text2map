import streamlit as st
from main import generate_mindmap_data
from streamlit_markmap import markmap
from datetime import datetime
import PyPDF2
from docx import Document
import io
import srt

# 设置页面配置
st.set_page_config(page_title="文本转思维导图", page_icon="🧠")

st.markdown(
    """
    <style>
    /* 导入现代字体 */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* 全局样式重置 */
    * {
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* 主背景 */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #667eea 100%);
        min-height: 100vh;
    }
    
    /* 主容器 - 增强层次感 */
    .main .block-container {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 3rem 2.5rem;
        margin: 2rem auto;
        max-width: 1200px;
        box-shadow: 
            0 32px 64px rgba(0, 0, 0, 0.12),
            0 16px 32px rgba(0, 0, 0, 0.08),
            0 8px 16px rgba(0, 0, 0, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.3);
        position: relative;
    }
    
    /* 主容器装饰效果 */
    .main .block-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        border-radius: 24px 24px 0 0;
    }
    
    /* 标题区域 */
    .title-section {
        text-align: center;
        margin-bottom: 3rem;
        position: relative;
    }
    
    h1 {
        color: #1a202c !important;
        font-weight: 700 !important;
        font-size: 3rem !important;
        text-align: center !important;
        margin-bottom: 0.5rem !important;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
    }
    
    h1 a { display: none !important; }
    
    /* 副标题 */
    .subtitle {
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 400;
        margin-top: 0.5rem;
        opacity: 0.8;
    }
    
    /* 分组标题样式 */
    h3 {
        color: #2d3748 !important;
        font-weight: 600 !important;
        font-size: 1.25rem !important;
        margin-bottom: 1rem !important;
        margin-top: 0 !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* 文本输入区域 */
    .stTextArea {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTextArea:hover {
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }
    
    .stTextArea > div > div > textarea {
        background: transparent !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 15px !important;
        color: #2d3748 !important;
        line-height: 1.6 !important;
        resize: vertical !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* 文件上传器样式 */
    .stFileUploader {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }
    
    .stFileUploader > div {
        background: #f8fafc !important;
        border: 2px dashed #cbd5e0 !important;
        border-radius: 12px !important;
        padding: 2rem 1rem !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
        min-height: 120px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #667eea !important;
        background: rgba(102, 126, 234, 0.05) !important;
    }
    
    /* 主要按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* 下载按钮样式 */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3) !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(72, 187, 120, 0.4) !important;
    }
    
    /* 次要按钮样式（重新生成、复制等） */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%) !important;
    }
    
    /* 加载动画 */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* 展开器样式 */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        color: #2d3748 !important;
        font-weight: 500 !important;
        padding: 1rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
        transform: translateY(-1px) !important;
    }
    
    /* 代码块样式 */
    .stCodeBlock {
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* 警告和错误消息 */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        margin: 1rem 0 !important;
    }
    
    /* 思维导图容器 */
    .markmap-container {
        background: white !important;
        border-radius: 16px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1) !important;
        margin: 2rem 0 !important;
        overflow: hidden !important;
    }
    
    /* 分隔线样式 */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent) !important;
        margin: 2rem 0 !important;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 2rem 1.5rem;
            margin: 1rem;
        }
        
        h1 {
            font-size: 2.25rem !important;
        }
        
        .stTextArea, .stFileUploader {
            padding: 1rem;
        }
        
        .stButton > button {
            padding: 0.875rem 1.5rem !important;
            font-size: 15px !important;
        }
    }
    
    @media (max-width: 480px) {
        h1 {
            font-size: 1.875rem !important;
        }
        
        .main .block-container {
            padding: 1.5rem 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 标题区域
st.markdown("""
<div class="title-section">
    <h1>🧠 文本转思维导图</h1>
    <div class="subtitle">使用 AI 智能分析，将复杂文本转化为结构化思维导图</div>
</div>
""", unsafe_allow_html=True)

# 使用列布局增强层次感
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    # 文本输入区域
    st.markdown("### 📝 文本输入")
    text_input = st.text_area(
        label="在此处粘贴文本",
        height=300,
        placeholder="请在此处粘贴或输入您要转换的文本内容...",
        label_visibility="collapsed"
    )

with col2:
    # 文件上传区域
    st.markdown("### 📁 文件上传")
    uploaded_file = st.file_uploader(
        label="支持 TXT, MD, DOCX, PDF, SRT 格式",
        type=['txt', 'md', 'docx', 'pdf', 'srt'],
        label_visibility="collapsed"
    )
    
    # 操作按钮区域
    st.markdown("<br>", unsafe_allow_html=True)
    generate_button = st.button(
        "🚀 生成思维导图",
        use_container_width=True
    )

def parse_srt_content(srt_string):
    """解析SRT字幕文件内容，提取纯文本"""
    try:
        subtitles = srt.parse(srt_string)
        text_content = []
        for subtitle in subtitles:
            text_content.append(subtitle.content)
        return '\n'.join(text_content)
    except Exception as e:
        st.error(f"解析SRT文件时出错：{str(e)}")
        return None

def extract_text_from_file(uploaded_file):
    """从上传的文件中提取文本内容"""
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_type in ['txt', 'md']:
            return uploaded_file.getvalue().decode("utf-8")
        
        elif file_type == 'srt':
            srt_text = uploaded_file.getvalue().decode("utf-8")
            return parse_srt_content(srt_text)
        
        elif file_type == 'docx':
            doc = Document(io.BytesIO(uploaded_file.getvalue()))
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return '\n'.join(text)
        
        elif file_type == 'pdf':
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
            text = []
            for page in pdf_reader.pages:
                text.append(page.extract_text())
            return '\n'.join(text)
        
        else:
            return None
            
    except Exception as e:
        st.error(f"读取文件时出错：{str(e)}")
        return None

if generate_button:
    # 整合输入逻辑：文件优先
    if uploaded_file is not None:
        final_text = extract_text_from_file(uploaded_file)
        if final_text is None:
            st.error("文件读取失败，请检查文件格式是否正确！")
            final_text = ""
    else:
        final_text = text_input
    
    if not final_text.strip():
        st.warning("请输入一些文本内容或上传文件！")
    else:
        with st.spinner('🧠 正在为您生成思维导图，请稍候...'):
            result_markdown = generate_mindmap_data(final_text)
            
            if result_markdown:
                markmap(result_markdown, height=500)
                
                # 操作按钮区域
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # 生成带时间戳的文件名
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"mindmap_{timestamp}.md"
                    
                    st.download_button(
                        label="💾 下载 MD",
                        data=result_markdown,
                        file_name=filename,
                        mime="text/markdown",
                        use_container_width=True
                    )
                
                with col2:
                    if st.button("🔄 重新生成", use_container_width=True):
                        st.rerun()
                
                with col3:
                    if st.button("📋 复制文本", use_container_width=True):
                        st.write("📎 请使用下方展开区域复制内容")
                
                # Markdown 源码区域
                st.markdown("---")
                with st.expander("📜 查看/复制 Markdown 源码", expanded=False):
                    st.code(result_markdown, language='markdown', line_numbers=True)
            else:
                st.error('抱歉，思维导图生成失败。可能是网络问题或API服务暂时不可用，请稍后再试。') 