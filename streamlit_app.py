import streamlit as st
from main import generate_mindmap_data
from streamlit_markmap import markmap
from datetime import datetime

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

# 创建生成按钮
generate_button = st.button("生成思维导图")

if generate_button:
    if not text_input.strip():
        st.warning("请输入一些文本内容！")
    else:
        with st.spinner('🧠 正在为您生成思维导图，请稍候...'):
            result_markdown = generate_mindmap_data(text_input)
            
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