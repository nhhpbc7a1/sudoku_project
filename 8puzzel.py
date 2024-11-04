import tkinter as tk
import random
from tkinter import messagebox

class FifteenPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Game")
        self.root.configure(bg="yellow")
        
        self.counter = tk.Frame(self.root, )
        
        # Initialize the puzzle grid and randomize the goal state
        self.size = 3
        self.grid = [[i + j * self.size for i in range(self.size)] for j in range(self.size)]
        self.goal = self.randomize_goal_state()
        self.shuffle_grid()
        
        # Create a frame to hold the puzzle buttons
        self.puzzle_frame = tk.Frame(self.root, bg="yellow")
        self.puzzle_frame.grid(row=0, column=0, padx=10, pady=10)

        # Create buttons for each cell in the puzzle grid
        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j] = tk.Button(self.puzzle_frame, text=str(self.grid[i][j]) if self.grid[i][j] != 0 else "", 
                                               font=('Helvetica', 18), width=6, height=3, 
                                               bg="#DEB887", fg="black", borderwidth=2)
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

        # Create a frame to display the goal state
        self.goal_frame = tk.Frame(self.root, bg="gray", relief=tk.SUNKEN, borderwidth=2)
        self.goal_frame.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.goal_frame, text="Goal State", font=('Helvetica', 18), bg="gray", fg="dark green").grid(row=0, column=0, columnspan=self.size)

        # Display the goal state in the goal frame
        self.goal_buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                self.goal_buttons[i][j] = tk.Button(self.goal_frame, text=str(self.goal[i][j]) if self.goal[i][j] != 0 else "", 
                                                    font=('Helvetica', 18), width=6, height=3, 
                                                    bg="white", fg="black", borderwidth=2)
                self.goal_buttons[i][j].grid(row=i+1, column=j, padx=2, pady=2)

        # Bind arrow keys to movement
        self.root.bind("<Up>", lambda event: self.move('up'))
        self.root.bind("<Down>", lambda event: self.move('down'))
        self.root.bind("<Left>", lambda event: self.move('left'))
        self.root.bind("<Right>", lambda event: self.move('right'))

        self.update_buttons()

    def randomize_goal_state(self):
        # Create a randomized goal state that is solvable
        numbers = [i for i in range(self.size * self.size)]
        random.shuffle(numbers)
        goal = [numbers[i:i+self.size] for i in range(0, self.size * self.size, self.size)]
        while not self.is_solvable(goal):
            random.shuffle(numbers)
            goal = [numbers[i:i+self.size] for i in range(0, self.size * self.size, self.size)]
        return goal

    def shuffle_grid(self):
        # Flatten and shuffle the grid
        numbers = [i for i in range(self.size * self.size)]
        random.shuffle(numbers)
        self.grid = [numbers[i:i+self.size] for i in range(0, self.size * self.size, self.size)]
        # Ensure it's solvable and not already solved
        while not self.is_solvable(self.grid) or self.grid == self.goal:
            random.shuffle(numbers)
            self.grid = [numbers[i:i+self.size] for i in range(0, self.size * self.size, self.size)]

    def find_empty(self):
        # Locate the empty space (0)
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
        # Check if the current grid matches the goal state
        return self.grid == self.goal

    def is_solvable(self, state):
        # Convert grid to a 1D list
        one_d = [num for row in state for num in row if num != 0]
        # Count inversions
        inversions = 0
        for i in range(len(one_d)):
            for j in range(i + 1, len(one_d)):
                if one_d[i] > one_d[j]:
                    inversions += 1
        # For a 4x4 puzzle, the number of inversions must be even
        return inversions % 2 == 0

    def show_win_message(self):
        messagebox.showinfo("8-Puzzle", "Congratulations! You solved the puzzle!")
        self.root.quit()

# Initialize the Tkinter root
root = tk.Tk()
game = FifteenPuzzle(root)
root.mainloop()
