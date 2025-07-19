import streamlit as st
from main import generate_mindmap_data
from streamlit_markmap import markmap

# 设置页面配置
st.set_page_config(page_title="文本转思维导图", page_icon="🧠")

# 显示主标题
st.title("文本转思维导图")

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
                
                with st.expander("查看/复制 Markdown 源码"):
                    st.code(result_markdown, language='markdown')
            else:
                st.error('抱歉，思维导图生成失败。可能是网络问题或API服务暂时不可用，请稍后再试。') 