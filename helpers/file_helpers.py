import os
from PIL import Image, ImageTk

def load_sudoku_img(file) :
    base_dir = os.path.dirname(__file__)
    
    # Đường dẫn đến file ảnh trong thư mục `sudoku`
    image_path = os.path.join(base_dir, "../sudoku", file)  # Thay "your_image.png" bằng tên file thực tế
    # Mở ảnh bằng PIL
    return Image.open(image_path)

