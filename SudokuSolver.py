import os

class SudokuSolver:
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def is_valid_move(self, row, col, num):
        # Check if the number is not in the row
        if num in self.puzzle[row]:
            return False

        # Check if the number is not in the column
        if num in [self.puzzle[r][col] for r in range(9)]:
            return False

        # Check if the number is not in the 3x3 grid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.puzzle[r][c] == num:
                    return False

        return True

    def solve(self):
        for row in range(9):
            for col in range(9):
                if self.puzzle[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid_move(row, col, num):
                            self.puzzle[row][col] = num
                            if self.solve():
                                return True
                            self.puzzle[row][col] = 0
                    return False
        return True

    def is_valid_puzzle(self):
        for row in range(9):
            for col in range(9):
                num = self.puzzle[row][col]
                if num != 0:
                    self.puzzle[row][col] = 0
                    if not self.is_valid_move(row, col, num):
                        return False
                    self.puzzle[row][col] = num
        return True

    def print_puzzle(self):
        for row in self.puzzle:
            print(" ".join(str(num) if num != 0 else '.' for num in row))

    @staticmethod
    def load_puzzle(filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File '{filename}' does not exist.")
        with open(filename, 'r') as file:
            lines = file.readlines()
        puzzle = []
        for line in lines:
            row = [int(num) if num != '.' else 0 for num in line.strip().split()]
            puzzle.append(row)
        if len(puzzle) != 9 or any(len(row) != 9 for row in puzzle):
            raise ValueError("Invalid Sudoku puzzle format.")
        return puzzle

    @staticmethod
    def save_puzzle(filename, puzzle):
        with open(filename, 'w') as file:
            for row in puzzle:
                file.write(" ".join(str(num) if num != 0 else '.' for num in row) + "\n")

# Example usage
if __name__ == "__main__":
    filename = "game.txt"

    try:
        puzzle = SudokuSolver.load_puzzle(filename)
        solver = SudokuSolver(puzzle)

        print("Initial Puzzle:")
        solver.print_puzzle()

        if solver.is_valid_puzzle():
            print("\nThe puzzle is valid.")
            if solver.solve():
                print("\nSolved Puzzle:")
                solver.print_puzzle()
                SudokuSolver.save_puzzle("solved_game.txt", solver.puzzle)
                print("\nSolved puzzle saved to 'solved_game.txt'.")
            else:
                print("\nThe puzzle cannot be solved.")
        else:
            print("\nThe puzzle is invalid.")

    except (FileNotFoundError, ValueError) as e:
        print(e)
