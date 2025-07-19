import os
from dotenv import load_dotenv
import google.generativeai as genai

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量获取API密钥并配置
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def read_text_file(filepath):
    """读取文本文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print("错误：输入文件未找到！")
        return None
    except Exception as e:
        print(f"读取文件时出错: {str(e)}")
        return None

def generate_mindmap_data(content):
    """生成思维导图数据"""
    # 定义提示词模板
    PROMPT_TEMPLATE = """
你是一个世界级的知识管理专家，擅长将复杂冗长的文本（如播客文稿、会议记录、文章）进行提炼、总结，并转换成层级清晰、逻辑严谨的 Markdown 格式的思维导图。

你的任务是处理用户提供的文本，并遵循以下所有要求：
1.  **核心目标**：以思维导图的形式，尽量详细地包含原文的所有关键知识点、论点和论据，确保不损失关键信息。
2.  **输出格式**：必须严格使用 Markdown 的标题层级（#, ##, ###, ...）和列表（-, *, +）来表示思维导图的父子关系。
3.  **逻辑结构**：导图必须有一个中心主题（一级标题），并围绕该主题分出几个关键分支（二级标题）。每个分支下可以有更详细的子分支（三级标题或列表项）。
4.  **语言风格**：保持简洁、精炼、中立、客观。

现在，请处理以下文本：
"""
    
    try:
        # 拼接完整的提示词
        final_prompt = PROMPT_TEMPLATE + content
        
        print("正在调用 Gemini API，请稍候...")
        
        # 初始化模型
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # 调用 API 并获取响应
        response = model.generate_content(final_prompt)
        
        # 返回文本结果
        return response.text
        
    except Exception as e:
        print(f"调用 API 时发生错误: {e}")
        return None

def save_text_to_file(filepath, content):
    """保存文本到文件"""
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"文件已成功保存到: {filepath}")
    except Exception as e:
        print(f"保存文件时出错: {str(e)}")

if __name__ == '__main__':
    # 主程序入口
    # 定义输入和输出文件名
    INPUT_FILENAME = 'input.txt'
    OUTPUT_FILENAME = 'output.md'
    
    # 读取输入文件
    content = read_text_file(INPUT_FILENAME)
    
    # 判断是否成功读取到内容
    if content is not None:
        # 生成思维导图数据
        mindmap_data = generate_mindmap_data(content)
        
        # 判断是否成功生成思维导图数据
        if mindmap_data is not None:
            # 保存思维导图到输出文件
            save_text_to_file(OUTPUT_FILENAME, mindmap_data)
            print("处理完成！思维导图已成功保存至 output.md") 