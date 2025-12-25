# Ứng dụng Viết lại Bài viết SEO

Ứng dụng web sử dụng Streamlit và OpenAI để viết lại bài viết theo phong cách được yêu cầu.

## Tính năng

- ✅ Tải file lên (TXT, MD, DOCX, PDF)
- ✅ Nhập URL để lấy nội dung
- ✅ Tùy chỉnh phong cách viết
- ✅ Sử dụng OpenAI GPT để viết lại bài viết
- ✅ Tải xuống kết quả

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

2. Chạy ứng dụng:
```bash
streamlit run app.py
```

## Sử dụng

1. Mở ứng dụng trong trình duyệt
2. Nhập OpenAI API Key ở sidebar
3. Chọn nguồn dữ liệu (file hoặc URL)
4. Nhập phong cách viết mong muốn
5. Nhấn nút "Viết lại bài viết"
6. Xem kết quả và tải xuống nếu cần

## Lưu ý

- Cần có OpenAI API Key để sử dụng
- API Key được lưu trong session và không được lưu lại
- Một số file format yêu cầu thư viện bổ sung (đã có trong requirements.txt)

