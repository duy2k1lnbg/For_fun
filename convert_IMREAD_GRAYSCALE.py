import cv2
import numpy as np
import os
import shutil

# Đường dẫn đến các thư mục cần xóa
base_output_folder = 'coordinates_output'
images_output_folder = 'images_output'

# Xóa các thư mục nếu chúng tồn tại
if os.path.exists(base_output_folder):
    shutil.rmtree(base_output_folder)
if os.path.exists(images_output_folder):
    shutil.rmtree(images_output_folder)

# Đọc ảnh ở chế độ grayscale
image = cv2.imread('vn.jpg', cv2.IMREAD_GRAYSCALE)

# # Chuyển ảnh sang nhị phân
# _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

# Áp dụng Otsu's Binarization để tự động tìm ngưỡng và chuyển đổi thành ảnh nhị phân
_, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print(f'Threshold value: {_}')

# Đảm bảo ảnh nhị phân là float64 cho các phép toán
binary_float = np.float64(binary_image)

# Bộ lọc Sobel
sobel_x = cv2.Sobel(binary_float, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(binary_float, cv2.CV_64F, 0, 1, ksize=3)
sobel_edges = cv2.magnitude(sobel_x, sobel_y)

# Bộ lọc Laplacian
laplacian_edges = cv2.Laplacian(binary_float, cv2.CV_64F)

# Bộ lọc Prewitt
prewitt_kx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float64)
prewitt_ky = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float64)
prewitt_x = cv2.filter2D(binary_float, -1, prewitt_kx)
prewitt_y = cv2.filter2D(binary_float, -1, prewitt_ky)
prewitt_edges = cv2.magnitude(prewitt_x, prewitt_y)

# Bộ lọc Scharr
scharr_x = cv2.Scharr(binary_float, cv2.CV_64F, 1, 0)
scharr_y = cv2.Scharr(binary_float, cv2.CV_64F, 0, 1)
scharr_edges = cv2.magnitude(scharr_x, scharr_y)

# Bộ lọc Roberts Cross
roberts_cross_kx = np.array([[1, 0], [0, -1]], dtype=np.float64)
roberts_cross_ky = np.array([[0, 1], [-1, 0]], dtype=np.float64)
roberts_cross_x = cv2.filter2D(binary_float, -1, roberts_cross_kx)
roberts_cross_y = cv2.filter2D(binary_float, -1, roberts_cross_ky)
roberts_cross_edges = cv2.magnitude(roberts_cross_x, roberts_cross_y)

# Bộ lọc Kirsch Compass Kernel
kirsch_kernels = {
    'N': np.array([[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]], dtype=np.float64),
    'NE': np.array([[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]], dtype=np.float64),
    'E': np.array([[5, 5, 5], [-3, 0, -3], [-3, -3, -3]], dtype=np.float64),
    'SE': np.array([[5, 5, -3], [5, 0, -3], [-3, -3, -3]], dtype=np.float64),
    'S': np.array([[5, -3, -3], [5, 0, -3], [5, -3, -3]], dtype=np.float64),
    'SW': np.array([[-3, -3, -3], [5, 0, -3], [5, 5, -3]], dtype=np.float64),
    'W': np.array([[-3, -3, -3], [-3, 0, -3], [5, 5, 5]], dtype=np.float64),
    'NW': np.array([[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]], dtype=np.float64)
}
kirsch_edges = np.max([cv2.filter2D(binary_float, -1, k) for k in kirsch_kernels.values()], axis=0)

# Bộ lọc Gabor
gabor_kernels = [cv2.getGaborKernel((21, 21), 5, np.pi / 4, 10, 0.5, 0, ktype=cv2.CV_64F)]
gabor_edges = np.max([cv2.filter2D(binary_float, -1, k) for k in gabor_kernels], axis=0)

# Bộ lọc Laplacian of Gaussian (LoG)
log_blurred = cv2.GaussianBlur(binary_float, (5, 5), 0)
log_edges = cv2.Laplacian(log_blurred, cv2.CV_64F)

# Bộ lọc Marr-Hildreth (tương đương với LoG)
marr_hildreth_blurred = cv2.GaussianBlur(binary_float, (5, 5), 0)
marr_hildreth_edges = cv2.Laplacian(marr_hildreth_blurred, cv2.CV_64F)

# Bộ lọc Canny
canny_edges = cv2.Canny(binary_image, 10, 200)

# Bộ lọc Difference of Gaussians (DoG)
gaussian1 = cv2.GaussianBlur(binary_float, (5, 5), 1)
gaussian2 = cv2.GaussianBlur(binary_float, (5, 5), 2)
dog_edges = gaussian1 - gaussian2
dog_edges = np.uint8(np.absolute(dog_edges))

# Tạo nền trắng
white_background = np.ones_like(binary_image) * 255

