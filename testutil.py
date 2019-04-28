from sudoku import Sudoku
from sudoku import SudokuSolution
from sudoku import Color
from pathlib import Path


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent


def puzzle1():
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


def puzzle2():
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


def puzzle3():
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


def puzzle4():
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
def loadpuzzles(filename):
    puzzles = []
    rowcount = 0
    cellcount = 0
    row = []
    rows = []
    name = ""

    path = get_project_root()
    filename = f"{path}/data/{filename}"
    file = open(filename, encoding="utf-8-sig")  # use default mode='r' for utf8
    line = file.readline().strip()
    while line:
        if line.isnumeric():
            for c in line:
                row.append(int(c))
                cellcount += 1
            if cellcount == Sudoku.matrix_height:
                cellcount = 0
                rows.append(row)
                rowcount += 1
                row = []
            if rowcount == Sudoku.matrix_height:
                puzzles.append(Sudoku(name, rows))
                rows = []
                rowcount = 0
        else:
            name = line
            cellcount = 0
            rowcount = 0
        line = file.readline().strip()
    file.close()
    return puzzles


# noinspection SpellCheckingInspection
def loadpuzzlebyname(puzzlename, filename):
    rowcount = 0
    cellcount = 0
    row = []
    rows = []
    processpuzzle = False

    path = get_project_root()
    filename = f"{path}/data/{filename}"
    file = open(filename, encoding="utf-8-sig")  # use default mode='r' for utf8
    line = file.readline().strip()
    while line:
        if line.isnumeric():
            if processpuzzle:
                for c in line:
                    row.append(int(c))
                    cellcount += 1
                if cellcount == Sudoku.matrix_height:
                    cellcount = 0
                    rows.append(row)
                    rowcount += 1
                    row = []
        else:
            name = line
            processpuzzle = name == puzzlename
            cellcount = 0
            rowcount = 0
        line = file.readline().strip()
    file.close()

    return Sudoku(puzzlename, rows)


# noinspection SpellCheckingInspection
def solve(puzzle):
    loop = 1
    previousloopemptycount = puzzle.emptycellcount
    print(puzzle.tostring())

    changes = False
    while not puzzle.ismatrixcomplete:
        puzzle.completeblockemptycells()
        changes = changes or puzzle.haschanged
        # puzzle.completeverticalblockemptycells()
        # changes = changes or puzzle.haschanged
        # puzzle.completesingleemptycellssections()
        # changes = changes or puzzle.haschanged
        # puzzle.completedoubleemptycellssections()
        # changes = changes or puzzle.haschanged

        if not changes or previousloopemptycount == puzzle.emptycellcount:
            break

        if puzzle.emptycellcount != previousloopemptycount:
            previousloopemptycount = puzzle.emptycellcount

        loop += 1

    color = Color.red
    if puzzle.ismatrixcomplete:
        color = Color.green

    print(puzzle.tostring(f"Solution ({loop})", color))


# noinspection SpellCheckingInspection
def main_singlepuzzle():
    mypuzzle = loadpuzzlebyname("Lesson 1", "board_sudoku_2.txt")
    mypuzzle.completeblockemptycells()
    color = Color.red
    if mypuzzle.ismatrixcomplete:
        color = Color.green
    print(mypuzzle.tostring(f"Solution:", color))


# noinspection SpellCheckingInspection
def main():
    games = [puzzle1(), puzzle2(), puzzle3(), puzzle4()]
    # games = loadpuzzles("board_sudoku_1.txt")

    solutions = []
    for game in games:
        solution = SudokuSolution(game.boardname, game.rows, game.columns, game.tostring(""))
        solve(game)
        solution.logsolution(game.tostring(""), game.ismatrixcomplete)
        solutions.append((game.emptycellcount, solution))


if __name__ == "__main__":
    main_singlepuzzle()
