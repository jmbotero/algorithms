from pathlib import Path

from backtrack import *
from sudoku import Color
from sudoku import Sudoku
from sudoku import SudokuSolution


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent


# noinspection SpellCheckingInspection
def loadpuzzles(filename, puzzlename=""):
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
    mygrid = puzzle.rows

    # list all spots
    l: int = len(mygrid)
    spots = []
    for i in range(l):
        for j in range(l):
            if mygrid[i][j] == 0:
                spots.append((i, j))

    # solve grid
    s = None
    value = 0
    while 1:
        if value == l:
            value = 0

        if s is None:
            s = solve(copy_grid(mygrid), spots, value + 1)
        if s is not None:
            break
        else:
            value += 1
    if s is not None:
        print_grid(s)

    color = Color.red
    if mygrid.ismatrixcomplete:
        color = Color.green

    print(mygrid.tostring(f"Solution", color), end="")
    print(f"Empty cell count = {mygrid.emptycellcount}", end="\n")


# noinspection SpellCheckingInspection
def __main_singlepuzzle():
    mypuzzle = loadpuzzlebyname("Lesson 3x3", "board_sudoku_2.txt")

    __solve(mypuzzle)


# noinspection SpellCheckingInspection
def __main():
    games = loadpuzzles("board_sudoku_2.txt")  # [__puzzle1(), __puzzle2(), __puzzle3(), __puzzle4()]
    # games = loadpuzzles("board_sudoku_1.txt")

    solutions = []
    for game in games:
        puzzle_solution = SudokuSolution(game.boardname, game.rows, game.columns, game.tostring(""))
        __solve(game)
        puzzle_solution.logsolution(game.tostring(""), game.ismatrixcomplete)
        solutions.append((game.emptycellcount, puzzle_solution))


if __name__ == "__main__":
    x = input("Which test utility (1/2)? ")
    if x == "1":
        __main()
    elif x == "2":
        __main_singlepuzzle()
