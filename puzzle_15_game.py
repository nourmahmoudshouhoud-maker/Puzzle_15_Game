import heapq
import random
import tkinter as tk
from tkinter import messagebox
import copy

class Puzzle15:
    def __init__(self, board=None):
        self.size = 4
        self.board = board if board else self.generate_board()
        self.goal = [[(i * self.size + j) % (self.size ** 2) for j in range(self.size)] for i in range(self.size)]

    def generate_board(self):
        tiles = list(range(16))
        random.shuffle(tiles)
        return [tiles[i:i+4] for i in range(0, 16, 4)]

    def get_empty_pos(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return i, j

    def get_neighbors(self):
        i, j = self.get_empty_pos()
        moves = []
        directions = {'Up': (i - 1, j), 'Down': (i + 1, j), 'Left': (i, j - 1), 'Right': (i, j + 1)}
        for move, (x, y) in directions.items():
            if 0 <= x < 4 and 0 <= y < 4:
                new_board = copy.deepcopy(self.board)
                new_board[i][j], new_board[x][y] = new_board[x][y], new_board[i][j]
                moves.append((move, new_board))
        return moves

    def is_goal(self):
        return self.board == self.goal

class Heuristic:
    def __init__(self, goal_state=None):
        if goal_state is None:
            self.goal_state = [
                [0, 1, 2, 3],
                [4, 5, 6, 7],
                [8, 9, 10, 11],
                [12, 13, 14, 15]
            ]
        else:
            self.goal_state = goal_state
        self.goal_positions = self._get_goal_positions()

    def _get_goal_positions(self):
        positions = {}
        for i in range(4):
            for j in range(4):
                tile = self.goal_state[i][j]
                positions[tile] = (i, j)
        return positions

    def manhattan_distance(self, current_state):
        distance = 0
        for i in range(4):
            for j in range(4):
                tile = current_state[i][j]
                if tile != 0:
                    goal_i, goal_j = self.goal_positions[tile]
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance

class PuzzleSolver:
    def __init__(self, start_state):
        self.start_state = start_state
        self.heuristic = Heuristic()
        self.goal_state = self.heuristic.goal_state

    def find_empty(self, state):
        for i in range(4):
            for j in range(4):
                if state[i][j] == 0:
                    return (i, j)

    def get_neighbors(self, state):
        neighbors = []
        x, y = self.find_empty(state)
        moves = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]
        for dx, dy, move_name in moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 4 and 0 <= new_y < 4:
                new_state = copy.deepcopy(state)
                new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
                neighbors.append((new_state, move_name))
        return neighbors

    def is_goal(self, state):
        return state == self.goal_state

    def serialize(self, state):
        return str(state)

    def solve(self):
        heap = []
        visited = set()
        h = self.heuristic.manhattan_distance(self.start_state)
        heapq.heappush(heap, (h, 0, self.start_state, []))

        while heap:
            f, g, current, path = heapq.heappop(heap)

            if self.is_goal(current):
                return path

            serialized = self.serialize(current)
            if serialized in visited:
                continue
            visited.add(serialized)

            for neighbor, move_name in self.get_neighbors(current):
                if self.serialize(neighbor) not in visited:
                    new_g = g + 1
                    new_h = self.heuristic.manhattan_distance(neighbor)
                    new_f = new_g + new_h
                    heapq.heappush(heap, (new_f, new_g, neighbor, path + [move_name]))

        return None

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("15 Puzzle Solver")
        self.root.configure(bg='black')

        self.puzzle = Puzzle15()
        self.buttons = []

        title = tk.Label(self.root, text="15 Puzzle Solver", font=("Helvetica", 20, "bold"),
                         fg='white', bg='black', pady=10)
        title.pack()

        self.frame = tk.Frame(root, bg='black')
        self.frame.pack(pady=10)

        self.update_board()

        self.button_frame = tk.Frame(self.root, bg='black')
        self.button_frame.pack(pady=10)

        self.solve_button = tk.Button(self.button_frame, text="Solve", command=self.solve_puzzle,
                                      bg='white', fg='black', font=("Helvetica", 14), width=10)
        self.solve_button.grid(row=0, column=0, padx=10)

        self.shuffle_button = tk.Button(self.button_frame, text="Shuffle", command=self.shuffle_board,
                                        bg='white', fg='black', font=("Helvetica", 14), width=10)
        self.shuffle_button.grid(row=0, column=1, padx=10)

    def update_board(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.buttons = []
        for i in range(4):
            for j in range(4):
                tile_value = self.puzzle.board[i][j]
                tile_text = str(tile_value)
                btn = tk.Button(self.frame, text=tile_text, width=6, height=3,
                                font=("Helvetica", 16, "bold"), relief='ridge', bd=2,
                                command=lambda row=i, col=j: self.move_tile(row, col),
                                bg='white', fg='black')
                btn.grid(row=i, column=j, padx=2, pady=2)
                self.buttons.append(btn)

    def shuffle_board(self):
        self.puzzle.board = self.puzzle.generate_board()
        self.update_board()

    def move_tile(self, row, col):
        empty_row, empty_col = self.puzzle.get_empty_pos()
        if (abs(empty_row - row) == 1 and empty_col == col) or (abs(empty_col - col) == 1 and empty_row == row):
            self.puzzle.board[empty_row][empty_col], self.puzzle.board[row][col] = \
                self.puzzle.board[row][col], self.puzzle.board[empty_row][empty_col]
            self.update_board()

    def solve_puzzle(self):
        self.solve_button.config(state="disabled")
        solver = PuzzleSolver(self.puzzle.board)
        moves = solver.solve()

        if moves:
            self.animate_solution(moves)
        else:
            messagebox.showinfo("No Solution", "This puzzle is unsolvable.")
            self.solve_button.config(state="normal")

    def animate_solution(self, moves, index=0):
        if index >= len(moves):
            self.solve_button.config(state="normal")
            return

        move = moves[index]
        empty_row, empty_col = self.puzzle.get_empty_pos()
        if move == "Up":
            new_row, new_col = empty_row - 1, empty_col
        elif move == "Down":
            new_row, new_col = empty_row + 1, empty_col
        elif move == "Left":
            new_row, new_col = empty_row, empty_col - 1
        elif move == "Right":
            new_row, new_col = empty_row, empty_col + 1

        self.puzzle.board[empty_row][empty_col], self.puzzle.board[new_row][new_col] = \
            self.puzzle.board[new_row][new_col], self.puzzle.board[empty_row][empty_col]

        self.update_board()
        self.root.after(300, lambda: self.animate_solution(moves, index + 1))

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()
