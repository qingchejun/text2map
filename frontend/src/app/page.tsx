'use client';

import { useState, useEffect, useRef } from 'react';
import { Transformer } from 'markmap-lib';
import { Markmap } from 'markmap-view';
import type { Markmap as MarkmapInstance } from 'markmap-view';
import { Sun, Moon } from 'lucide-react';

export default function HomePage() {
  // --- 状态管理 ---
  const [inputText, setInputText] = useState('');
  const [mindmapData, setMindmapData] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [theme, setTheme] = useState('light');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  // --- 用于渲染Markmap的引用 ---
  const svgRef = useRef<SVGSVGElement>(null);
  const mmRef = useRef<MarkmapInstance | null>(null);
  
  // 清理Markmap实例
  const cleanupMarkmap = () => {
    if (mmRef.current) {
      try {
        mmRef.current.destroy();
      } catch (error) {
        console.warn('清理Markmap实例时出错:', error);
      }
      mmRef.current = null;
    }
  };

  // --- 主题管理 Effect (只管理页面，不管理思维导图) ---
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (savedTheme) {
      setTheme(savedTheme);
    } else if (prefersDark) {
      setTheme('dark');
    }
  }, []);

  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  // --- 处理文件选择 ---
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] || null;
    setSelectedFile(file);
    setError(''); // 清除之前的错误
  };

  // --- 处理按钮点击的函数 ---
  const handleGenerateClick = async () => {
    setIsLoading(true);
    setMindmapData('');
    setError('');
    
    try {
      let response;
      
      if (selectedFile) {
        // 如果有选择文件，使用文件上传API
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        response = await fetch('http://localhost:8000/generate-from-file', {
          method: 'POST',
          body: formData, // 不需要手动设置Content-Type，浏览器会自动处理
        });
      } else {
        // 如果没有选择文件，使用文本输入API
        if (!inputText.trim()) {
          throw new Error('请输入文本内容或选择文件');
        }
        
        response = await fetch('http://localhost:8000/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: inputText }),
        });
      }
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setMindmapData(data.mindmap_data);
    } catch (e: any) {
      setError(`请求失败: ${e.message}`);
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };
  
  // --- 渲染思维导图 Effect (恢复到最简单的版本) ---
  useEffect(() => {
    if (!mindmapData || !svgRef.current) return;

    // 使用setTimeout确保DOM完全准备好
    const timer = setTimeout(() => {
      try {
        const transformer = new Transformer();
        const { root } = transformer.transform(mindmapData);
        
        // 清空画布
        svgRef.current!.innerHTML = '';
        
        // 确保SVG有正确的尺寸
        svgRef.current!.setAttribute('width', '100%');
        svgRef.current!.setAttribute('height', '500px');
        svgRef.current!.style.width = '100%';
        svgRef.current!.style.height = '500px';
        
        // 清理之前的实例
        cleanupMarkmap();
        
        // 使用默认选项创建思维导图，添加错误处理
        mmRef.current = Markmap.create(svgRef.current!, { 
          autoFit: true,
          duration: 500,
          nodeMinHeight: 16,
          spacingVertical: 5,
          spacingHorizontal: 80,
          paddingX: 8
        }, root);
      } catch (error) {
        console.error('Markmap渲染错误:', error);
        setError('思维导图渲染失败，请重试');
      }
    }, 100); // 延迟100ms确保DOM完全准备好

    return () => {
      clearTimeout(timer);
      cleanupMarkmap();
    };
  }, [mindmapData]); // <-- 关键：只在数据变化时重绘，不再监听主题

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-100 dark:bg-gray-900 p-4 sm:p-8 transition-colors duration-300">
      <div className={`w-full max-w-2xl backdrop-blur-xl rounded-2xl shadow-2xl p-6 sm:p-8 space-y-6 relative transition-colors duration-300 ${
        theme === 'dark' 
          ? 'bg-gray-800/80 text-white' 
          : 'bg-white/80 text-gray-900'
      }`}>
        
        <button
          onClick={toggleTheme}
          className={`absolute top-4 right-4 p-2 rounded-full transition-colors ${
            theme === 'dark'
              ? 'text-gray-300 hover:bg-gray-700'
              : 'text-gray-600 hover:bg-gray-200'
          }`}
          aria-label="Toggle theme"
        >
          {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
        </button>

        <h1 className={`text-3xl sm:text-4xl font-bold text-center ${
          theme === 'dark' ? 'text-white' : 'text-gray-800'
        }`}>
          文本转思维导图
        </h1>
        <p className={`text-center text-sm mb-4 ${
          theme === 'dark' ? 'text-gray-300' : 'text-gray-600'
        }`}>
          当前主题: {theme}
        </p>

        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          className={`w-full h-48 p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none transition-colors duration-200 ${
            theme === 'dark'
              ? 'bg-gray-700 border-gray-600 text-gray-100 placeholder-gray-400'
              : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500'
          }`}
          placeholder="请在此处粘贴或输入您要转换的文本内容..."
        />

        {/* 文件上传区域 */}
        <div className="space-y-2">
          <h3 className={`text-lg font-semibold ${
            theme === 'dark' ? 'text-white' : 'text-gray-800'
          }`}>
            或者... 上传文件
          </h3>
          <div className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors duration-200 ${
            selectedFile 
              ? (theme === 'dark' ? 'border-green-500 bg-green-900/20' : 'border-green-500 bg-green-50')
              : (theme === 'dark' ? 'border-gray-600 hover:border-gray-500' : 'border-gray-300 hover:border-gray-400')
          }`}>
            <input
              type="file"
              onChange={handleFileChange}
              accept=".txt,.md,.docx,.pdf,.srt"
              className="hidden"
              id="file-upload"
            />
            <label
              htmlFor="file-upload"
              className={`cursor-pointer block ${
                theme === 'dark' ? 'text-gray-300 hover:text-white' : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              {selectedFile ? (
                <div>
                  <p className="text-green-500 font-medium">✓ 已选择文件</p>
                  <p className={`text-sm mt-1 ${
                    theme === 'dark' ? 'text-gray-400' : 'text-gray-500'
                  }`}>
                    {selectedFile.name} ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
                  </p>
                </div>
              ) : (
                <div>
                  <p className="text-lg font-medium">点击选择文件</p>
                  <p className={`text-sm mt-1 ${
                    theme === 'dark' ? 'text-gray-400' : 'text-gray-500'
                  }`}>
                    支持格式: TXT, MD, DOCX, PDF, SRT (最大50MB)
                  </p>
                </div>
              )}
            </label>
          </div>
          {selectedFile && (
            <button
              onClick={() => {
                setSelectedFile(null);
                const fileInput = document.getElementById('file-upload') as HTMLInputElement;
                if (fileInput) fileInput.value = '';
              }}
              className={`text-sm ${
                theme === 'dark' ? 'text-red-400 hover:text-red-300' : 'text-red-600 hover:text-red-700'
              }`}
            >
              清除文件选择
            </button>
          )}
        </div>

        <button
          onClick={handleGenerateClick}
          disabled={isLoading || (!inputText.trim() && !selectedFile)}
          className={`w-full font-semibold py-3 px-6 rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 transition-all duration-200 ease-in-out hover:scale-105 disabled:cursor-not-allowed disabled:hover:scale-100 ${
            theme === 'dark'
              ? 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-400 disabled:bg-gray-600'
              : 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500 disabled:bg-gray-400'
          }`}
        >
          {isLoading ? '正在生成中...' : '生成思维导图'}
        </button>

        <div className="mt-6 w-full">
          {isLoading && <p className={`text-center ${
            theme === 'dark' ? 'text-gray-300' : 'text-gray-600'
          }`}>🧠 AI 正在思考，请稍候...</p>}
          {error && <p className={`text-center p-3 rounded-lg ${
            theme === 'dark' 
              ? 'text-red-400 bg-red-900/20' 
              : 'text-red-500 bg-red-100'
          }`}>{error}</p>}
          
          <div className={`transition-opacity duration-500 ${mindmapData ? 'opacity-100' : 'opacity-0 h-0'}`}>
            <svg 
              ref={svgRef} 
              className="w-full h-[500px] border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800"
              style={{ minHeight: '500px', width: '100%' }}
            />
          </div>
        </div>
      </div>
    </main>
  );
}
