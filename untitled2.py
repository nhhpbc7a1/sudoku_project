import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
import random
import time  # Thêm thư viện time để tính toán thời gian
from tkinter import messagebox
from collections import deque

class Sodoku:
    def __init__(self, root):
        self.root = root
        self.root.title("Sodoku")
        self.root.geometry("950x550")
        self.root.configure(bg="#FDE2BC")
        
        
        self.sidebar = tk.Frame(self.root, bg="#D2691E", width=250, height=550)
        self.sidebar.pack(side="left", fill="y")
        
        image_path = "D:\Thirdyear_Semester01\AI\Sodoku\icons8-sudoku-100.png"
        image = Image.open(image_path)
        tk_image = ImageTk.PhotoImage(image)
        
        self.logo_label = tk.Label(self.sidebar, image=tk_image,  bg="#D2691E",width=180,height=150)
        self.logo_label.image = tk_image  # Giữ tham chiếu để tránh bị garbage collected
        self.logo_label.pack(pady=1)

        
        self.buttonSingle = ctk.CTkButton(self.sidebar, text="Single Player", fg_color="#C72424", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=150, height=40)
        self.buttonSingle.pack(pady=10)
        
        self.buttonVs = ctk.CTkButton(self.sidebar, text="Machine vs Player", fg_color="#C72424", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=150, height=40)
        self.buttonVs.pack(pady=10)
        
        self.buttonMachine = ctk.CTkButton(self.sidebar, text="Machine mode", fg_color="#C72424", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=150, height=40)
        self.buttonMachine.pack(pady=10)
        
        self.buttonExit = ctk.CTkButton(self.sidebar, text="Exit", fg_color="#C72424", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=150, height=40)
        self.buttonExit.pack(pady=10)

        
        #Right part
        
        self.board_frame = tk.Frame(self.root,bg="#FDE2BC")
        self.board_frame.pack(side="right", fill="both", expand=True)
        
        # top-right part
        self.top_frame = tk.Frame(self.board_frame, bg="#FDE2BC", height=50)
        self.top_frame.pack(fill="x")
        # top-right part
        self.mistakes_label = tk.Label(self.top_frame, text="Mistakes:", fg="black",bg="#FDE2BC", font=("Arial", 12))
        self.mistakes_label.grid(row=0, column=0, padx=30,pady=5)
        
        self.level_label = tk.Label(self.top_frame, text="Easy", fg="#E2810C",bg="#FDE2BC", font=("Arial", 12, "bold"))
        self.level_label.grid(row=0, column=1, padx=40,pady=5)

        self.timer_label = tk.Label(self.top_frame, text="Time: ", fg="black",bg="#FDE2BC", font=("Arial", 12))
        self.timer_label.grid(row=0, column=2, padx=30,pady=5)
        
        self.newGame = ctk.CTkButton(self.top_frame, text="New Game", fg_color="#F64444", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=75, height=40)
        self.newGame.grid(row=0, column=3,padx=280,pady=(15,10))

        # sodoku board
        #middle part
        self.middle_frame = tk.Frame(self.board_frame,bg="#FDE2BC", height=350)
        self.middle_frame.pack(fill="both", expand=True)
        
        self.middle_frame.grid_columnconfigure(0, weight=85)  # Cột trái chiếm 65%
        self.middle_frame.grid_columnconfigure(1, weight=5)  # Cột phải chiếm 35%

        # middle left-part
        
        self.left_middle_frame = tk.Frame(self.middle_frame, bg="#FDE2BC",height=350)
        self.left_middle_frame.grid(row=0, column=0, sticky="nsew")
        
        #  middle right-part
        self.right_middle_frame = tk.Frame(self.middle_frame,bg="#FDE2BC",height=350)
        self.right_middle_frame.grid(row=0, column=1, sticky="nsew")
        
        self.spacer = tk.Label(self.right_middle_frame, bg="#FDE2BC")
        self.spacer.grid(row=1, column=1, padx=40)


        for i in range(1, 10):
            button = ctk.CTkButton(self.right_middle_frame, text=str(i), font=("Arial", 32, "bold"),text_color="#C72424", width=60, height=65, fg_color="#F9C57D",corner_radius=5, command=lambda num=i: self.select_number(num))
            button.grid(row=(i-1)//3, column=(i-1)%3, padx=20, pady=20)


        self.bottom_frame = tk.Frame(self.board_frame, height=150,bg="#FDE2BC")
        self.bottom_frame.pack(fill="x")
        
        self.buttonStart = ctk.CTkButton(self.bottom_frame, text="Start", fg_color="#25980E", text_color="white",font=("Arial", 14, "bold"), corner_radius=6,width=100, height=40)
        self.buttonStart.grid( padx= 150,pady=35)

if __name__ == "__main__":
    root = tk.Tk()
    game = Sodoku(root)
    root.mainloop()
