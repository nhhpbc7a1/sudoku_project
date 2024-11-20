import tkinter as tk
from tkinter import ttk
import random
import numpy as np

def generate_sudoku(self, level="medium"):
    def fill_board(board):
        def is_safe(board, row, col, num):
            for x in range(self.game_size ** 2):
                if board[row][x] == num or board[x][col] == num:
                    return False
            start_row, start_col = self.game_size * (row // self.game_size), self.game_size * (col // self.game_size)
            for i in range(self.game_size):
                for j in range(self.game_size):
                    if board[i + start_row][j + start_col] == num:
                        return False
            return True

        def solve(board):
            numbers = list(range(1, self.game_size ** 2 + 1))
            random.shuffle(numbers)  # Ngẫu nhiên chọn thứ tự các số từ 1 đến 9
            for row in range(self.game_size ** 2):
                for col in range(self.game_size ** 2):
                    if board[row][col] == 0:
                        for num in numbers:
                            if is_safe(board, row, col, num):
                                board[row][col] = num
                                if solve(board):
                                    return True
                                board[row][col] = 0
                        return False
            return True

        solve(board)
        return board

    # Tạo bảng Sudoku hoàn chỉnh với các số ngẫu nhiên
    board = np.zeros((self.game_size ** 2, self.game_size ** 2), dtype=int)
    board = fill_board(board)
    self.goal_state = board.tolist()

    if (self.game_size == 3):
        # Xác định số ô sẽ xóa dựa vào mức độ khó
        if level == "easy":
            self.blanks = 1
        elif level == "medium":
            self.blanks = 40
        elif level == "hard":
            self.blanks = 50
        else:
            raise ValueError("Mức độ chỉ chấp nhận: 'easy', 'medium' hoặc 'hard'.")
        
    if (self.game_size == 4):

        if level == "easy":
            self.blanks = 60
        elif level == "medium":
            self.blanks = 80
        elif level == "hard":
            self.blanks = 100
        else:
            raise ValueError("Mức độ chỉ chấp nhận: 'easy', 'medium' hoặc 'hard'.")


    # Xóa ngẫu nhiên các ô để tạo bảng Sudoku chưa hoàn chỉnh
    for _ in range(self.blanks):
        row, col = random.randint(0, self.game_size**2 - 1), random.randint(0, self.game_size**2 - 1)
        while board[row][col] == 0:
            row, col = random.randint(0, self.game_size**2 - 1), random.randint(0, self.game_size**2 - 1)
        board[row][col] = 0

    self.start_state = board.tolist()
    self.robot1_start_state = board.tolist()




    
def int_to_alpha(x):
    return chr(x + ord('A'));

def solve_sudoku_backtracking(self, board):
    
    if self.stop_flag:
        return False
    
    # Tìm một ô trống trong bảng
    empty_cell = self.find_empty_cell(board)
    if not empty_cell:
        # Nếu không còn ô trống nào, tức là Sudoku đã được giải xong
        self.fill_resolve_AI(board);
        self.root.exit();
        return True

    row, col = empty_cell

    # Thử các số từ 1 đến 9 vào ô trống
    for num in range(1, self.game_size**2 + 1):
        
        if self.is_valid(board, row, col, num):
            board[row][col] = num  # Đặt số nếu hợp lệ
            
            
            self.robot1_entries[int_to_alpha(row)+int_to_alpha(col)].create_text(5, 5, text=str(num), font=("Arial", 12), anchor="nw")  # Đặt số ở góc trái trên
            
            self.root.update()  # Cập nhật giao diện
            
            #if (self.stop_flag == False):
                #self.root.after(1000)  

            
            # Gọi đệ quy hàm solve_sudoku_backtracking
            if self.solve_sudoku_backtracking(board):
                return True

            self.robot1_entries[int_to_alpha(row)+int_to_alpha(col)].delete("all")

            # Hoàn tác nếu không giải được với số hiện tại
            board[row][col] = 0

    # Quay lại (backtracking) nếu không tìm được số phù hợp
    return False


def solve_sudoku_constraint_propagation(self, board):
    """
    Giải bài toán Sudoku bằng thuật toán Constraint Propagation.
    """
    # Hàm helper để xác định ô có thể chứa số nào
    def possible_values(board, row, col):
        if board[row][col] != 0:
            return []  # Nếu ô đã có giá trị, không cần tính toán
        
        values = set(range(1, self.game_size**2 + 1))  # Các giá trị có thể là từ 1 đến 9
        
        # Loại bỏ các giá trị đã có trong hàng
        values -= set(board[row])
        
        # Loại bỏ các giá trị đã có trong cột
        values -= set(board[i][col] for i in range(self.game_size ** 2))
        
        # Loại bỏ các giá trị đã có trong ô 3x3
        start_row, start_col = self.game_size * (row // self.game_size), self.game_size * (col // self.game_size)
        for i in range(self.game_size):
            for j in range(self.game_size):
                values.discard(board[start_row + i][start_col + j])
        
        return values

    # Hàm đệ quy để giải Sudoku
    def constraint_propagation(board):
        
        if self.stop_flag:
            return False

        # Tìm ô trống đầu tiên
        empty_cell = self.find_empty_cell(board)
        if not empty_cell:
            # Nếu không còn ô trống, Sudoku đã được giải
            return True
        
        row, col = empty_cell
        
        # Lấy danh sách giá trị có thể điền vào ô
        for num in possible_values(board, row, col):
            board[row][col] = num  # Thử điền số vào ô
            
            self.robot1_entries[int_to_alpha(row)+int_to_alpha(col)].create_text(5, 5, text=str(num), font=("Arial", 12), anchor="nw") 
            self.root.update()  # Cập nhật giao diện
            
            #if (self.stop_flag == False):
                #self.root.after(1000)
                
            # Gọi đệ quy để giải tiếp
            if constraint_propagation(board):
                return True
            
            # Hoàn tác nếu không giải được
            self.robot1_entries[int_to_alpha(row)+int_to_alpha(col)].delete("all")
            board[row][col] = 0
        
        # Trả về False nếu không có giá trị hợp lệ
        return False

    # Gọi hàm giải với bảng Sudoku ban đầu
    constraint_propagation(board)

    
def find_empty_cell(self, board):
    # Tìm một ô trống đầu tiên (được biểu diễn bằng số 0)
    for i in range(self.game_size ** 2):
        for j in range(self.game_size ** 2):
            if board[i][j] == 0:
                return (i, j)
    return None



def is_valid(self, board, row, col, num):
    # Kiểm tra xem số num có hợp lệ trong hàng row, cột col và ô 3x3 không
    # Kiểm tra hàng
    for i in range(self.game_size ** 2):
        if board[row][i] == num:
            return False

    # Kiểm tra cột
    for i in range(self.game_size ** 2):
        if board[i][col] == num:
            return False

    # Kiểm tra ô 3x3
    start_row, start_col = self.game_size * (row // self.game_size), self.game_size * (col // self.game_size)
    for i in range(self.game_size):
        for j in range(self.game_size):
            if board[start_row + i][start_col + j] == num:
                return False

    # Nếu không vi phạm quy tắc nào, trả về True
    return True    

