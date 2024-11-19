import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import os

            
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
                    
def load_sudoku_img(file) :
    base_dir = os.path.dirname(__file__)
    
    # Đường dẫn đến file ảnh trong thư mục `sudoku`
    image_path = os.path.join(base_dir, "../sudoku", file)  # Thay "your_image.png" bằng tên file thực tế
    # Mở ảnh bằng PIL
    return Image.open(image_path)



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
    
