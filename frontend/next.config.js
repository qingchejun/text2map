/** @type {import('next').NextConfig} */
const nextConfig = {
    // App Router 配置
    experimental: {
      appDir: true,
    },
    
    // 生产环境优化
    compress: true,
    poweredByHeader: false,
    
    // 确保静态资源正确处理
    assetPrefix: '',
    basePath: '',
    trailingSlash: false,
    
    // 图片优化
    images: {
      unoptimized: true, // Render 免费版建议设置
    },
  }
  
  module.exports = nextConfig