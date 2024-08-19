import cv2
import numpy as np
import os

# Đọc ảnh ở chế độ BGR
image = cv2.imread('vn.jpg')
height, width = image.shape[:2]

# Chuyển ảnh sang thang độ xám
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Chuyển ảnh xám sang nhị phân
# _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

# Áp dụng Otsu's Binarization để tự động tìm ngưỡng và chuyển đổi thành ảnh nhị phân
_, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print(f'Threshold value: {_}')


# Đảm bảo ảnh nhị phân là float64 cho các phép toán
binary_float = np.float64(binary_image)

# Tạo thư mục lưu trữ tọa độ
base_output_folder = 'coordinates_output_COLOR_BGR2GRAY'
os.makedirs(base_output_folder, exist_ok=True)

# Tạo thư mục con cho từng phương pháp
methods = [
    'canny_edges', 'sobel_edges', 'laplacian_edges',
    'prewitt_edges', 'scharr_edges', 'roberts_cross_edges',
    'kirsch_edges', 'gabor_edges', 'log_edges', 'marr_hildreth_edges', 'dog_edges'
]

for method in methods:
    os.makedirs(os.path.join(base_output_folder, method), exist_ok=True)

# Hàm lưu tọa độ của đường biên vào file
def save_coordinates(edges, folder, base_filename):
    contours, _ = cv2.findContours(edges.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i, contour in enumerate(contours):
        coordinates = contour.squeeze()
        if coordinates.ndim == 2 and coordinates.size > 0:
            np.savetxt(os.path.join(folder, f'contour_{i+1}.txt'), coordinates, fmt='%d')

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
canny_edges = cv2.Canny(binary_image, 100, 200)

# Bộ lọc Difference of Gaussians (DoG)
gaussian1 = cv2.GaussianBlur(binary_float, (5, 5), 1)
gaussian2 = cv2.GaussianBlur(binary_float, (5, 5), 2)
dog_edges = gaussian1 - gaussian2
dog_edges = np.uint8(np.absolute(dog_edges))

# Lưu tọa độ các đường biên
save_coordinates(canny_edges, os.path.join(base_output_folder, 'canny_edges'), 'contour')
save_coordinates(np.uint8(sobel_edges), os.path.join(base_output_folder, 'sobel_edges'), 'contour')
save_coordinates(np.uint8(laplacian_edges), os.path.join(base_output_folder, 'laplacian_edges'), 'contour')
save_coordinates(np.uint8(prewitt_edges), os.path.join(base_output_folder, 'prewitt_edges'), 'contour')
save_coordinates(np.uint8(scharr_edges), os.path.join(base_output_folder, 'scharr_edges'), 'contour')
save_coordinates(np.uint8(roberts_cross_edges), os.path.join(base_output_folder, 'roberts_cross_edges'), 'contour')
save_coordinates(np.uint8(kirsch_edges), os.path.join(base_output_folder, 'kirsch_edges'), 'contour')
save_coordinates(np.uint8(gabor_edges), os.path.join(base_output_folder, 'gabor_edges'), 'contour')
save_coordinates(np.uint8(log_edges), os.path.join(base_output_folder, 'log_edges'), 'contour')
save_coordinates(np.uint8(marr_hildreth_edges), os.path.join(base_output_folder, 'marr_hildreth_edges'), 'contour')
save_coordinates(np.uint8(dog_edges), os.path.join(base_output_folder, 'dog_edges'), 'contour')

# Hàm vẽ các đường biên từ tọa độ lên nền trắng
def draw_contours_on_white(edges):
    # Chuyển đổi edges thành ảnh nhị phân
    edges_uint8 = np.uint8(edges)
    
    # Tạo ảnh nền trắng
    result = np.ones((height, width), dtype=np.uint8) * 255
    
    # Vẽ các đường biên từ ảnh edges lên nền trắng
    result[edges_uint8 > 0] = 0  # Vẽ biên màu đen trên nền trắng
    
    return result

# Tạo thư mục để lưu ảnh
output_folder = 'images_output_COLOR_BGR2GRAY'
os.makedirs(output_folder, exist_ok=True)

# Lưu và hiển thị ảnh với các đường biên trên nền trắng
for name, edges in [
    ('Canny_Edges', canny_edges),
    ('Sobel_Edges', sobel_edges),
    ('Laplacian_Edges', laplacian_edges),
    ('Prewitt_Edges', prewitt_edges),
    ('Scharr_Edges', scharr_edges),
    ('Roberts_Cross_Edges', roberts_cross_edges),
    ('Kirsch_Edges', kirsch_edges),
    ('Gabor_Edges', gabor_edges),
    ('Laplacian_of_Gaussian_Edges', log_edges),
    ('Marr_Hildreth_Edges', marr_hildreth_edges),
    ('DoG_Edges', dog_edges)
]:
    # Vẽ các đường biên lên nền trắng
    edges_on_white = draw_contours_on_white(edges)
    
    # Lưu ảnh
    cv2.imwrite(os.path.join(output_folder, f'{name}_on_White_Background.png'), edges_on_white)
    
    # Hiển thị ảnh
    cv2.imshow(f'{name} on White Background', edges_on_white)

# Đợi người dùng nhấn phím để đóng tất cả cửa sổ hiển thị
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Đã lưu và hiển thị tất cả các ảnh với các đường biên trên nền trắng.")
print("Đã lưu tọa độ các đường biên vào các thư mục tương ứng.")
