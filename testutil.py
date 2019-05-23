from pathlib import Path

from backtrack import *
from sudoku import Sudoku


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
def __main_singlepuzzle():
    mypuzzle = loadpuzzlebyname("Lesson 7", "board_sudoku_2.txt")
    solve(mypuzzle.rows, mypuzzle.boardname)


# noinspection SpellCheckingInspection
def __main():
    games = loadpuzzles("board_sudoku_1.txt")

    start = time.time()

    for game in games:
        solve(game.rows, game.boardname)

    stop = time.time()
    print(f"Set of puzzles lapse == {round((stop - start) * 1000, 1)} ms")

if __name__ == "__main__":
    x = input("1:(test one), 2:(test all) :: ")
    if x == "1":
        __main_singlepuzzle()
    elif x == "2":
        __main()