# Hàm vẽ các đường biên lên nền trắng
def draw_edges_on_white(edges):
    result = white_background.copy()
    result[edges != 0] = 0  # Vẽ biên màu đen trên nền trắng
    return result

# Hàm lưu tọa độ biên vào file
def save_contours_to_txt(contours, filename):
    np.savetxt(filename, contours, fmt='%d', delimiter=' ', comments='')

# Hàm chuyển đổi ảnh thành tọa độ biên
def extract_contours_from_edges(edges, method_name):
    contours, _ = cv2.findContours(edges.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    folder = f'coordinates_output/{method_name}'
    os.makedirs(folder, exist_ok=True)
    for i, contour in enumerate(contours):
        # Chuyển đổi contours từ (x, y) thành (x, y) dạng float
        contour = np.squeeze(contour)
        if contour.size == 0:
            continue
        filename = os.path.join(folder, f'contour_{i+1}.txt')
        save_contours_to_txt(contour, filename)

# Tạo các ảnh biên
canny_on_white = draw_edges_on_white(canny_edges)
dog_on_white = draw_edges_on_white(dog_edges)
sobel_on_white = draw_edges_on_white(np.uint8(sobel_edges))
laplacian_on_white = draw_edges_on_white(np.uint8(laplacian_edges))
prewitt_on_white = draw_edges_on_white(np.uint8(prewitt_edges))
scharr_on_white = draw_edges_on_white(np.uint8(scharr_edges))
roberts_cross_on_white = draw_edges_on_white(np.uint8(roberts_cross_edges))
kirsch_on_white = draw_edges_on_white(np.uint8(kirsch_edges))
gabor_on_white = draw_edges_on_white(np.uint8(gabor_edges))
log_on_white = draw_edges_on_white(np.uint8(log_edges))
marr_hildreth_on_white = draw_edges_on_white(np.uint8(marr_hildreth_edges))

# Lưu các ảnh biên vào file
def save_images():
    os.makedirs('images_output', exist_ok=True)
    cv2.imwrite('images_output/canny_edges.png', canny_on_white)
    cv2.imwrite('images_output/dog_edges.png', dog_on_white)
    cv2.imwrite('images_output/sobel_edges.png', sobel_on_white)
    cv2.imwrite('images_output/laplacian_edges.png', laplacian_on_white)
    cv2.imwrite('images_output/prewitt_edges.png', prewitt_on_white)
    cv2.imwrite('images_output/scharr_edges.png', scharr_on_white)
    cv2.imwrite('images_output/roberts_cross_edges.png', roberts_cross_on_white)
    cv2.imwrite('images_output/kirsch_edges.png', kirsch_on_white)
    cv2.imwrite('images_output/gabor_edges.png', gabor_on_white)
    cv2.imwrite('images_output/lap_of_gaussian_edges.png', log_on_white)
    cv2.imwrite('images_output/marr_hildreth_edges.png', marr_hildreth_on_white)

# Lưu các tọa độ biên
def save_all_contours():
    extract_contours_from_edges(canny_edges, 'canny_edges')
    extract_contours_from_edges(np.uint8(sobel_edges), 'sobel_edges')
    extract_contours_from_edges(np.uint8(laplacian_edges), 'laplacian_edges')
    extract_contours_from_edges(np.uint8(prewitt_edges), 'prewitt_edges')
    extract_contours_from_edges(np.uint8(scharr_edges), 'scharr_edges')
    extract_contours_from_edges(np.uint8(roberts_cross_edges), 'roberts_cross_edges')
    extract_contours_from_edges(np.uint8(kirsch_edges), 'kirsch_edges')
    extract_contours_from_edges(np.uint8(gabor_edges), 'gabor_edges')
    extract_contours_from_edges(np.uint8(log_edges), 'log_edges')
    extract_contours_from_edges(np.uint8(marr_hildreth_edges), 'marr_hildreth_edges')
    extract_contours_from_edges(dog_edges, 'dog_edges')

# Lưu các ảnh và tọa độ
save_images()
save_all_contours()

# Hiển thị kết quả
cv2.imshow('Canny Edges on White Background', canny_on_white)
cv2.imshow('DoG Edges on White Background', dog_on_white)
cv2.imshow('Sobel Edges on White Background', sobel_on_white)
cv2.imshow('Laplacian Edges on White Background', laplacian_on_white)
cv2.imshow('Prewitt Edges on White Background', prewitt_on_white)
cv2.imshow('Scharr Edges on White Background', scharr_on_white)
cv2.imshow('Roberts Cross Edges on White Background', roberts_cross_on_white)
cv2.imshow('Kirsch Edges on White Background', kirsch_on_white)
cv2.imshow('Gabor Edges on White Background', gabor_on_white)
cv2.imshow('Laplacian of Gaussian Edges on White Background', log_on_white)
cv2.imshow('Marr-Hildreth Edges on White Background', marr_hildreth_on_white)

cv2.waitKey(0)
cv2.destroyAllWindows()
