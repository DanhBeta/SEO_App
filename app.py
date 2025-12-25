import streamlit as st
from openai import OpenAI
import requests

# Cấu hình trang
st.set_page_config(
    page_title="Ứng dụng Viết lại Bài viết SEO",
    page_icon="✍️",
    layout="wide"
)

# Sidebar cho API Key
with st.sidebar:
    st.header("⚙️ Cấu hình")
    api_key = st.text_input("OpenAI API Key", type="password", help="Nhập API key của bạn từ OpenAI")
    
    client = None
    if api_key:
        client = OpenAI(api_key=api_key)
    
    st.markdown("---")
    st.markdown("### 📝 Hướng dẫn")
    st.markdown("""
    1. Nhập OpenAI API Key ở trên
    2. Chọn nguồn dữ liệu (file hoặc URL)
    3. Nhập phong cách viết mong muốn
    4. Nhấn nút để viết lại bài viết
    """)

# Tiêu đề chính
st.title("✍️ Ứng dụng Viết lại Bài viết SEO")
st.markdown("Viết lại bài viết theo phong cách bạn yêu cầu với sức mạnh của AI")

# Kiểm tra API Key
if not api_key:
    st.warning("⚠️ Vui lòng nhập OpenAI API Key ở sidebar để sử dụng ứng dụng")
    st.stop()

# Chọn nguồn dữ liệu
st.header("📄 Nguồn dữ liệu")
source_type = st.radio(
    "Chọn nguồn:",
    ["📁 Tải file lên", "🔗 Nhập URL"],
    horizontal=True
)

content = None
file_name = None

if source_type == "📁 Tải file lên":
    uploaded_file = st.file_uploader(
        "Chọn file để tải lên",
        type=['txt', 'md', 'docx', 'pdf'],
        help="Hỗ trợ các định dạng: TXT, MD, DOCX, PDF"
    )
    
    if uploaded_file is not None:
        file_name = uploaded_file.name
        try:
            # Xử lý file text
            if file_name.endswith('.txt') or file_name.endswith('.md'):
                uploaded_file.seek(0)  # Reset file pointer
                content = str(uploaded_file.read(), "utf-8")
            
            # Xử lý file docx (cần thêm thư viện python-docx)
            elif file_name.endswith('.docx'):
                try:
                    import docx
                    uploaded_file.seek(0)  # Reset file pointer
                    doc = docx.Document(uploaded_file)
                    content = "\n".join([para.text for para in doc.paragraphs])
                except ImportError:
                    st.error("Cần cài đặt thư viện python-docx: pip install python-docx")
            
            # Xử lý file PDF (cần thêm thư viện PyPDF2)
            elif file_name.endswith('.pdf'):
                try:
                    import PyPDF2
                    uploaded_file.seek(0)  # Reset file pointer
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    content = "\n".join([page.extract_text() for page in pdf_reader.pages])
                except ImportError:
                    st.error("Cần cài đặt thư viện PyPDF2: pip install PyPDF2")
            
            if content:
                st.success(f"✅ Đã tải file: {file_name}")
                with st.expander("Xem nội dung gốc"):
                    st.text_area("Nội dung:", content, height=200, disabled=True)
        
        except Exception as e:
            st.error(f"Lỗi khi đọc file: {str(e)}")

