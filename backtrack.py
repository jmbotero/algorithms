#!/usr/bin/python3

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
    [0, 7, 0, 2, 5, 0, 4, 0, 0],
    [8, 0, 0, 0, 0, 0, 9, 0, 3],
    [0, 0, 0, 0, 0, 3, 0, 7, 0],
    [7, 0, 0, 0, 0, 4, 0, 2, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 7],
    [0, 4, 0, 5, 0, 0, 0, 0, 8],
    [0, 9, 0, 6, 0, 0, 0, 0, 0],
    [4, 0, 1, 0, 0, 0, 0, 0, 5],
    [0, 0, 7, 0, 8, 2, 0, 3, 0]
]
solution = None  # solution grid

# noinspection SpellCheckingInspection
'''pretty print Sudoku grid'''


def print_grid(rows):
    if rows is not None:
        for row in rows:
            print(' '.join([str(x) for x in row if x != 0]))


def copy_grid(rows):
    result = [row[:] for row in rows]
    return result


'''check rows for constraint validity'''


def check_rows(rows):
    for row in rows:
        xs = set()

        for x in row:
            if x == 0:
                continue

            if x in xs:
                return False

            xs.add(x)

    return True


'''check columns for constraint validity'''


def check_cols(rows):
    cols = [[row[i] for row in rows] for i in range(n)]

    return check_rows(cols)


'''check sub-grids for constraint validity'''


def check_sub_grids(rows):
    m = int(n ** 0.5)

    # sub-grids exist for squared grids only
    if m * m != n:
        return True

    for i in range(m):
        for j in range(m):
            sub_grid = [row[j * m:(j + 1) * m] for row in rows[i * m:(i + 1) * m]]
            xs = set()

            for row in sub_grid:
                for x in row:
                    if x == 0:
                        continue

                    if x in xs:
                        return False

                    xs.add(x)

    return True


'''check solution grid for goal validity'''


def check_solution(rows):
    return sum([row.count(0) for row in rows]) == 0


def solve(rows, spots, x):
    global solution
    global n

    n = len(rows)
    solution = []

    # all spots filled: stop searching
    if len(spots) == 0:
        return None

    # another search solved the grid: stop searching
    if solution is not None:
        return solution

    # set the (i, j) cell to x
    (i, j) = spots[0]
    rows[i][j] = x

    # the grid is invalid: stop searching
    is_grid_valid = check_rows(rows) and check_cols(rows) and check_sub_grids(rows)
    if not is_grid_valid:
        return None

    # the grid is valid and solved: stop searching
    is_grid_solved = check_solution(rows)
    if is_grid_solved:
        solution = copy_grid(rows)
        return rows

    # here, the grid is valid but not solved: continue searching
    for x in range(n):
        spots1 = spots[1:]  # clone `spots` array starting from 1st index
        solve(copy_grid(rows), spots1, x + 1)


def main():
    # list all spots
    spots = []
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                spots.append((i, j))

    # solve grid
    for x in range(n):
        solve(copy_grid(grid), spots, x + 1)

    print_grid(solution)


if __name__ == '__main__':
    grid = grid9
    n = len(grid)
    main()
