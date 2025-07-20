"""
API数据模型
定义请求和响应的数据结构
"""

from pydantic import BaseModel
from typing import List


class TextInput(BaseModel):
    """文本输入模型"""
    text: str


class MindmapResponse(BaseModel):
    """思维导图响应模型"""
    mindmap_data: str


class FileUploadResponse(BaseModel):
    """文件上传响应模型"""
    mindmap_data: str
    extracted_text: str
    filename: str
    file_size: int


class SupportedFormatsResponse(BaseModel):
    """支持的文件格式响应模型"""
    formats: List[str]
    max_file_size_mb: int


class ErrorResponse(BaseModel):
    """错误响应模型"""
    detail: str
    error_type: str = "validation_error" 