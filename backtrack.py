import time

from sudoku import Color

grid3 = [
    [2, 0, 3],
    [1, 0, 0],
    [0, 0, 1],
]

grid4 = [
    [4, 0, 0, 0],
    [0, 2, 0, 4],
    [2, 0, 3, 0],
    [0, 0, 0, 2],
]

grid9 = [
    [0, 0, 0, 0, 0, 0, 6, 8, 0],
    [0, 0, 0, 0, 7, 3, 0, 0, 9],
    [3, 0, 9, 0, 0, 0, 0, 4, 5],
    [4, 9, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 3, 0, 5, 0, 9, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 3, 6],
    [9, 6, 0, 0, 0, 0, 3, 0, 8],
    [7, 0, 0, 6, 8, 0, 0, 0, 0],
    [0, 2, 8, 0, 0, 0, 0, 0, 0],
]

solution = None  # solution grid

# noinspection SpellCheckingInspection
'''pretty print Sudoku grid'''


def print_grid(rows: object, grid_name: str = "", label: str = None, color=Color.reset):
    result = ""
    matrix = ""

    if isinstance(rows, list):
        grid_height = len(rows)
        block_height = int(grid_height ** 0.5)

        if block_height * block_height != grid_height:
            block_height = 0

        for i in range(grid_height):
            matrix += "\t"
            for j in range(grid_height):
                matrix += str(rows[i][j]) + " "
                if block_height > 0 and (j + 1) % block_height == 0:
                    matrix += " "
            matrix += "\n"
            if block_height > 0 and (i + 1) % block_height == 0:
                matrix += "\n"
        if label is None:
            result = color.value + grid_name + "\n" + matrix + Color.reset.value
        else:
            result = color.value + label + "\n" + matrix + Color.reset.value

    print(result)


def copy_grid(grid):
    return [row[:] for row in grid]


def check_rows(grid):
    for row in grid:
        unique_row_values = set()

        for value in row:
            if value == 0:  # skip zeroes
                continue

            if value in unique_row_values:
                return False

            unique_row_values.add(value)

    return True


'''check columns for constraint validity'''


def check_cols(grid):
    grid_height = len(grid)
    cols = [[row[i] for row in grid] for i in range(grid_height)]

    return check_rows(cols)


'''check blocks for constraint validity'''


def check_blocks(grid):
    grid_height = len(grid)
    block_height = int(grid_height ** 0.5)

    # blocks exist for squared grids only
    if block_height * block_height != grid_height:
        return True

    for i in range(block_height):
        for j in range(block_height):
            block = [row[j * block_height:(j + 1) * block_height] for row in
                     grid[i * block_height:(i + 1) * block_height]]
            unique_block_values = set()

            for row in block:
                for value in row:
                    if value == 0:  # skip zeroes
                        continue

                    if value in unique_block_values:
                        return False

                    unique_block_values.add(value)

    return True


'''check solution grid for goal validity'''


def check_solution(grid):
    if grid is None or grid == []:
        return False
    return sum([row.count(0) for row in grid]) == 0


def backtrack(grid, spots, x):
    global solution

    grid_height = len(grid)

    # all spots filled: stop searching
    if len(spots) == 0:
        return

    # another search solved the grid: stop searching
    if solution is not None:
        return

    # set the (i, j) cell to x
    (i, j) = spots[0]
    grid[i][j] = x

    # the grid is invalid: stop searching
    is_grid_valid = check_rows(grid)
    is_grid_valid = is_grid_valid and check_cols(grid)
    is_grid_valid = is_grid_valid and check_blocks(grid)
    if not is_grid_valid:
        return

    # the grid is valid and solved: stop searching
    is_grid_solved = check_solution(grid)
    if is_grid_solved:
        solution = grid
        return

    # here, the grid is valid but not solved: continue searching
    for x in range(1, grid_height + 1):
        backtrack(copy_grid(grid), spots[1:], x)


def solve(grid, name: str = ""):
    global solution

    start = time.time()

    # list all spots
    spots = []
    grid_height = len(grid)
    for i in range(grid_height):
        for j in range(grid_height):
            if grid[i][j] == 0:
                spots.append((i, j))

    # backtrack grid
    for x in range(1, grid_height + 1):
        backtrack(copy_grid(grid), spots, x)

    color = Color.red
    if check_solution(solution):
        color = Color.green
    if solution is not None:
        print_grid(solution, grid_name=name, color=color)
        solution = None
    else:
        print(color.value + f"{name}: Issues with grid" + Color.reset.value)

    stop = time.time()
    print(f"Single puzzle lapse == {round((stop - start) * 1000, 1)} ms")


if __name__ == '__main__':
    solve(grid9)
