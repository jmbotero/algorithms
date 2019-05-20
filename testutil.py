from pathlib import Path

from backtrack import *
from sudoku import Color
from sudoku import Sudoku
from sudoku import SudokuSolution


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent


def __puzzle1():
    p = Sudoku("Lesson 1",
               [[4, 7, 8, 3, 0, 9, 1, 2, 0],
                [0, 0, 9, 1, 2, 8, 7, 5, 4],
                [2, 5, 1, 0, 7, 0, 3, 0, 8],
                [3, 0, 4, 7, 8, 2, 9, 0, 5],
                [9, 0, 0, 6, 3, 0, 2, 4, 0],
                [7, 1, 2, 9, 0, 5, 8, 6, 0],
                [8, 2, 6, 0, 9, 0, 4, 7, 1],
                [0, 4, 3, 0, 6, 7, 0, 0, 9],
                [5, 0, 0, 8, 1, 4, 0, 3, 2]])

    return p


def __puzzle2():
    p = Sudoku("Lesson 2",
               [[2, 0, 0, 0, 7, 0, 9, 4, 0],
                [0, 3, 0, 6, 0, 2, 8, 0, 0],
                [1, 6, 0, 0, 0, 9, 7, 0, 2],
                [4, 1, 0, 5, 0, 0, 6, 0, 3],
                [0, 0, 7, 3, 2, 0, 0, 0, 0],
                [3, 5, 0, 4, 0, 6, 1, 0, 9],
                [9, 0, 1, 0, 0, 0, 3, 8, 4],
                [0, 0, 0, 0, 1, 8, 0, 6, 7],
                [0, 0, 6, 7, 0, 4, 5, 0, 1]])
    return p


def __puzzle3():
    p = Sudoku("Lesson 4",
               [[0, 0, 3, 9, 0, 0, 1, 7, 6],
                [0, 0, 4, 0, 0, 6, 5, 3, 0],
                [6, 7, 0, 1, 5, 0, 0, 4, 0],
                [0, 8, 0, 3, 2, 0, 0, 0, 0],
                [9, 4, 0, 0, 1, 0, 0, 2, 3],
                [0, 0, 1, 0, 7, 8, 0, 5, 9],
                [0, 1, 0, 0, 9, 4, 0, 0, 5],
                [0, 6, 9, 0, 0, 0, 4, 0, 0],
                [4, 0, 5, 0, 6, 7, 2, 0, 1]])
    return p


def __puzzle4():
    p = Sudoku("Lesson H")
    p.createemptyboard()
    p.setmatrixvalue(0, 1, 7, True)
    p.setmatrixvalue(0, 3, 2, True)
    p.setmatrixvalue(0, 4, 5, True)
    p.setmatrixvalue(0, 6, 4, True)
    p.setmatrixvalue(1, 0, 8, True)
    p.setmatrixvalue(1, 6, 9, True)
    p.setmatrixvalue(1, 8, 3, True)
    p.setmatrixvalue(2, 5, 3, True)
    p.setmatrixvalue(2, 7, 7, True)
    p.setmatrixvalue(3, 0, 7, True)
    p.setmatrixvalue(3, 5, 4, True)
    p.setmatrixvalue(3, 7, 2, True)
    p.setmatrixvalue(4, 0, 1, True)
    p.setmatrixvalue(4, 7, 4, True)
    p.setmatrixvalue(4, 8, 7, True)
    p.setmatrixvalue(5, 0, 4, True)
    p.setmatrixvalue(5, 6, 5, True)
    p.setmatrixvalue(5, 8, 8, True)
    p.setmatrixvalue(6, 1, 9, True)
    p.setmatrixvalue(6, 3, 6, True)
    p.setmatrixvalue(6, 5, 5, True)
    p.setmatrixvalue(7, 0, 4, True)
    p.setmatrixvalue(7, 2, 1, True)
    p.setmatrixvalue(7, 8, 5, True)
    p.setmatrixvalue(8, 2, 7, True)
    p.setmatrixvalue(8, 4, 8, True)
    p.setmatrixvalue(8, 5, 2, True)
    p.setmatrixvalue(8, 7, 3, True)

    return p


