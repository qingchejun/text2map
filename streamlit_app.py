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
    /* 强制设置页面主要元素的文字颜色为黑色 */
    html, body, [class*="st-"] {
       color: #000000;
    }
    h1 {
        color: #000000 !important;
    }
    /* 新增规则：隐藏Streamlit为标题自动生成的锚链接图标 */
    h1 a {
        display: none !important;
    }
    /* 将背景强制设置为白色 */
    body {
        background-color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 显示主标题
st.markdown("<h1>文本转思维导图</h1>", unsafe_allow_html=True)

# 创建文本输入框
text_input = st.text_area(
    label="在此处粘贴文本：",
    height=300,
    placeholder="请在此处粘贴或输入您要转换的文本内容..."
)

# 创建文件上传组件
uploaded_file = st.file_uploader(
    label="或者，直接上传文档文件：",
    type=['txt', 'md', 'docx', 'pdf', 'srt']
)

# 创建生成按钮
generate_button = st.button("生成思维导图")

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
                
                # 生成带时间戳的文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"mindmap_{timestamp}.md"
                
                st.download_button(
                    label="下载为 Markdown 文件 (.md)",
                    data=result_markdown,
                    file_name=filename,
                    mime="text/markdown",
                )
                
                with st.expander("查看/复制 Markdown 源码"):
                    st.code(result_markdown, language='markdown')
            else:
                st.error('抱歉，思维导图生成失败。可能是网络问题或API服务暂时不可用，请稍后再试。') 