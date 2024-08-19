import turtle
import os
import cv2
from PIL import Image
import pygame

# Khởi tạo pygame mixer
pygame.mixer.init()
sound = pygame.mixer.Sound("a.mp3")
#sound.play()

# Hàm lấy kích thước của ảnh
def get_image_size(image_path):
    if os.path.exists(image_path):
        with Image.open(image_path) as img:
            return img.size
    else:
        print(f"Tệp ảnh {image_path} không tồn tại.")
        return 800, 600  # Trả về kích thước mặc định nếu ảnh không tồn tại

# Hàm đọc tọa độ từ file văn bản
def read_coordinates(filename):
    coordinates = []
    with open(filename, 'r') as file:
        for line in file:
            x, y = map(int, line.strip().split())
            coordinates.append((x, y))
    return coordinates

# Hàm chuyển đổi tọa độ từ hệ tọa độ ảnh sang hệ tọa độ của Turtle
def convert_coordinates(x, y, image_width, image_height, window_width, window_height):
    turtle_x = (x / image_width) * window_width - window_width / 2
    turtle_y = (1 - y / image_height) * window_height - window_height / 2
    return turtle_x, turtle_y

# Hàm vẽ đường biên từ file tọa độ
def draw_contour(filename, image_width, image_height, window_width, window_height):
    coordinates = read_coordinates(filename)
    if not coordinates:
        print(f"No data to draw from {filename}")
        return
    
    turtle.penup()
    x, y = convert_coordinates(*coordinates[0], image_width, image_height, window_width, window_height)
    turtle.goto(x, y)
    turtle.pendown()
    
    for x, y in coordinates[1:]:
        turtle_x, turtle_y = convert_coordinates(x, y, image_width, image_height, window_width, window_height)
        turtle.goto(turtle_x, turtle_y)
    
    # Vẽ đường biên hoàn chỉnh bằng cách trở về điểm đầu
    turtle.goto(*convert_coordinates(*coordinates[0], image_width, image_height, window_width, window_height))

# Hàm thiết lập Turtle và vẽ các đường biên từ thư mục
def setup_turtle(image_path, directory):
    image_width, image_height = get_image_size(image_path)
    turtle.setup(image_width, image_height)
    turtle.clear()
    turtle.speed(0)
    turtle.showturtle()
    turtle.color("red")
    #turtle.tracer(0) # Nếu muốn tắt hiệu ứng vẽ liên tục
    turtle.hideturtle()
    
    # Duyệt qua các file trong thư mục và vẽ các đường biên
    for filename in sorted(os.listdir(directory)):
        if filename.startswith('contour_') and filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            draw_contour(filepath, image_width, image_height, image_width, image_height)
    
    turtle.update()
    # cv2.waitKey(0) # Nếu cần đợi phím nhấn
    cv2.destroyAllWindows()  # Đóng tất cả các cửa sổ OpenCV

# Hàm hiển thị ảnh bằng OpenCV
def show_image(image_path, window_name):
    img = cv2.imread(image_path)
    cv2.namedWindow(window_name, cv2.WINDOW_KEEPRATIO)
    cv2.imshow(window_name, img)
    cv2.moveWindow(window_name, 0, 0)

# Hàm chính thực thi chương trình
def main():
    # Xử lý ảnh đầu tiên
    image_path1 = 'vn.jpg'
    show_image(image_path1, 'Image 1')
    directory1 = 'file_img_test/file1'
    setup_turtle(image_path1, directory1)

    # Xử lý ảnh thứ hai
    image_path2 = 'vn.jpg'
    show_image(image_path2, 'Image 2')
    directory2 = 'file_img_test/file2'
    setup_turtle(image_path2, directory2)

    # # Xử lý ảnh thứ ba
    # image_path3 = 'v3.jpg'
    # show_image(image_path3, 'Image 3')
    # directory3 = 'file_img/file3'
    # setup_turtle(image_path3, directory3)
    
    # Đợi phím nhấn và kết thúc chương trình
    cv2.waitKey(0)
    turtle.done()  # Bắt đầu vòng lặp chính của Turtle

# Điểm vào của chương trình
if __name__ == "__main__":
    main()
