import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk
import copy

def clear_memset(self):
    self.values = {}
    self.entries = {}
    
    self.robot1_values = {}
    self.robot1_entries = {}
    self.robot1_algorithm = "backtracking";
    self.robot1_start_state = [];
    
    self.start_state = []
    self.goal_state = []
    self.mode = "hard";
    self.cnt_mistake = 0;
    self.is_playing = False;
    self.is_using_pencil = False;
    self.selected_entry = "";

def check_and_confirm(self, string, mode):
    if self.is_playing:
        result = messagebox.askokcancel("Xác nhận", "Bạn có chắc chắn muốn bỏ trò chơi và chuyển trang?")
        if result:  # Nếu người dùng chọn "OK"
            self.switch_page(string, mode)
        else:
            print("Đã hủy bỏ thao tác chuyển trang.")
    else: 
        self.switch_page(string, mode)

def switch_page(self, string, mode):
    self.clear_memset();

     # Thực hiện thao tác chuyển trang tại đây        
    if string == "human_vs_robot":
        self.human_vs_robot(self.board_frame);
    elif string == "human_single":
        self.human_single(self.board_frame, mode)

def fill_game_board(self, mode):
    self.generate_sudoku(mode);
    
    for row in range(1,10):
        for col in range(1,10):
            self.selected_entry = str(row) + str(col);
            self.enter_start_number(self.start_state[row - 1][col - 1])

def show_level_buttons(self):
    if self.level_buttons_visible:
        self.easy_button.grid_remove()
        self.middle_button.grid_remove()
        self.hard_button.grid_remove()
    else:  
        self.easy_button = ctk.CTkButton(self.sidebar, text="Easy",fg_color="#F64444", font=("Arial", 14,"bold"),corner_radius=6, width=150, command=lambda: self.check_and_confirm("human_single", "easy"))
        self.easy_button.grid(row=2, column=0, padx=30,pady=(0,2))
                    
        self.middle_button = ctk.CTkButton(self.sidebar, text="Middle",fg_color="#F64444", font=("Arial", 14,"bold"),corner_radius=6, width=150, command=lambda: self.check_and_confirm("human_single", "medium"))
        self.middle_button.grid(row=3, column=0, padx=30,pady=2)
                    
        self.hard_button = ctk.CTkButton(self.sidebar, text="Hard",fg_color="#F64444", font=("Arial", 14,"bold"),corner_radius=6, width=150, command=lambda: self.check_and_confirm("human_single", "hard"))
        self.hard_button.grid(row=4, column=0, padx=30,pady=2)
        
    self.level_buttons_visible = not self.level_buttons_visible
    
def show_AI_options_buttons(self):
    if self.level_buttons_visible:
        self.easy_button.grid_remove()
        self.middle_button.grid_remove()
        self.hard_button.grid_remove()
    else:  
        self.easy_button = ctk.CTkButton(self.sidebar, text="Backtracking",fg_color="#F64444", font=("Arial", 14,"bold"),corner_radius=6, width=150, command=lambda: self.check_and_confirm("human_single", "easy"))
        self.easy_button.grid(row=7, column=0, padx=30,pady=(0,2))
                    
        self.middle_button = ctk.CTkButton(self.sidebar, text="Constraint Propagation",fg_color="#F64444", font=("Arial", 14,"bold"),corner_radius=6, width=150, command=lambda: self.check_and_confirm("human_single", "medium"))
        self.middle_button.grid(row=8, column=0, padx=30,pady=2)
                    
        self.hard_button = ctk.CTkButton(self.sidebar, text="Dancing Link",fg_color="#F64444", font=("Arial", 14,"bold"),corner_radius=6, width=150, command=lambda: self.check_and_confirm("human_single", "hard"))
        self.hard_button.grid(row=9, column=0, padx=30,pady=2)
        
    self.level_buttons_visible = not self.level_buttons_visible

