import cv2
import numpy as np
import os

# Đọc kích thước ảnh
image_path = 'vn.jpg'
image = cv2.imread(image_path)
height, width = image.shape[:2]

# Tạo thư mục lưu trữ tọa độ
base_output_folder = 'coordinates_output'

# Hàm vẽ các đường biên từ tọa độ
def draw_contours_from_file(file_folder, image_shape):
    canvas = np.ones(image_shape, dtype=np.uint8) * 255  # Nền trắng
    for filename in os.listdir(file_folder):
        if filename.endswith('.txt'):
            contours = np.loadtxt(os.path.join(file_folder, filename), dtype=int)
            if contours.ndim == 2 and contours.size > 0:
                cv2.polylines(canvas, [contours], isClosed=False, color=0, thickness=1)
    return canvas

# Hàm vẽ lại và hiển thị các đường biên từ tọa độ
def draw_and_show_edges():
    methods = [
        'canny_edges', 'sobel_edges', 'laplacian_edges',
        'prewitt_edges', 'scharr_edges', 'roberts_cross_edges',
        'kirsch_edges', 'gabor_edges', 'log_edges', 'marr_hildreth_edges', 'dog_edges'
    ]
    
    for method in methods:
        folder = os.path.join(base_output_folder, method)
        canvas = draw_contours_from_file(folder, (height, width))
        cv2.imshow(f'{method} on White Background', canvas)
        
    cv2.waitKey(0)
draw_and_show_edges()
