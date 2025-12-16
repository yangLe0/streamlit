from typing import List
import os
import pdfplumber
import pytesseract

def split_into_chunks(doc_file: str, max_pages: int = None, language: str = 'chi_sim') -> List[str]:
    """使用OCR技术提取PDF文本，优化中文识别"""
    if not os.path.exists(doc_file):
        raise FileNotFoundError(f"文件 {doc_file} 不存在")
    
    with pdfplumber.open(doc_file) as pdf:
        content = ""
        pages_to_process = pdf.pages[:max_pages] if max_pages else pdf.pages
        total_pages = len(pages_to_process)
        
        for page_num, page in enumerate(pages_to_process, 1):
            print(f"正在处理第 {page_num}/{total_pages} 页...")
            
            # 提高分辨率以获得更好的识别效果
            image = page.to_image(resolution=400)
            
            # OCR配置：使用所有可用引擎模式和自动页面分割
            custom_config = r'--oem 3 --psm 3'
            
            # 使用OCR提取文本
            page_text = pytesseract.image_to_string(image.original, 
                                                  lang=language,
                                                  config=custom_config)
            
            if page_text.strip():
                content += page_text + "\n"
                print(f"第 {page_num} 页提取完成")
            else:
                print(f"第 {page_num} 页未提取到文本")
    
    # 分割段落并过滤空段落
    chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
    return chunks

# 示例：处理前5页
if __name__ == "__main__":
    try:
        print("开始提取PDF文本...")
        chunks = split_into_chunks("doc.pdf", max_pages=5)
        print(f"\n✅ 提取完成！共提取 {len(chunks)} 个段落")
        
        # 显示前5个段落
        print("\n📄 提取的内容预览：")
        for i, chunk in enumerate(chunks[:5]):
            print(f"\n[{i+1}] {chunk}")
              
    except Exception as e:
        print(f"❌ 处理出错: {e}")

# 进一步优化建议：
# 1. 如果PDF质量较差，可以尝试调整图像预处理（如二值化、去噪）
# 2. 对于特定字体或排版，可以调整--psm参数（0-13）
# 3. 对于混合语言文档，可以使用lang='chi_sim+eng'
# 4. 考虑使用更专业的OCR服务（如百度AI、阿里云OCR）获取更好的识别效果