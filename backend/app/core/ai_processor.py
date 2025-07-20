"""
AI处理模块
负责调用Google Gemini API生成思维导图
"""

import os
import logging
from typing import Optional
import google.generativeai as genai

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_gemini():
    """初始化Gemini API配置"""
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("未找到 GOOGLE_API_KEY 环境变量")
        
        genai.configure(api_key=api_key)
        logger.info("Gemini API 配置成功")
        return True
    except Exception as e:
        logger.error(f"Gemini API 配置失败: {e}")
        return False


def generate_mindmap_data(text_content: str) -> Optional[str]:
    """
    调用 Google Gemini API 来处理文本并生成思维导图Markdown。
    
    Args:
        text_content: 输入的文本内容
        
    Returns:
        生成的思维导图Markdown字符串，失败时返回None
    """
    PROMPT_TEMPLATE = """
    你是一个顶级的知识架构师和信息分析专家。你的核心任务是将用户提供的复杂、可能结构混乱的原始文本，转换成一份极其详细、高度结构化、完全忠于原文信息的 Markdown 格式思维导图。

    **你必须严格遵循以下所有规则：**

    1.  **【无损原则】**: 你的首要目标是 **零信息损失**。必须捕捉并包含原文中所有的关键概念、论点、论据、数据、案例和细节。如果原文提到了一个具体的名字、数字或例子，你的导图中也必须体现出来。

    2.  **【结构保留原则】**: 尽可能地识别并保留原文的内在逻辑结构和层级关系。如果原文是按"总-分-总"或者"问题-分析-解决"的结构来写的，你的思维导图主干也应该反映出这种结构。

    3.  **【逐层深化】**:
        * 一级标题 (#): 应该是整个文档最核心、最顶层的主题。
        * 二级标题 (##): 应该是支撑核心主题的关键分支或主要部分。
        * 三级标题 (###): 应该是对二级分支的进一步展开或子论点。
        * 列表项 (-): 用于列举具体的细节、例子、数据或步骤。可以使用多级缩进列表来表示更深层次的从属关系。

    4.  **【精确提炼，而非泛泛总结】**: 你的输出应该是对原文信息的**结构化呈现**，而不是模糊的概括。
        * **错误示范**: "作者讨论了几个工具。"
        * **正确示范**: "- 工具示例: Evernote, Notion"

    现在，请基于以上所有规则，处理以下原始文本：
    """
    
    try:
        # 检查API密钥
        if not os.environ.get('GOOGLE_API_KEY'):
            logger.error("GOOGLE_API_KEY 未设置")
            return None
        
        logger.info("正在初始化 Gemini 模型...")
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        logger.info("模型初始化成功")
        
        logger.info("正在调用 Gemini API...")
        full_prompt = PROMPT_TEMPLATE + text_content
        logger.info(f"输入文本长度: {len(text_content)} 字符")
        
        response = model.generate_content(full_prompt)
        logger.info("成功获取API响应")
        logger.info(f"响应长度: {len(response.text)} 字符")
        
        return response.text
        
    except Exception as e:
        logger.error(f"调用 Gemini API 时发生错误: {e}")
        logger.error(f"错误类型: {type(e).__name__}")
        import traceback
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        return None 