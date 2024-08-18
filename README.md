# Dự Án Xử Lý Ảnh và Vẽ Đường Biên

## Giới thiệu

Dự án này bao gồm hai tập tin Python:
1. **`convert_img_to_txt.py`**: Chuyển đổi ảnh thành các tọa độ đường biên và lưu chúng vào các file văn bản.
2. **`paint.py`**: Vẽ các đường biên từ các file văn bản đã lưu lên các cửa sổ Turtle.

## Cài Đặt Môi Trường

### 1. Cài Đặt Python
Để chạy các tập tin Python trong dự án này, trước tiên bạn cần cài đặt Python trên máy tính của mình:

1. **Tải Python:**
   - Truy cập [python.org/downloads](https://www.python.org/downloads/) và tải phiên bản mới nhất.

2. **Cài Đặt Python:**
   - Trong quá trình cài đặt, đảm bảo rằng bạn đã chọn tùy chọn "Add Python to PATH".
   - Hoàn thành quá trình cài đặt.

3. **Kiểm Tra Cài Đặt:**
   - Mở Command Prompt (CMD) và nhập:
     ```bash
     python --version
     ```
   - Nếu lệnh trên trả về phiên bản Python, bạn đã cài đặt thành công.

### 2. Cài Đặt Các Thư Viện Cần Thiết

Dự án này sử dụng các thư viện sau:

- **OpenCV**: Thư viện xử lý ảnh.
- **Pillow**: Thư viện xử lý ảnh, dùng để lấy kích thước của ảnh.
- **Turtle**: Thư viện đồ họa có sẵn trong Python để vẽ đường biên.
- **Pygame**: Ở đầy dùng để phát mp3.

Để cài đặt các thư viện này, hãy mở Command Prompt và chạy các lệnh sau:

**Cài Đặt:**
   ```bash
   pip install opencv-python
   pip install pillow
   pip install PythonTurtle
   pip install pygame