# noinspection SpellCheckingInspection
def loadpuzzles(filename, puzzlename=""):
    puzzle = None
    puzzles = []
    row = []
    rows = []
    name = ""
    processpuzzle = puzzlename == ""

    path = get_project_root()
    filename = f"{path}/data/{filename}"
    file = open(filename, encoding="utf-8-sig")  # use default mode='r' for utf8
    line = file.readline().strip()
    while line:
        if line.isnumeric():
            if processpuzzle:
                for c in line:
                    row.append(int(c))
                rows.append(row)
                row = []
        else:
            if puzzlename != "" and rows:
                puzzle = Sudoku(puzzlename, rows)
                rows = []
            elif name != "" and rows:
                puzzle = Sudoku(name, rows)
                rows = []
            else:
                puzzle = None

            name = line

            if puzzle is not None:
                puzzles.append(puzzle)
            if puzzlename != "":
                processpuzzle = name == puzzlename
        line = file.readline().strip()

    if name != "" and rows:  # add the last one
        puzzle = Sudoku(name, rows)
        puzzles.append(puzzle)

    file.close()

    if puzzlename == "":
        return puzzles
    else:
        return puzzles[0]


# noinspection SpellCheckingInspection
def loadpuzzlebyname(puzzlename, filename):
    return loadpuzzles(filename, puzzlename)

# noinspection SpellCheckingInspection
def __solve(puzzle):
    loop = 1
    previousloopemptycount = puzzle.emptycellcount
    print(puzzle.tostring(), end="")

    changes = False
    while not puzzle.ismatrixcomplete:
        puzzle.completehorizontalblocksemptycells()
        changes = changes or puzzle.haschanged
        puzzle.completeverticalblocksemptycells()
        changes = changes or puzzle.haschanged
        puzzle.completehorizontalblocksemptycells()
        changes = changes or puzzle.haschanged
        puzzle.completeverticalblocksemptycells()
        changes = changes or puzzle.haschanged
        puzzle.completehorizontalblocksemptycells()
        changes = changes or puzzle.haschanged
        puzzle.completesingleemptycellssections()
        changes = changes or puzzle.haschanged
        puzzle.completedoubleemptycellssections()
        changes = changes or puzzle.haschanged
        puzzle.completehorizontalblocksemptycells()
        changes = changes or puzzle.haschanged
        puzzle.completesingleemptycellssections()
        changes = changes or puzzle.haschanged
        puzzle.completehorizontalblocksemptycells()
        changes = changes or puzzle.haschanged
        puzzle.completeverticalblocksemptycells()
        changes = changes or puzzle.haschanged
        puzzle.completesingleemptycellssections()
        changes = changes or puzzle.haschanged

        # puzzle.completesingleemptycellssections()
        # changes = changes or puzzle.haschanged
        # puzzle.completedoubleemptycellssections()
        # changes = changes or puzzle.haschanged
        # puzzle.completeemptycellswithnotcontainedvalues()
        # changes = changes or puzzle.haschanged

        if not changes or previousloopemptycount == puzzle.emptycellcount:
            break

        if puzzle.emptycellcount != previousloopemptycount:
            previousloopemptycount = puzzle.emptycellcount

        loop += 1

    color = Color.red
    if puzzle.ismatrixcomplete:
        color = Color.green

    print(puzzle.tostring(f"Solution ({loop})", color), end="")
    print(f"Empty cell count = {puzzle.emptycellcount}", end="\n")


def __solve_backtrack(puzzle):
    # list all spots
    l: int = len(puzzle)
    spots = []
    for i in range(l):
        for j in range(l):
            if puzzle[i][j] == 0:
                spots.append((i, j))

    # solve grid
    s = None
    x = 0
    while 1:
        if x == l:
            x = 0

        if s is None:
            s = solve(copy_grid(puzzle), spots, x + 1)
        if s is not None:
            break
        else:
            x += 1
    if s is not None:
        print_grid(s)


# noinspection SpellCheckingInspection
def __main_singlepuzzle():
    mypuzzle = loadpuzzlebyname("Lesson 3x3", "board_sudoku_2.txt")

    __solve_backtrack(mypuzzle.rows)


# noinspection SpellCheckingInspection
def __main():
    games = loadpuzzles("board_sudoku_2.txt")  # [__puzzle1(), __puzzle2(), __puzzle3(), __puzzle4()]
    # games = loadpuzzles("board_sudoku_1.txt")

    solutions = []
    for game in games:
        solution = SudokuSolution(game.boardname, game.rows, game.columns, game.tostring(""))
        __solve(game)
        solution.logsolution(game.tostring(""), game.ismatrixcomplete)
        solutions.append((game.emptycellcount, solution))
    games = None

if __name__ == "__main__":
    x = input("Which test utility (1/2)? ")
    if x == "1":
        __main()
    elif x == "2":
        __main_singlepuzzle()
