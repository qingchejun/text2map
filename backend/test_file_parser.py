"""
文件解析器测试脚本
用于验证各种文件格式的解析功能
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.file_parser import parse_file_content, get_supported_formats


def test_supported_formats():
    """测试支持的文件格式列表"""
    print("=== 测试支持的文件格式 ===")
    formats = get_supported_formats()
    print(f"支持的文件格式: {formats}")
    print()


def test_txt_parsing():
    """测试TXT文件解析"""
    print("=== 测试TXT文件解析 ===")
    
    # 创建测试TXT文件
    test_content = """这是一个测试TXT文件。
包含多行文本内容。
用于测试文件解析功能。
"""
    
    test_file_path = "test.txt"
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    try:
        with open(test_file_path, "rb") as f:
            file_bytes = f.read()
        
        result = parse_file_content("test.txt", file_bytes)
        print(f"解析结果: {result}")
        print("✅ TXT文件解析测试通过")
    except Exception as e:
        print(f"❌ TXT文件解析测试失败: {e}")
    finally:
        # 清理测试文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
    print()


def test_md_parsing():
    """测试Markdown文件解析"""
    print("=== 测试Markdown文件解析 ===")
    
    # 创建测试MD文件
    test_content = """# 测试标题

这是一个测试Markdown文件。

## 二级标题

- 列表项1
- 列表项2

### 三级标题

**粗体文本** 和 *斜体文本*。
"""
    
    test_file_path = "test.md"
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    try:
        with open(test_file_path, "rb") as f:
            file_bytes = f.read()
        
        result = parse_file_content("test.md", file_bytes)
        print(f"解析结果: {result}")
        print("✅ Markdown文件解析测试通过")
    except Exception as e:
        print(f"❌ Markdown文件解析测试失败: {e}")
    finally:
        # 清理测试文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
    print()


def test_srt_parsing():
    """测试SRT文件解析"""
    print("=== 测试SRT文件解析 ===")
    
    # 创建测试SRT文件
    test_content = """1
00:00:01,000 --> 00:00:04,000
这是第一行字幕内容

2
00:00:05,000 --> 00:00:08,000
这是第二行字幕内容

3
00:00:09,000 --> 00:00:12,000
这是第三行字幕内容
"""
    
    test_file_path = "test.srt"
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    try:
        with open(test_file_path, "rb") as f:
            file_bytes = f.read()
        
        result = parse_file_content("test.srt", file_bytes)
        print(f"解析结果: {result}")
        print("✅ SRT文件解析测试通过")
    except Exception as e:
        print(f"❌ SRT文件解析测试失败: {e}")
    finally:
        # 清理测试文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
    print()


def test_unsupported_format():
    """测试不支持的文件格式"""
    print("=== 测试不支持的文件格式 ===")
    
    test_content = b"This is a test file"
    
    try:
        result = parse_file_content("test.xyz", test_content)
        print(f"❌ 应该抛出异常，但得到了结果: {result}")
    except ValueError as e:
        print(f"✅ 正确抛出异常: {e}")
    except Exception as e:
        print(f"❌ 抛出了意外的异常: {e}")
    print()


def main():
    """运行所有测试"""
    print("开始文件解析器测试...\n")
    
    test_supported_formats()
    test_txt_parsing()
    test_md_parsing()
    test_srt_parsing()
    test_unsupported_format()
    
    print("所有测试完成！")


if __name__ == "__main__":
    main() 