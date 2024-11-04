import tkinter as tk
import random
from tkinter import messagebox
from collections import deque

class FifteenPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Game")
        self.root.configure(bg="yellow")
        
        self.size = 3
        self.grid = [[i + j * self.size for i in range(self.size)] for j in range(self.size)]
        self.goal = self.randomize_goal_state()
        self.shuffle_grid()

        self.counter = tk.Frame(self.root)
        self.puzzle_frame = tk.Frame(self.root, bg="yellow")
        self.puzzle_frame.grid(row=0, column=0, padx=10, pady=10)

        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j] = tk.Button(self.puzzle_frame, text=str(self.grid[i][j]) if self.grid[i][j] != 0 else "", 
                                               font=('Helvetica', 18), width=6, height=3, 
                                               bg="#DEB887", fg="black", borderwidth=2)
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

        self.goal_frame = tk.Frame(self.root, bg="gray", relief=tk.SUNKEN, borderwidth=2)
        self.goal_frame.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.goal_frame, text="Goal State", font=('Helvetica', 18), bg="gray", fg="dark green").grid(row=0, column=0, columnspan=self.size)

        self.goal_buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                self.goal_buttons[i][j] = tk.Button(self.goal_frame, text=str(self.goal[i][j]) if self.goal[i][j] != 0 else "", 
                                                    font=('Helvetica', 18), width=6, height=3, 
                                                    bg="white", fg="black", borderwidth=2)
                self.goal_buttons[i][j].grid(row=i+1, column=j, padx=2, pady=2)

        self.root.bind("<Up>", lambda event: self.move('up'))
        self.root.bind("<Down>", lambda event: self.move('down'))
        self.root.bind("<Left>", lambda event: self.move('left'))
        self.root.bind("<Right>", lambda event: self.move('right'))

        self.update_buttons()

        # Button to start auto-solve
        self.solve_button = tk.Button(self.root, text="Auto Solve", command=self.solve_puzzle, font=('Helvetica', 14), bg="lightblue")
        self.solve_button.grid(row=1, column=0, pady=10)

    def randomize_goal_state(self):
        numbers = [i for i in range(self.size * self.size)]
        random.shuffle(numbers)
        goal = [numbers[i:i+self.size] for i in range(0, self.size * self.size, self.size)]
        while not self.is_solvable(goal):
            random.shuffle(numbers)
            goal = [numbers[i:i+self.size] for i in range(0, self.size * self.size, self.size)]
        return goal

    def shuffle_grid(self):
        numbers = [i for i in range(self.size * self.size)]
        random.shuffle(numbers)
        self.grid = [numbers[i:i+self.size] for i in range(0, self.size * self.size, self.size)]
        while not self.is_solvable(self.grid) or self.grid == self.goal:
            random.shuffle(numbers)
            self.grid = [numbers[i:i+self.size] for i in range(0, self.size * self.size, self.size)]

    def find_empty(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return i, j

    def move(self, direction):
        x, y = self.find_empty()
        if direction == 'up' and x < self.size - 1:
            self.grid[x][y], self.grid[x+1][y] = self.grid[x+1][y], self.grid[x][y]
        elif direction == 'down' and x > 0:
            self.grid[x][y], self.grid[x-1][y] = self.grid[x-1][y], self.grid[x][y]
        elif direction == 'left' and y < self.size - 1:
            self.grid[x][y], self.grid[x][y+1] = self.grid[x][y+1], self.grid[x][y]
        elif direction == 'right' and y > 0:
            self.grid[x][y], self.grid[x][y-1] = self.grid[x][y-1], self.grid[x][y]
        else:
            return  # Invalid move, do nothing

        self.update_buttons()
        if self.check_goal():
            self.show_win_message()

    def update_buttons(self):
        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j].config(text=str(self.grid[i][j]) if self.grid[i][j] != 0 else "")

    def check_goal(self):
        return self.grid == self.goal

    def is_solvable(self, state):
        one_d = [num for row in state for num in row if num != 0]
        inversions = 0
        for i in range(len(one_d)):
            for j in range(i + 1, len(one_d)):
                if one_d[i] > one_d[j]:
                    inversions += 1
        return inversions % 2 == 0

    def show_win_message(self):
        messagebox.showinfo("8-Puzzle", "Congratulations! You solved the puzzle!")
        self.root.quit()

    def solve_puzzle(self):
        start_state = tuple(tuple(row) for row in self.grid)
        goal_state = tuple(tuple(row) for row in self.goal)
        queue = deque([(start_state, [])])  # (current_state, path_to_state)
        visited = set()
        visited.add(start_state)

        while queue:
            current_state, path = queue.popleft()

            if current_state == goal_state:
                self.execute_solution(path)
                return

            x, y = self.find_empty_in_state(current_state)

            for direction in ['up', 'down', 'left', 'right']:
                new_state = self.make_move(current_state, x, y, direction)
                if new_state and new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, path + [direction]))

    def find_empty_in_state(self, state):
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == 0:
                    return i, j

    def make_move(self, state, x, y, direction):
        new_state = [list(row) for row in state]  # Create a copy of the state
        if direction == 'up' and x < self.size - 1:
            new_state[x][y], new_state[x+1][y] = new_state[x+1][y], new_state[x][y]
        elif direction == 'down' and x > 0:
            new_state[x][y], new_state[x-1][y] = new_state[x-1][y], new_state[x][y]
        elif direction == 'left' and y < self.size - 1:
            new_state[x][y], new_state[x][y+1] = new_state[x][y+1], new_state[x][y]
        elif direction == 'right' and y > 0:
            new_state[x][y], new_state[x][y-1] = new_state[x][y-1], new_state[x][y]
        else:
            return None
        return tuple(tuple(row) for row in new_state)

    def execute_solution(self, path):
        for direction in path:
            self.move(direction)
            self.root.update()  # Update the GUI after each move
            self.root.after(500)  # Pause for half a second before the next move

# Initialize the Tkinter root
root = tk.Tk()
game = FifteenPuzzle(root)
root.mainloop()
