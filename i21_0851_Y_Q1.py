
#Muhammad Kashif
#I21-0851
#Section Y
#Artificial Intelligence Assignment 2

import time
import resource
import numpy as np
from collections import deque

# Sudoku size
N = 9

def display_grid(grid):
    for i in range(N):
        if i % 3 == 0 and i != 0:
            print('-' * (N*2 + 5))  # horizontal line
        for j in range(N):
            if j % 3 == 0 and j != 0:
                print('|', end=' ')  #vertical line
            print(grid[i][j], end=' ')
        print()

def generate_sudoku():
    # Generate a random Sudoku puzzle
    grid = np.zeros((N, N), dtype=int)
    solve_sudoku(grid)  # Generate a complete puzzle
    remove_numbers(grid, 21)  # Remove numbers to create a puzzle
    return grid

def remove_numbers(grid, num_to_remove):
    # Remove numbers from the grid to create a puzzle
    cells = np.random.choice(N * N, num_to_remove, replace=False)
    for cell in cells:
        row, col = divmod(cell, N)
        grid[row][col] = 0

def is_valid_move(grid, row, col, num):
    # Check if placing num at grid[row][col] is valid
    # Check row and column
    if num in grid[row] or num in grid[:, col]:
        return False

    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    subgrid = grid[start_row:start_row + 3, start_col:start_col + 3]
    if num in subgrid:
        return False

    return True

def solve_sudoku(grid):
    empty_cells = find_empty_cells(grid)
    if not empty_cells:
        return True  # if puzzle solved successful

    # MRV and Degree Heuristic
    empty_cells = sorted(empty_cells, key=lambda x: len(get_valid_moves(grid, x[0], x[1])))

    row, col = empty_cells[0]  # Choose cell with minimum remainng value
    valid_moves = get_valid_moves(grid, row, col)

    # LCV: Sort validd moves based on least constraining value
    valid_moves.sort(key=lambda x: count_least_constraining_values(grid, row, col, x))

    for num in valid_moves:
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            if solve_sudoku(grid):
                return True
            grid[row][col] = 0  # Undo the move if it doesn't lead to a solution
    return False

def find_empty_cells(grid):
    empty_cells = []
    for i in range(N):
        for j in range(N):
            if grid[i][j] == 0:
                empty_cells.append((i, j))
    return empty_cells

def get_valid_moves(grid, row, col):
    valid_moves = []
    for num in range(1, N + 1):
        if is_valid_move(grid, row, col, num):
            valid_moves.append(num)
    return valid_moves

def count_least_constraining_values(grid, row, col, num):
    count = 0
    for i in range(N):
        if i != col and grid[row][i] == 0 and num in get_valid_moves(grid, row, i):
            count += 1
        if i != row and grid[i][col] == 0 and num in get_valid_moves(grid, i, col):
            count += 1
    return count

def arc_consistency(grid):
    queue = deque(find_empty_cells(grid))
    while queue:
        row, col = queue.popleft()
        for num in range(1, N + 1):
            if is_valid_move(grid, row, col, num):
                grid[row][col] = num
                queue.extend(find_empty_cells(grid))

def main():
    # Generate a Sudoku puzzle
    puzzle = generate_sudoku()

    print("Generated Sudoku Puzzle:")
    display_grid(puzzle)

    # Calculate and print time complexity
    start_time = time.time()
    arc_consistency(puzzle)
    solve_sudoku(puzzle)
    end_time = time.time()
    print(f"Time complexity: O(9^(N*N)), where N = {N}, Execution time: {end_time - start_time:.6f} seconds")

    # Calculate and print space complexity
    space_used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # Convert to KB
    print(f"Space complexity: O(1) or O(N), Space used: {space_used:.2f} KB")

    if solve_sudoku(puzzle):
        print("\nSolved Sudoku Puzzle:")
        display_grid(puzzle)
    else:
        print("No solution found for the Sudoku puzzle.")

if __name__ == "__main__":
    main()