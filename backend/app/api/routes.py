"""
API路由模块
定义所有的API端点
"""

import logging
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List

from ..models.schemas import (
    TextInput, 
    MindmapResponse, 
    FileUploadResponse, 
    SupportedFormatsResponse,
    ErrorResponse
)
from ..core.ai_processor import generate_mindmap_data
from ..core.file_parser import parse_file_content, get_supported_formats

# 配置日志
logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter()


@router.get("/", summary="服务根路径，用于健康检查")
def read_root():
    """检查API服务是否正在运行"""
    return {"message": "Text2Map Backend is running!", "status": "healthy"}


@router.post("/generate", response_model=MindmapResponse, summary="从文本生成思维导图")
def create_mindmap_from_text(text_input: TextInput):
    """
    接收用户提交的文本，调用AI模型生成思维导图，并返回Markdown格式的结果。
    
    Args:
        text_input: 包含文本内容的数据模型
        
    Returns:
        生成的思维导图Markdown数据
        
    Raises:
        HTTPException: 当输入为空或AI处理失败时
    """
    try:
        # 验证输入
        if not text_input.text or text_input.text.isspace():
            raise HTTPException(
                status_code=400, 
                detail="输入的文本不能为空"
            )
        
        # 检查文本长度
        if len(text_input.text) > 50000:  # 限制为50KB
            raise HTTPException(
                status_code=400,
                detail="文本长度超过50KB限制"
            )
        
        logger.info(f"开始处理文本输入，长度: {len(text_input.text)} 字符")
        
        # 调用AI处理
        result = generate_mindmap_data(text_input.text)
        
        if result is None:
            raise HTTPException(
                status_code=500, 
                detail="AI服务处理失败，请稍后再试"
            )
        
        logger.info("文本处理完成，成功生成思维导图")
        return MindmapResponse(mindmap_data=result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"处理文本输入时发生未知错误: {e}")
        raise HTTPException(
            status_code=500,
            detail="服务器内部错误，请稍后再试"
        )


@router.post("/generate-from-file", response_model=FileUploadResponse, summary="从文件生成思维导图")
def create_mindmap_from_file(file: UploadFile = File(...)):
    """
    接收上传的文件，解析文件内容，调用AI模型生成思维导图。
    
    Args:
        file: 上传的文件对象
        
    Returns:
        包含思维导图数据、提取的文本、文件名和文件大小的响应
        
    Raises:
        HTTPException: 当文件格式不支持、解析失败或AI处理失败时
    """
    try:
        # 验证文件
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="文件名不能为空"
            )
        
        logger.info(f"开始处理文件: {file.filename}")
        
        # 读取文件内容
        file_content = file.file.read()
        file_size = len(file_content)
        
        logger.info(f"文件大小: {file_size} 字节")
        
        # 解析文件内容
        try:
            extracted_text = parse_file_content(file.filename, file_content)
            logger.info(f"文件解析成功，提取文本长度: {len(extracted_text)} 字符")
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"文件解析失败: {e}")
            raise HTTPException(
                status_code=500,
                detail="文件解析失败，请检查文件格式是否正确"
            )
        
        # 验证提取的文本
        if not extracted_text or extracted_text.isspace():
            raise HTTPException(
                status_code=400,
                detail="文件内容为空或无法提取有效文本"
            )
        
        # 调用AI处理
        result = generate_mindmap_data(extracted_text)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail="AI服务处理失败，请稍后再试"
            )
        
        logger.info("文件处理完成，成功生成思维导图")
        
        return FileUploadResponse(
            mindmap_data=result,
            extracted_text=extracted_text,
            filename=file.filename,
            file_size=file_size
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"处理文件上传时发生未知错误: {e}")
        raise HTTPException(
            status_code=500,
            detail="服务器内部错误，请稍后再试"
        )


@router.get("/supported-formats", response_model=SupportedFormatsResponse, summary="获取支持的文件格式")
def get_supported_file_formats():
    """
    获取当前系统支持的文件格式列表
    
    Returns:
        支持的文件格式列表和最大文件大小限制
    """
    try:
        formats = get_supported_formats()
        return SupportedFormatsResponse(
            formats=formats,
            max_file_size_mb=50
        )
    except Exception as e:
        logger.error(f"获取支持格式时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail="获取支持格式失败"
        ) 