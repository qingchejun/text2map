/** @type {import('next').NextConfig} */
const nextConfig = {
    // 暂时禁用字体优化避免错误
    optimizeFonts: false,
    
    // 基础配置
    compress: true,
    poweredByHeader: false,
    
    // 图片优化
    images: {
      unoptimized: true,
    },
    
    // 试验性功能
    experimental: {
      optimizePackageImports: ['lucide-react']
    },
  }
  
  module.exports = nextConfig