else:  # URL
    url = st.text_input("Nhập URL bài viết:")
    
    if url:
        try:
            with st.spinner("Đang tải nội dung từ URL..."):
                response = requests.get(url, timeout=10, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                response.raise_for_status()
                
                # Sử dụng BeautifulSoup để lấy nội dung text (cần cài đặt)
                try:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Loại bỏ các thẻ script và style
                    for script in soup(["script", "style"]):
                        script.decompose()
                    content = soup.get_text()
                    # Làm sạch text
                    lines = (line.strip() for line in content.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    content = ' '.join(chunk for chunk in chunks if chunk)
                except ImportError:
                    # Nếu không có BeautifulSoup, lấy raw text
                    content = response.text[:5000]  # Giới hạn độ dài
                    st.warning("Cài đặt BeautifulSoup4 để xử lý HTML tốt hơn: pip install beautifulsoup4")
                
                st.success("✅ Đã tải nội dung từ URL thành công")
                with st.expander("Xem nội dung gốc"):
                    st.text_area("Nội dung:", content[:1000] + "..." if len(content) > 1000 else content, 
                               height=200, disabled=True)
        
        except Exception as e:
            st.error(f"Lỗi khi tải URL: {str(e)}")

# Nhập phong cách viết
st.header("🎨 Phong cách viết")
writing_style = st.text_area(
    "Mô tả phong cách viết mong muốn:",
    placeholder="Ví dụ: Viết lại theo phong cách SEO thân thiện, ngắn gọn, dễ hiểu, có nhiều từ khóa...",
    height=100,
    help="Mô tả chi tiết phong cách viết bạn muốn cho bài viết mới"
)

# Các tùy chọn bổ sung
with st.expander("⚙️ Tùy chọn nâng cao"):
    col1, col2 = st.columns(2)
    
    with col1:
        max_tokens = st.number_input("Số từ tối đa (tokens):", min_value=100, max_value=4000, value=2000)
        temperature = st.slider("Temperature (sáng tạo):", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    
    with col2:
        model = st.selectbox(
            "Chọn mô hình:",
            ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
            index=0
        )
        preserve_length = st.checkbox("Giữ nguyên độ dài tương đối", value=False)

# Nút xử lý
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    process_button = st.button("🚀 Viết lại bài viết", type="primary", use_container_width=True)

if process_button:
    if not api_key:
        st.error("❌ Vui lòng nhập OpenAI API Key ở sidebar")
    elif not content:
        st.error("❌ Vui lòng cung cấp nội dung từ file hoặc URL")
    elif not writing_style.strip():
        st.error("❌ Vui lòng nhập phong cách viết mong muốn")
    else:
        # Tạo client nếu chưa có
        if not client:
            client = OpenAI(api_key=api_key)
        
        with st.spinner("⏳ Đang xử lý và viết lại bài viết..."):
            try:
                # Tạo prompt cho OpenAI
                prompt = f"""Bạn là một chuyên gia viết bài SEO chuyên nghiệp. 

Nhiệm vụ: Viết lại bài viết sau đây theo phong cách: {writing_style}

Yêu cầu:
- Giữ nguyên thông tin chính và ý nghĩa của bài viết gốc
- Viết lại hoàn toàn theo phong cách được yêu cầu
- Đảm bảo bài viết tự nhiên, mạch lạc và hấp dẫn
- Tối ưu hóa cho SEO nếu phong cách yêu cầu

Bài viết gốc:
{content}

Hãy viết lại bài viết theo phong cách yêu cầu:"""

                # Gọi API OpenAI
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "Bạn là một chuyên gia viết bài SEO và copywriting chuyên nghiệp."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                rewritten_content = response.choices[0].message.content
                
                # Hiển thị kết quả
                st.header("✨ Kết quả bài viết đã viết lại")
                
                # Text area để xem và copy
                st.text_area(
                    "Nội dung bài viết mới:",
                    rewritten_content,
                    height=500,
                    key="rewritten_content"
                )
                
                # Nút download
                st.download_button(
                    label="📥 Tải xuống bài viết",
                    data=rewritten_content,
                    file_name=f"rewritten_{file_name if file_name else 'article'}.txt",
                    mime="text/plain"
                )
                
                # Thống kê
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Số từ gốc", len(content.split()))
                with col2:
                    st.metric("Số từ mới", len(rewritten_content.split()))
                with col3:
                    st.metric("Tokens sử dụng", response.usage.total_tokens)
                
                st.success("✅ Viết lại bài viết thành công!")
            
            except Exception as e:
                error_message = str(e)
                if "authentication" in error_message.lower() or "api key" in error_message.lower() or "invalid" in error_message.lower():
                    st.error("❌ API Key không hợp lệ. Vui lòng kiểm tra lại.")
                elif "rate limit" in error_message.lower():
                    st.error("❌ Đã vượt quá giới hạn API. Vui lòng thử lại sau.")
                else:
                    st.error(f"❌ Đã xảy ra lỗi: {error_message}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Ứng dụng Viết lại Bài viết SEO | Powered by OpenAI & Streamlit</div>",
    unsafe_allow_html=True
)

