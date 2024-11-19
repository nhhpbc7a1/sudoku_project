import tkinter as tk
from tkinter import ttk

def create_board(self, frame):
    for box_col in range(self.game_size):
        for box_row in range(self.game_size):
            tmp_frame_2 = tk.Frame(frame, bg="black")
            tmp_frame_2.grid(column=box_col, row=box_row)

            box = ttk.Frame(tmp_frame_2)
            box.grid(padx=1, pady=1)
            for cell_col in range(self.game_size):
                for cell_row in range(self.game_size):
                    v = tk.StringVar()
                    col = '123456789'[3 * box_col + cell_col]
                    row = '123456789'[3 * box_row + cell_row]
                    key = col + row
                    self.values[key] = v

                    entryPlayer = tk.Canvas(
                        box, width=33, height=33, bg="#fff", highlightthickness=1, highlightbackground="lightgray"
                    )
                    entryPlayer.grid(row=cell_row, column=cell_col)

                    self.entries[key] = entryPlayer
                    entryPlayer.bind("<Button-1>", lambda e, key=key: self.select_entry(key))


def create_robot_board(self, frame, algorithm_name):
    for box_col in range(self.game_size):
        for box_row in range(self.game_size):
            tmp_frame_2 = tk.Frame(frame, bg="black")
            tmp_frame_2.grid(column=box_col, row=box_row)

            box = ttk.Frame(tmp_frame_2)
            box.grid(padx=1, pady=1)
            for cell_col in range(self.game_size):
                for cell_row in range(self.game_size):
                    v = tk.StringVar()
                    col = '123456789'[3 * box_col + cell_col]
                    row = '123456789'[3 * box_row + cell_row]
                    key = col + row
                    self.robot1_values[key] = v

                    entryPlayer = tk.Canvas(
                        box, width=33, height=33, bg="#fff", highlightthickness=1, highlightbackground="lightgray"
                    )
                    entryPlayer.grid(row=cell_row, column=cell_col)

                    self.robot1_entries[key] = entryPlayer
