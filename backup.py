import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter as ctk
import random
import time  # Thêm thư viện time để tính toán thời gian
from tkinter import messagebox
from collections import deque
import os
import numpy as np
import copy

class Sudoku:
    def __init__(self, root):
        self.game_size = 3;
        self.selected_entry = ""
        self.root = root
        self.root.title("Sodoku")
        self.root.geometry("900x550")
        #self.root.state('zoomed')
        #self.root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        self.root.configure(bg="#FDE2BC")
        

        self.sidebar = tk.Frame(self.root, bg="#D2691E", width=250)
        self.sidebar.pack(side="left", fill="y")
        
        image_path = "icons8-sudoku-100.png"
        image = load_sudoku_img(image_path)
        tk_image = ImageTk.PhotoImage(image)
        
        self.logo_label = tk.Label(self.sidebar, image=tk_image,  bg="#D2691E",width=180,height=150, )
        self.logo_label.image = tk_image  # Giữ tham chiếu để tránh bị garbage collected
        self.logo_label.grid(row=0,column=0, pady=1)

        self.level_buttons_visible = False
        self.buttonSingle = ctk.CTkButton(self.sidebar, text="Single Player", fg_color="#C72424", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=150, height=40, command=self.show_level_buttons)
        self.buttonSingle.grid(row=1, column=0, padx=30,pady=2)
        
        self.buttonVs = ctk.CTkButton(self.sidebar, text="Machine vs Player", fg_color="#C72424", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=150, height=40, command=lambda: self.check_and_confirm("human_vs_robot", ""))
        self.buttonVs.grid(row=5,column=0, pady=(20,10))
        
        self.buttonMachine = ctk.CTkButton(self.sidebar, text="Machine mode", fg_color="#C72424", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=150, height=40, command=self.show_AI_options_buttons)
        self.buttonMachine.grid(row=6,column=0, pady=10)
        
        self.buttonExit = ctk.CTkButton(self.sidebar, text="Exit", fg_color="#C72424", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=150, height=40)
        self.buttonExit.grid(row=10,column=0, pady=10)
        
        
        #Right part
        
        self.board_frame = tk.Frame(self.root,bg="#FDE2BC", width= 1000)
        self.board_frame.pack(side="right", fill="both", expand=True)

        self.values = {}
        self.entries = {}
        
        self.robot1_values = {}
        self.robot1_entries = {}
        self.robot1_algorithm = "back";
        self.robot1_start_state = [];
        
        self.start_state = []
        self.goal_state = []
        self.mode = "hard";
        self.cnt_mistake = 0;
        self.is_playing = False;
        self.is_using_pencil = False;

        self.human_single(self.board_frame, "easy");
        
    
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
            
    def create_board(self, frame):
        
        for box_col in range(self.game_size):
            for box_row in range(self.game_size):
                tmp_frame_2 = tk.Frame(frame,bg="black")
                tmp_frame_2.grid(column=box_col, row=box_row)
                
                box = ttk.Frame(tmp_frame_2)
                box.grid(padx = 1, pady = 1)
                for cell_col in range(self.game_size):
                    for cell_row in range(self.game_size):
                        v = tk.StringVar()
                        col = '123456789'[3*box_col + cell_col]
                        row = '123456789'[3*box_row + cell_row]
                        key = col + row
                        self.values[key] = v
                        
                        entryPlayer = tk.Canvas(box, width=33, height=33, bg="#fff", highlightthickness=1, highlightbackground="lightgray")
                        entryPlayer.grid(row=cell_row, column=cell_col)
                        
                        self.entries[key] = entryPlayer
                        entryPlayer.bind("<Button-1>", lambda e, key=key: self.select_entry(key))

                        
    def create_robot_board(self, frame, algorithm_name):
        
        for box_col in range(self.game_size):
            for box_row in range(self.game_size):
                tmp_frame_2 = tk.Frame(frame,bg="black")
                tmp_frame_2.grid(column=box_col, row=box_row)
                
                box = ttk.Frame(tmp_frame_2)
                box.grid(padx = 1, pady = 1)
                for cell_col in range(self.game_size):
                    for cell_row in range(self.game_size):
                        v = tk.StringVar()
                        col = '123456789'[3*box_col + cell_col]
                        row = '123456789'[3*box_row + cell_row]
                        key = col + row
                        self.robot1_values[key] = v
                        
                        entryPlayer = tk.Canvas(box, width=33, height=33, bg="#fff", highlightthickness=1, highlightbackground="lightgray")
                        entryPlayer.grid(row=cell_row, column=cell_col)
                        
                        self.robot1_entries[key] = entryPlayer
                        
        

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
        
        print()
        print(self.selected_entry) 
        print(value)
        print(self.values[self.selected_entry]);

        if self.start_state[row][col] != 0:
            return
        

        if self.selected_entry:
            self.values[self.selected_entry].set(value)
            self.clear_highlight()
            if (self.is_using_pencil == True):
                self.enter_small_number(value)
            else:
                self.enter_large_number(value)
                
    def human_vs_robot(self, board_frame):
        mode = "hard"
        for widget in board_frame.winfo_children():
                widget.destroy()
                
        # top-right part
        top_frame = tk.Frame(board_frame, bg="#FDE2BC", height=50)
        top_frame.pack(fill="x")
        # top-right part
        mistakes_label = tk.Label(top_frame, text="Mistakes:", fg="black",bg="#FDE2BC", font=("Arial", 12))
        mistakes_label.grid(row=0, column=0, padx=(30,2),pady=10)
        self.mistakes_cnt = tk.Label(top_frame, text="0", fg="black",bg="#FDE2BC", font=("Arial", 12))
        self.mistakes_cnt.grid(row=0, column=1, padx=0,pady=10)
        self.cnt_mistake = 0;
        self.mistakes_cnt.config(text=str(self.cnt_mistake))
        
        level_label = tk.Label(top_frame, text=mode, fg="#E2810C",bg="#FDE2BC", font=("Arial", 12, "bold"))
        level_label.grid(row=0, column=2, padx=40,pady=10)
    
        timer_label = tk.Label(top_frame, text="Time: ", fg="black",bg="#FDE2BC", font=("Arial", 12,"bold"))
        timer_label.grid(row=0, column=3, padx=(0,5),pady=10)
        
        self.time_display = tk.Label(top_frame, text="00:00", fg="black", bg="#FDE2BC", font=("Arial", 12, "bold"))
        self.time_display.grid(row=0, column=4, padx=(0,5), pady=10)
        
        self.seconds = 0
        self.running = False
                
        # sodoku board
        #middle part
        middle_frame = tk.Frame(board_frame,bg="#FDE2BC", height=300)
        middle_frame.pack(fill="both", expand=True)
        
        middle_frame.grid_columnconfigure(0, weight=50)  # Cột trái chiếm 65%
        middle_frame.grid_columnconfigure(1, weight=50)  # Cột phải chiếm 35%
        #hesesfs
        #events
    
        # middle left-part
        left_middle_frame = tk.Canvas(middle_frame, width= 300, height=300, bg="#FDE2BC", highlightthickness=1, highlightbackground="black")
        left_middle_frame.grid(row=0, column=0, sticky="nsw", padx=(20,0))

        self.create_robot_board(left_middle_frame, "backtracking");       
             
        
        right_middle_frame = tk.Canvas(middle_frame, width= 300, height=300, bg="#FDE2BC", highlightthickness=1, highlightbackground="black")
        right_middle_frame.grid(row=0, column=1, sticky="nse", padx=(0,20))

        self.create_board(right_middle_frame);                    
        
    
    
        #  bottom right frame
        almostbottom_frame = tk.Frame(board_frame, height=75,bg="#FDE2BC")
        almostbottom_frame.pack(fill="x")
        
        spacer = tk.Label(almostbottom_frame, width=2, bg="#FDE2BC")
        spacer.grid(row=0, column=0,padx=45)
        for i in range(1, 10):
            button = ctk.CTkButton(almostbottom_frame, text=str(i), font=("Arial", 20, "bold"),text_color="#C72424", width=45, height=55, fg_color="#F9C57D",corner_radius=5, command=lambda num = i: self.set_value(num))
            button.grid(row=0, column=i, padx=5, pady=5)
    
        #  bottom right frame
    
        bottom_frame = tk.Frame(board_frame, height=75,bg="#FDE2BC")
        bottom_frame.pack(fill="x")
        
        buttonStart = ctk.CTkButton(bottom_frame, text="Start", fg_color="#25980E", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=100, height=40, command = lambda: self.start_game_action(mode))
        buttonStart.grid(row=0, column=0, padx=30)
    
        
        iconUndo = ImageTk.PhotoImage(load_sudoku_img("icons8-undo-30.png"))
        btnUndo = ctk.CTkButton(
           bottom_frame,
           text="Undo",
           image=iconUndo,
           compound="top",
           font=("Arial", 14, "bold"),
           fg_color="#F4CE98",
           text_color="Black",
           width=55, height=35,)
        btnUndo.grid(row=0, column=1, padx=(40,10),pady=20)
        iconErase = ImageTk.PhotoImage(load_sudoku_img("icons8-erase-30.png"))
        btnErase = ctk.CTkButton(
           bottom_frame,
           text="Erase",
           image=iconErase,
           compound="top",
           font=("Arial", 14, "bold"),
           fg_color="#F4CE98",
           text_color="Black",
           command = lambda: self.erase(),
           width=55, height=35,)
        btnErase.grid(row=0, column=2, padx=15,pady=20)
        
        self.iconPencil = ImageTk.PhotoImage(load_sudoku_img("icons8-pencil-30.png"))
        self.btnPencil = ctk.CTkButton(
           bottom_frame,
           text="Pencil",
           image=self.iconPencil,
           compound="top",
           font=("Arial", 14, "bold"),
           fg_color="#F4CE98",
           text_color="Black",
           command = lambda: self.pencil_action(),
           width=50, height=35,)
    
        self.btnPencil.grid(row=0, column=3, padx=(15,0),pady=20)
        self.pencil_status = tk.Label(bottom_frame, text="off", fg="black",bg="#FDE2BC", font=("Arial", 12))
        self.pencil_status.grid(row=0, column=4, padx=0,pady=20)

        
        
        iconHint = ImageTk.PhotoImage(load_sudoku_img("icons8-hint-30.png"))
        btnHint = ctk.CTkButton(
           bottom_frame,
           text="Hint",
           image=iconHint,
           compound="top",
           font=("Arial", 14, "bold"),
           fg_color="#F4CE98",
           text_color="Black",
           width=55, height=35,)
        btnHint.grid(row=0, column=5, padx=15,pady=20)
        
        newGame = ctk.CTkButton(bottom_frame, text="New Game", fg_color="#F64444", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=70, height=40, command = lambda : self.new_game_action(mode))
        newGame.grid(row=0, column=6,pady=20, padx=(40,0))
        self.mode = "hard"
    
    def human_single(self, board_frame, mode):
        
        
        for widget in board_frame.winfo_children():
            widget.destroy()
    
        
        # top-right part
        top_frame = tk.Frame(board_frame, bg="#FDE2BC", height=50)
        top_frame.pack(fill="x")
        # top-right part
        mistakes_label = tk.Label(top_frame, text="Mistakes:", fg="black",bg="#FDE2BC", font=("Arial", 12))
        mistakes_label.grid(row=0, column=0, padx=(30,2),pady=10)
        self.mistakes_cnt = tk.Label(top_frame, text="0", fg="black",bg="#FDE2BC", font=("Arial", 12))
        self.mistakes_cnt.grid(row=0, column=1, padx=0,pady=10)
        self.cnt_mistake = 0;
        self.mistakes_cnt.config(text=str(self.cnt_mistake))
        
        level_label = tk.Label(top_frame, text=mode, fg="#E2810C",bg="#FDE2BC", font=("Arial", 12, "bold"))
        level_label.grid(row=0, column=2, padx=40,pady=10)
    
        timer_label = tk.Label(top_frame, text="Time: ", fg="black",bg="#FDE2BC", font=("Arial", 12,"bold"))
        timer_label.grid(row=0, column=3, padx=(0,5),pady=10)
        
        self.time_display = tk.Label(top_frame, text="00:00", fg="black", bg="#FDE2BC", font=("Arial", 12, "bold"))
        self.time_display.grid(row=0, column=4, padx=(0,5), pady=10)
        
        self.seconds = 0
        self.running = False
        
        #newGame = ctk.CTkButton(top_frame, text="New Game", fg_color="#F64444", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=75, height=40)
        #newGame.grid(row=0, column=3,padx=30,pady=10)
    
        # sodoku board
        #middle part
        middle_frame = tk.Frame(board_frame,bg="#FDE2BC", height=310)
        middle_frame.pack(fill="both", expand=True)
        middle_frame.grid_columnconfigure(0, weight=65)  # Cột trái chiếm 65%
        middle_frame.grid_columnconfigure(1, weight=35)  # Cột phải chiếm 35%
        
        # middle left-part
        
        # middle left-part
        left_middle_frame = tk.Canvas(middle_frame, width= 300, height=300, bg="#FDE2BC", highlightthickness=1, highlightbackground="black")
        left_middle_frame.grid(row=0, column=0, sticky="nsw", padx=(20,0))

        self.create_board(left_middle_frame);                    
        
        #  middle right-part
        right_middle_frame = tk.Frame(middle_frame,bg="#FDE2BC",height=350)
        right_middle_frame.grid(row=0, column=1, sticky="nsw")
        
        for i in range(1, 10):
            button = ctk.CTkButton(right_middle_frame, text=str(i), font=("Arial", 32, "bold"),text_color="#C72424", width=60, height=65, fg_color="#F9C57D",corner_radius=5, command = lambda num = i : self.set_value(num))
            button.grid(row=(i-1)//3, column=(i-1)%3, padx=20, pady=20)
        
        bottom_frame = tk.Frame(board_frame, height=75,bg="#FDE2BC")
        bottom_frame.pack(fill="x")
        
        buttonStart = ctk.CTkButton(bottom_frame, text="Start", fg_color="#25980E", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=100, height=40, command = lambda: self.start_game_action(mode))
        buttonStart.grid(row=0, column=0, padx=30)
    
        
        iconUndo = ImageTk.PhotoImage(load_sudoku_img("icons8-undo-30.png"))
        btnUndo = ctk.CTkButton(
           bottom_frame,
           text="Undo",
           image=iconUndo,
           compound="top",
           font=("Arial", 14, "bold"),
           fg_color="#F4CE98",
           text_color="Black",
           width=55, height=35,)
        btnUndo.grid(row=0, column=1, padx=(40,10),pady=20)
        iconErase = ImageTk.PhotoImage(load_sudoku_img("icons8-erase-30.png"))
        btnErase = ctk.CTkButton(
           bottom_frame,
           text="Erase",
           image=iconErase,
           compound="top",
           font=("Arial", 14, "bold"),
           fg_color="#F4CE98",
           text_color="Black",
           command = lambda: self.erase(),
           width=55, height=35,)
        btnErase.grid(row=0, column=2, padx=15,pady=20)
        
        self.iconPencil = ImageTk.PhotoImage(load_sudoku_img("icons8-pencil-30.png"))
        self.btnPencil = ctk.CTkButton(
           bottom_frame,
           text="Pencil",
           image=self.iconPencil,
           compound="top",
           font=("Arial", 14, "bold"),
           fg_color="#F4CE98",
           text_color="Black",
           command = lambda: self.pencil_action(),
           width=50, height=35,)
    
        self.btnPencil.grid(row=0, column=3, padx=(15,0),pady=20)
        self.pencil_status = tk.Label(bottom_frame, text="off", fg="black",bg="#FDE2BC", font=("Arial", 12))
        self.pencil_status.grid(row=0, column=4, padx=0,pady=20)

        
        
        iconHint = ImageTk.PhotoImage(load_sudoku_img("icons8-hint-30.png"))
        btnHint = ctk.CTkButton(
           bottom_frame,
           text="Hint",
           image=iconHint,
           compound="top",
           font=("Arial", 14, "bold"),
           fg_color="#F4CE98",
           text_color="Black",
           width=55, height=35,)
        btnHint.grid(row=0, column=5, padx=15,pady=20)
        
        newGame = ctk.CTkButton(bottom_frame, text="New Game", fg_color="#F64444", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=70, height=40, command = lambda : self.new_game_action(mode) )
        newGame.grid(row=0, column=6,pady=20, padx=(40,0))
        
        self.mode = mode
    
    
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

    def start_game_action(self, mode):
        self.is_playing = True;    
        self.start_timer();
        
        if (self.robot1_algorithm == "backtracking"):
            board = copy.deepcopy(self.robot1_start_state)
            self.solve_sudoku_backtracking(board);
            self.fill_resolve_AI(board);
            #print(board);
    
    def fill_resolve_AI(self,board):
        print(board);
        print(self.robot1_start_state)
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
    
    def generate_sudoku(self, level="medium"):
        def fill_board(board):
            def is_safe(board, row, col, num):
                for x in range(self.game_size ** 2):
                    if board[row][x] == num or board[x][col] == num:
                        return False
                start_row, start_col = 3 * (row // 3), 3 * (col // 3)
                for i in range(self.game_size):
                    for j in range(self.game_size):
                        if board[i + start_row][j + start_col] == num:
                            return False
                return True
    
            def solve(board):
                numbers = list(range(1, 10))
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
        board = np.zeros((9, 9), dtype=int)
        board = fill_board(board)
        self.goal_state = board.tolist()
    
        # Xác định số ô sẽ xóa dựa vào mức độ khó
        if level == "easy":
            self.blanks = 1
        elif level == "medium":
            self.blanks = 40
        elif level == "hard":
            self.blanks = 50
        else:
            raise ValueError("Mức độ chỉ chấp nhận: 'easy', 'medium' hoặc 'hard'.")
    
        # Xóa ngẫu nhiên các ô để tạo bảng Sudoku chưa hoàn chỉnh
        for _ in range(self.blanks):
            row, col = random.randint(0, 8), random.randint(0, 8)
            while board[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            board[row][col] = 0
    
        self.start_state = board.tolist()
        self.robot1_start_state = board.tolist()
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
        
    def solve_sudoku_backtracking(self, board):
        # Tìm một ô trống trong bảng
        empty_cell = self.find_empty_cell(board)
        if not empty_cell:
            # Nếu không còn ô trống nào, tức là Sudoku đã được giải xong
            return True
    
        row, col = empty_cell
    
        # Thử các số từ 1 đến 9 vào ô trống
        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row][col] = num  # Đặt số nếu hợp lệ
                
                self.robot1_entries[str(row + 1)+str(col + 1)].create_text(5, 5, text=str(num), font=("Arial", 12), anchor="nw")  # Đặt số ở góc trái trên
                
                self.root.update()  # Cập nhật giao diện
                
                # Gọi đệ quy hàm solve_sudoku_backtracking
                if self.solve_sudoku_backtracking(board):
                    return True
    
                self.robot1_entries[str(row + 1)+str(col + 1)].delete("all")

                # Hoàn tác nếu không giải được với số hiện tại
                board[row][col] = 0
    
        # Quay lại (backtracking) nếu không tìm được số phù hợp
        return False
    
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
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(self.game_size):
            for j in range(self.game_size):
                if board[start_row + i][start_col + j] == num:
                    return False
    
        # Nếu không vi phạm quy tắc nào, trả về True
        return True    
    
    def start_game_action(self, mode):
        self.is_playing = True    
        self.start_timer()
        
        if self.robot1_algorithm == "backtracking":
            board = copy.deepcopy(self.robot1_start_state)
            tmp = self.solve_sudoku_backtracking(board)
            #self.solve_sudoku_constraint_propagation(board)        
            print(tmp)
            self.fill_resolve_AI(board)

            
        if self.robot1_algorithm == "constraint_propagation":
            board = copy.deepcopy(self.robot1_start_state)
            self.solve_sudoku_constraint_propagation(board)            
            self.fill_resolve_AI(board)

        

    
    def solve_sudoku_constraint_propagation(self, board):
        """
        Giải bài toán Sudoku bằng thuật toán Constraint Propagation.
        """
        # Hàm helper để xác định ô có thể chứa số nào
        def possible_values(board, row, col):
            if board[row][col] != 0:
                return []  # Nếu ô đã có giá trị, không cần tính toán
            
            values = set(range(1, 10))  # Các giá trị có thể là từ 1 đến 9
            
            # Loại bỏ các giá trị đã có trong hàng
            values -= set(board[row])
            
            # Loại bỏ các giá trị đã có trong cột
            values -= set(board[i][col] for i in range(self.game_size ** 2))
            
            # Loại bỏ các giá trị đã có trong ô 3x3
            start_row, start_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(3):
                for j in range(3):
                    values.discard(board[start_row + i][start_col + j])
            
            return values
    
        # Hàm đệ quy để giải Sudoku
        def constraint_propagation(board):
            # Tìm ô trống đầu tiên
            empty_cell = self.find_empty_cell(board)
            if not empty_cell:
                # Nếu không còn ô trống, Sudoku đã được giải
                return True
            
            row, col = empty_cell
            
            # Lấy danh sách giá trị có thể điền vào ô
            for num in possible_values(board, row, col):
                board[row][col] = num  # Thử điền số vào ô
                
                self.robot1_entries[str(row + 1)+str(col + 1)].create_text(15, 15, text=str(num), font=("Arial", 20), anchor="center", fill="green")
                self.root.update()  # Cập nhật giao diện
                
                # Gọi đệ quy để giải tiếp
                if constraint_propagation(board):
                    return True
                
                # Hoàn tác nếu không giải được
                self.robot1_entries[str(row + 1)+str(col + 1)].delete("all")
                board[row][col] = 0
            
            # Trả về False nếu không có giá trị hợp lệ
            return False
    
        # Gọi hàm giải với bảng Sudoku ban đầu
        constraint_propagation(board)
        self.fill_resolve_AI(board)

    


def load_sudoku_img(file) :
    base_dir = os.path.dirname(__file__)
    
    # Đường dẫn đến file ảnh trong thư mục `sudoku`
    image_path = os.path.join(base_dir, "sudoku", file)  # Thay "your_image.png" bằng tên file thực tế
    # Mở ảnh bằng PIL
    return Image.open(image_path)

    
if __name__ == "__main__":
    root = tk.Tk()
    game = Sudoku(root)
    root.mainloop()

