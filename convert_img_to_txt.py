import cv2
import numpy as np
import os
import shutil

# Thư mục lưu trữ kết quả
base_folder = 'file_img'

# Xóa toàn bộ nội dung của thư mục 'file_img' nếu nó đã tồn tại
if os.path.exists(base_folder):
    shutil.rmtree(base_folder)

# Đảm bảo thư mục 'file_img' tồn tại sau khi xóa
os.makedirs(base_folder)

# Danh sách các ảnh cần xử lý
images = ['vn.jpg', 'v2.jpg', 'v3.jpg']

# Tên thư mục tương ứng với từng ảnh
folder_names = ['file1', 'file2', 'file3']

# Xử lý từng ảnh
for image_file, folder_name in zip(images, folder_names):
    # Đọc ảnh theo chế độ xám (grayscale)
    image = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
    
    # Áp dụng bộ lọc Gaussian để làm mịn ảnh
    #smoothed_image = cv2.GaussianBlur(image, (5, 5), 1.5)
    
    if image is None:
        # Nếu không thể đọc ảnh, in thông báo và tiếp tục với ảnh tiếp theo
        print(f"Không thể đọc ảnh: {image_file}")
        continue

    # # Tạo kernel cho bộ lọc làm sắc nét
    # kernel = np.array([[0, -1, 0],
    #                [-1, 5,-1],
    #                [0, -1, 0]])

    # # Áp dụng bộ lọc để làm sắc nét ảnh
    # sharpened = cv2.filter2D(image, -1, kernel)

    # Áp dụng Otsu's Binarization để tự động tìm ngưỡng và chuyển đổi thành ảnh nhị phân
    _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # # Áp dụng Canny edge detection lên ảnh nhị phân
    edges = cv2.Canny(binary_image, 100,200 )
    #Hiển thị ngưỡng tự động tìm được
    print(f'Threshold value: {_}')
    #cv2.imshow(f'binary_image - {image_file}', binary_image)
    cv2.imshow(f'edges - {image_file}', edges)

    # Tìm các đường biên (contours) từ ảnh đã phát hiện đường biên
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Tạo thư mục cho ảnh hiện tại
    folder = os.path.join(base_folder, folder_name)
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Chuyển đổi ảnh từ chế độ xám sang màu để vẽ các đường biên
    image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # Vẽ các đường biên lên ảnh màu
    cv2.drawContours(image_color, contours, -1, (0, 255, 0), 1)

    # Hiển thị ảnh với các đường biên
    #cv2.imshow(f'Contours - {image_file}', image_color)

    # Lưu từng đường biên vào một file văn bản khác nhau
    for i, contour in enumerate(contours):
        # Tạo tên file cho từng đường biên
        filename = os.path.join(folder, f'contour_{i+1}.txt')
        # Mở file và ghi tọa độ của các điểm trong đường biên
        with open(filename, 'w') as file:
            for point in contour:
                x, y = point[0]
                file.write(f"{x} {y}\n")
    
    # In thông báo cho biết tọa độ các đường biên đã được lưu
    print(f"Tọa độ các đường biên của ảnh {image_file} đã được lưu vào thư mục {folder}")

# Đợi cho đến khi nhấn phím bất kỳ để đóng cửa sổ hiển thị
cv2.waitKey(0)
cv2.destroyAllWindows()
