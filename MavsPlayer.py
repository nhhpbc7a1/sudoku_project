import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter as ctk
import random
import time  # Thêm thư viện time để tính toán thời gian
from tkinter import messagebox
from collections import deque
import os

def load_sudoku_img(file) :
    base_dir = os.path.dirname(__file__)

    # Đường dẫn đến file ảnh trong thư mục `sudoku`
    image_path = os.path.join(base_dir, "sodoku", file)  # Thay "your_image.png" bằng tên file thực tế
    # Mở ảnh bằng PIL
    return Image.open(image_path)

class Sodoku:
    def __init__(self, root):
        self.root = root
        self.root.title("Sodoku")
        self.root.geometry("900x550")
        self.root.configure(bg="#FDE2BC")
        
        
        self.sidebar = tk.Frame(self.root, bg="#D2691E", width=250, height=550)
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
        
        self.buttonVs = ctk.CTkButton(self.sidebar, text="Machine vs Player", fg_color="#C72424", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=150, height=40)
        self.buttonVs.grid(row=5,column=0, pady=(20,10))
        
        self.buttonMachine = ctk.CTkButton(self.sidebar, text="Machine mode", fg_color="#C72424", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=150, height=40)
        self.buttonMachine.grid(row=6,column=0, pady=10)
        
        self.buttonExit = ctk.CTkButton(self.sidebar, text="Exit", fg_color="#C72424", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=150, height=40)
        self.buttonExit.grid(row=7,column=0, pady=10)
        
        #Right part
        
        self.board_frame = tk.Frame(self.root,bg="#FDE2BC")
        self.board_frame.pack(side="right", fill="both", expand=True)
        
        # top-right part
        self.top_frame = tk.Frame(self.board_frame, bg="#FDE2BC", height=50)
        self.top_frame.pack(fill="x")
        # top-right part
        #machine
        self.mistakes_label = tk.Label(self.top_frame, text="Mistakes:", fg="black",bg="#FDE2BC", font=("Arial", 12))
        self.mistakes_label.grid(row=0, column=0, padx=20,pady=10)
        
        self.level_label = tk.Label(self.top_frame, text="Machine", fg="#E2810C",bg="#FDE2BC", font=("Arial", 12, "bold"))
        self.level_label.grid(row=0, column=1, padx=30,pady=10)

        self.timer_label = tk.Label(self.top_frame, text="Time: ", fg="black",bg="#FDE2BC", font=("Arial", 12,  "bold"))
        self.timer_label.grid(row=0, column=2, padx=20,pady=10)
        #player
        self.mistakes_label = tk.Label(self.top_frame, text="Mistakes:", fg="black",bg="#FDE2BC", font=("Arial", 12))
        self.mistakes_label.grid(row=0, column=3,padx=40)
        
        self.level_label = tk.Label(self.top_frame, text="Player", fg="#E2810C",bg="#FDE2BC", font=("Arial", 12, "bold"))
        self.level_label.grid(row=0, column=4, padx=10,pady=10)

        self.timer_label = tk.Label(self.top_frame, text="Time: ", fg="black",bg="#FDE2BC", font=("Arial", 12, "bold"))
        self.timer_label.grid(row=0, column=5, padx=30,pady=10)
        
        # sodoku board
        #middle part
        self.middle_frame = tk.Frame(self.board_frame,bg="#FDE2BC", height=300)
        self.middle_frame.pack(fill="both", expand=True)
        
        self.middle_frame.grid_columnconfigure(0, weight=50)  # Cột trái chiếm 65%
        self.middle_frame.grid_columnconfigure(1, weight=50)  # Cột phải chiếm 35%
        
        #events
        self.buttonVs.bind("<Button-1>", lambda e: self.human_vs_robot())
    
    def human_vs_robot(self):
        # middle left-part
        self.tmp_frame = tk.Frame(self.middle_frame,bg="black",height=350)
        self.tmp_frame.grid(row=0, column=0, sticky="nsw", padx=(20,0))
        
        self.left_middle_frame = tk.Frame(self.tmp_frame,bg="#FDE2BC",height=350)
        self.left_middle_frame.grid(padx=1, pady=1)
        
        self.values_1 = {}
        self.entries_1 = {}
        
        for box_col in range(3):
            for box_row in range(3):
                tmp_frame_2 = tk.Frame(self.left_middle_frame,bg="black")
                tmp_frame_2.grid(column=box_col, row=box_row)
                
                box = ttk.Frame(tmp_frame_2)
                box.grid(padx = 1, pady = 1)
                for cell_col in range(3):
                    for cell_row in range(3):
                        v = tk.StringVar()
                        col = 'ABCDEFGHI'[3*box_col + cell_col]
                        row = '123456789'[3*box_row + cell_row]
                        key = col + row
                        self.values_1[key] = v
                        
                        tmp_frame_3 = tk.Frame(box,bg="#d3d3d3")
                        tmp_frame_3.grid(row=cell_row, column=cell_col)
                        
                        entryPlayer = tk.Entry(
                            tmp_frame_3, 
                            width=2, 
                            font=("Arial", 20), 
                            justify="center", 
                            bg="#fff",
                            borderwidth=0,  # Độ dày viền
                            relief="solid",
                            textvariable=v)
                        entryPlayer.grid(padx=1, pady=1)
                        
                        self.entries_1[key] = entryPlayer
                        entryPlayer.bind("<Button-1>", lambda e, key=key: self.select_entry(key))



        self.tmp_frame = tk.Frame(self.middle_frame,bg="black",height=350)
        self.tmp_frame.grid(row=0, column=1, sticky="nsw")
        
        self.right_middle_frame = tk.Frame(self.tmp_frame,bg="#FDE2BC",height=350)
        self.right_middle_frame.grid(padx=1, pady=1)
        
        self.values_2 = {}
        self.entries_2 = {}
        
        for box_col in range(3):
            for box_row in range(3):
                tmp_frame_2 = tk.Frame(self.right_middle_frame,bg="black")
                tmp_frame_2.grid(column=box_col, row=box_row)
                
                box = ttk.Frame(tmp_frame_2)
                box.grid(padx = 1, pady = 1)
                for cell_col in range(3):
                    for cell_row in range(3):
                        v = tk.StringVar()
                        col = 'ABCDEFGHI'[3*box_col + cell_col]
                        row = '123456789'[3*box_row + cell_row]
                        key = col + row
                        self.values_2[key] = v
                        
                        tmp_frame_3 = tk.Frame(box,bg="#d3d3d3")
                        tmp_frame_3.grid(row=cell_row, column=cell_col)
                        
                        entryPlayer = tk.Entry(
                            tmp_frame_3, 
                            width=2, 
                            font=("Arial", 20), 
                            justify="center", 
                            bg="#fff",
                            borderwidth=0,  # Độ dày viền
                            relief="solid",
                            textvariable=v)

                        
                        entryPlayer.grid(padx=1, pady=1)
                        self.entries_2[key] = entryPlayer

                        #entryPlayer.bind("<Button-1>", lambda e, key=key: self.select_entry(key))

                


        #  bottom right frame
        self.almostbottom_frame = tk.Frame(self.board_frame, height=75,bg="#FDE2BC")
        self.almostbottom_frame.pack(fill="x")
        
        self.spacer = tk.Label(self.almostbottom_frame, width=2, bg="#FDE2BC")
        self.spacer.grid(row=0, column=0,padx=45)
        for i in range(1, 10):
            button = ctk.CTkButton(self.almostbottom_frame, text=str(i), font=("Arial", 20, "bold"),text_color="#C72424", width=45, height=55, fg_color="#F9C57D",corner_radius=5, command=lambda num=i: self.set_value(num))
            button.grid(row=0, column=i, padx=5, pady=5)

        #  bottom right frame

        self.bottom_frame = tk.Frame(self.board_frame, height=75,bg="#FDE2BC")
        self.bottom_frame.pack(fill="x")
        
        self.buttonStart = ctk.CTkButton(self.bottom_frame, text="Start", fg_color="#25980E", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=100, height=40)
        self.buttonStart.grid(row=0, column=0, padx=30)

        
        self.iconUndo = ImageTk.PhotoImage(load_sudoku_img("icons8-undo-30.png"))
        self.btnUndo = ctk.CTkButton(
           self.bottom_frame,
           text="Undo",
           image=self.iconUndo,
           compound="top",
           font=("Arial", 14, "bold"),
           fg_color="#F4CE98",
           text_color="Black",
           width=55, height=35,)
        self.btnUndo.grid(row=0, column=1, padx=(50,10),pady=20)
        self.iconErase = ImageTk.PhotoImage(load_sudoku_img("icons8-erase-30.png"))
        self.btnErase = ctk.CTkButton(
           self.bottom_frame,
           text="Erase",
           image=self.iconErase,
           compound="top",
           font=("Arial", 14, "bold"),
           fg_color="#F4CE98",
           text_color="Black",
           width=55, height=35,)
        self.btnErase.grid(row=0, column=2, padx=15,pady=20)
        
        self.iconPencil = ImageTk.PhotoImage(load_sudoku_img("icons8-pencil-30.png"))
        self.btnPencil = ctk.CTkButton(
           self.bottom_frame,
           text="Pencil",
           image=self.iconPencil,
           compound="top",
           font=("Arial", 14, "bold"),
           fg_color="#F4CE98",
           text_color="Black",
           width=50, height=35,)

        self.btnPencil.grid(row=0, column=3, padx=15,pady=20)
        
        self.iconHint = ImageTk.PhotoImage(load_sudoku_img("icons8-hint-30.png"))
        self.btnHint = ctk.CTkButton(
           self.bottom_frame,
           text="Hint",
           image=self.iconHint,
           compound="top",
           font=("Arial", 14, "bold"),
           fg_color="#F4CE98",
           text_color="Black",
           width=55, height=35,)
        self.btnHint.grid(row=0, column=4, padx=15,pady=20)
        
        self.newGame = ctk.CTkButton(self.bottom_frame, text="New Game", fg_color="#F64444", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=70, height=40)
        self.newGame.grid(row=0, column=5,pady=20, padx=65)
        
    
    def select_entry(self, key):
        """Đánh dấu ô được chọn và các ô liên quan."""
        # Xóa màu của các ô đã được chọn trước đó
        self.clear_highlight()
        print(key);
        # Tô màu cho ô được chọn và các ô liên quan
        col, row = key[0], key[1]
        self.selected_entry = key

        # Tô màu các ô cùng hàng, cột và vùng 3x3
        for k, entry in self.entries_1.items():
            entry_col, entry_row = k[0], k[1]
            same_row = (entry_row == row)
            same_col = (entry_col == col)
            same_box = ((ord(entry_col) - ord('A')) // 3 == (ord(col) - ord('A')) // 3) and ((int(entry_row) - 1) // 3 == (int(row) - 1) // 3)

            if same_row or same_col or same_box:
                entry.config(bg="#efefef")
        
        # Tô màu riêng cho ô được chọn
        self.entries_1[key].config(bg="#c2d9cf")

    def clear_highlight(self):
        """Xóa màu của tất cả các ô để đưa về trạng thái ban đầu."""
        for entry in self.entries_1.values():
            entry.config(bg="white")

    def set_value(self, value):
        """Đặt giá trị vào ô được chọn."""
        if self.selected_entry:
            self.values_1[self.selected_entry].set(value)
            self.selected_entry = None  # Bỏ chọn ô sau khi đặt giá trị
            self.clear_highlight()  # Xóa màu sau khi đặt giá trị
        
    def show_level_buttons(self):
        if self.level_buttons_visible:
            self.easy_button.grid_remove()
            self.middle_button.grid_remove()
            self.hard_button.grid_remove()
        else:  
            self.easy_button = ctk.CTkButton(self.sidebar, text="Easy",fg_color="#F64444", font=("Arial", 14,"bold"),corner_radius=6, width=150)
            self.easy_button.grid(row=2, column=0, padx=30,pady=(0,2))
                        
            self.middle_button = ctk.CTkButton(self.sidebar, text="Middle",fg_color="#F64444", font=("Arial", 14,"bold"),corner_radius=6, width=150)
            self.middle_button.grid(row=3, column=0, padx=30,pady=2)
                        
            self.hard_button = ctk.CTkButton(self.sidebar, text="Hard",fg_color="#F64444", font=("Arial", 14,"bold"),corner_radius=6, width=150)
            self.hard_button.grid(row=4, column=0, padx=30,pady=2)
        self.level_buttons_visible = not self.level_buttons_visible
if __name__ == "__main__":
    root = tk.Tk()
    game = Sodoku(root)
    root.mainloop()
