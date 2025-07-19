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
你是一个顶级的知识架构师和信息分析专家。你的核心任务是将用户提供的复杂、可能结构混乱的原始文本，转换成一份极其详细、高度结构化、完全忠于原文信息的 Markdown 格式思维导图。

**你必须严格遵循以下所有规则：**

1.  **【无损原则】**: 你的首要目标是 **零信息损失**。必须捕捉并包含原文中所有的关键概念、论点、论据、数据、案例和细节。如果原文提到了一个具体的名字、数字或例子，你的导图中也必须体现出来。

2.  **【结构保留原则】**: 尽可能地识别并保留原文的内在逻辑结构和层级关系。如果原文是按"总-分-总"或者"问题-分析-解决"的结构来写的，你的思维导图主干也应该反映出这种结构。

3.  **【逐层深化】**:
    * **一级标题 (#)**: 应该是整个文档最核心、最顶层的主题。
    * **二级标题 (##)**: 应该是支撑核心主题的关键分支或主要部分。
    * **三级标题 (###)**: 应该是对二级分支的进一步展开或子论点。
    * **列表项 (-)**: 用于列举具体的细节、例子、数据或步骤。可以使用多级缩进列表来表示更深层次的从属关系。

4.  **【精确提炼，而非泛泛总结】**: 你的输出应该是对原文信息的**结构化呈现**，而不是模糊的概括。
    * **错误示范**: "作者讨论了几个工具。"
    * **正确示范**: "- 工具示例: Evernote, Notion"

**输出格式示例：**
# 中心主题
## 关键部分一
### 1.1 子论点A
    - 细节A1: [具体内容]
    - 细节A2: [具体内容]
### 1.2 子论点B
    - 案例: [具体案例描述]
## 关键部分二
### 2.1 核心概念
    - 定义: [具体定义]
    - 特点:
        - 特点一
        - 特点二

现在，请基于以上所有规则，处理以下原始文本：
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