def select_entry(self, key):
    """Đánh dấu ô được chọn và các ô liên quan."""
    # Xóa màu của các ô đã được chọn trước đó
    self.clear_highlight()
    print(key);
    # Tô màu cho ô được chọn và các ô liên quan
    col, row = key[0], key[1]
    self.entry = key

    # Tô màu các ô cùng hàng, cột và vùng 3x3
    for k, entry in self.entries.items():
        entry_col, entry_row = k[0], k[1]
        same_row = (entry_row == row)
        same_col = (entry_col == col)
        same_box = ((int(entry_col) - 1) // 3 == (int(col) - 1) // 3) and ((int(entry_row) - 1) // 3 == (int(row) - 1) // 3)

        if same_row or same_col or same_box:
            entry.config(bg="#efefef")
    
    # Tô màu riêng cho ô được chọn
    self.entries[key].config(bg="#c2d9cf")
    self.selected_entry = key;

def clear_highlight(self):
    """Xóa màu của tất cả các ô để đưa về trạng thái ban đầu."""
    for entry in self.entries.values():
        entry.config(bg="white")

def set_value(self, value):
    row = int(self.selected_entry[0]) - 1
    col = int(self.selected_entry[1]) - 1

    """Đặt giá trị vào ô được chọn."""
    
    print("1.",)
    print("2.",self.selected_entry) 
    print("3.",value)
    print("4.",self.values[self.selected_entry]);
    print("5. ",row , " " , col);


    if self.start_state[row][col] != 0:
        return
    

    if self.selected_entry:
        self.values[self.selected_entry].set(value)
        self.clear_highlight()
        if (self.is_using_pencil == True):
            self.enter_small_number(value)
        else:
            self.enter_large_number(value)

def pencil_action(self):
    if (self.is_using_pencil):
        self.pencil_status.configure(text="off");
        self.pencil_status.configure(bg="red");
    else:
        self.is_using_pencil =self.pencil_status.configure(text="on");
        self.pencil_status.configure(bg="green");

    self.is_using_pencil = not self.is_using_pencil;
  
def new_game_action(self, mode):
    self.fill_game_board(mode);
    self.reset_timer();
    self.cnt_mistake = 0;
    self.mistakes_cnt.config(text=str(self.cnt_mistake))

def fill_resolve_AI(self,board):
    for row in range(1,10):
        print(board[row-1]);
    #print(self.robot1_start_state)
    for row in range(1,10):
        for col in range(1,10):
            if (self.robot1_start_state[row - 1][col - 1] == 0):
                self.robot1_entries[str(row)+str(col)].delete("all")
                self.robot1_entries[str(row)+str(col)].create_text(15, 15, text=str(board[row-1][col-1]), font=("Arial", 20), anchor="center", fill="green")
    self.done_game_action("AI backtracking")

def erase(self):
    row = int(self.selected_entry[0]) - 1
    col = int(self.selected_entry[1]) - 1
    
    if self.start_state[row][col] == 0:
        self.entries[self.selected_entry].delete("all")
    else:
        return;
        #messagebox.showerror("Message", "Số này không xóa được")
    
def enter_start_number(self, number):
    
    print(self.selected_entry);
    print(type (self.entries[self.selected_entry]))
    self.entries[self.selected_entry].delete("all")  # Xóa nội dung trước đó
    
    if (self.robot1_entries != {}) :
        self.robot1_entries[self.selected_entry].delete("all")
    color = "black"
    if (number > 0):
            
        self.entries[self.selected_entry].create_text(15, 15, text=str(number), font=("Arial", 20), anchor="center", fill=color)
        if (self.robot1_entries != {}) :
            self.robot1_entries[self.selected_entry].create_text(15, 15, text=str(number), font=("Arial", 20), anchor="center", fill=color)


def enter_large_number(self, number):
    
    if (self.selected_entry == ""):
        print("=-=============================");
        return
    self.entries[self.selected_entry].delete("all")  # Xóa nội dung trước đó
    
    row = int(self.selected_entry[0]) - 1
    col = int(self.selected_entry[1]) - 1

    if number == self.goal_state[row][col]:
        self.start_state[row][col] = number
        color = "green"
        self.blanks -= 1
        if (self.blanks == 0):
            self.done_game_action("Người chơi");
            
    else:
        color = "red";
        messagebox.showerror("Error", "Bạn đã nhập sai số!")
        self.increase_mistake()
    
    if (number > 0):
        self.entries[self.selected_entry].create_text(15, 15, text=str(number), font=("Arial", 20), anchor="center", fill=color)


# Hàm để nhập số nhỏ nằm ở góc trái trên ô với font-size 12
def enter_small_number(self, number):
    self.entries[self.selected_entry].delete("all")  # Xóa nội dung trước đó
    self.entries[self.selected_entry].configure(bg="#fff")  # Khôi phục lại màu nền
    if (number > 0):
        self.entries[self.selected_entry].create_text(5, 5, text=str(number), font=("Arial", 12), anchor="nw")  # Đặt số ở góc trái trên

def increase_mistake(self):
    self.cnt_mistake += 1;
    self.mistakes_cnt.config(text=str(self.cnt_mistake))

def update_timer(self):
    if self.running:
        # Tăng giây và cập nhật hiển thị thời gian
        self.seconds += 1
        minutes = self.seconds // 60
        seconds = self.seconds % 60
        self.time_display.config(text=f"{minutes:02}:{seconds:02}")
        # Gọi lại hàm này sau 1000ms (1 giây)
        self.time_display.after(1000, self.update_timer)

def start_timer(self):
    # Bắt đầu đếm giờ nếu chưa chạy
    if not self.running:
        self.running = True
        self.update_timer()        

def reset_timer(self):
    
    
    # Đặt lại thời gian và cập nhật hiển thị
    self.seconds = 0
    self.time_display.config(text="00:00")
    self.running = False    
def done_game_action(self, winner):
    self.running = False;
    minutes = self.seconds // 60
    seconds = self.seconds % 60
    messagebox.showinfo("Hoàn thành", winner +  f" chiến thắng.\n Thời gian hoàn thành: {minutes:02}:{seconds:02}")
    

def start_game_action(self, mode):
    self.is_playing = True    
    self.start_timer()
    
    board = copy.deepcopy(self.robot1_start_state)

    #self.solve_sudoku_backtracking(board);
    #self.solve_sudoku_constraint_propagation(board);
    self.solve_sudoku_dancing_links(board);
    


    return;
    
    if self.robot1_algorithm == "backtracking":
        #self.solve_sudoku_constraint_propagation(board)            
        tmp = self.solve_sudoku_backtracking(board)
        #print(tmp);
        self.fill_resolve_AI(board)

        
    if self.robot1_algorithm == "constraint_propagation":
        self.solve_sudoku_constraint_propagation(board)            
        self.fill_resolve_AI(board)
        
