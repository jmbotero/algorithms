from unittest import TestCase
from sudoku import Sudoku

import testutil

# noinspection SpellCheckingInspection
class TestSudoku(TestCase):

    def test_completesingleemptycellssections(self):
        p = Sudoku("One empty cells",
                   [[4, 7, 8, 3, 5, 9, 1, 2, 6], [6, 3, 9, 1, 2, 8, 7, 5, 4], [2, 5, 1, 4, 7, 6, 3, 9, 8],
                    [3, 6, 4, 7, 8, 2, 9, 1, 5], [9, 8, 0, 6, 3, 1, 2, 4, 7], [7, 1, 2, 9, 4, 5, 8, 6, 3],
                    [8, 2, 6, 5, 9, 3, 4, 7, 1], [1, 4, 3, 2, 6, 7, 5, 8, 9], [5, 9, 7, 8, 1, 4, 6, 3, 2]])
        expectedcellvalue = 5

        p.completesingleemptycellssections()

        self.assertEqual(expectedcellvalue, p.rows[4][2])

    def test_completedoubleemptycellssections(self):
        p = Sudoku("Two empty cells in row",
                   [[4, 7, 8, 3, 5, 9, 1, 2, 6], [6, 3, 9, 1, 2, 8, 7, 5, 4], [2, 5, 1, 4, 7, 6, 3, 9, 8],
                    [3, 6, 4, 7, 8, 2, 9, 1, 5], [9, 0, 5, 6, 3, 1, 2, 4, 0], [7, 1, 2, 9, 4, 5, 8, 6, 3],
                    [8, 2, 6, 5, 9, 3, 4, 7, 1], [1, 4, 3, 2, 6, 7, 5, 8, 9], [5, 9, 7, 8, 1, 4, 6, 3, 2]])
        expectedcellvalue1 = 8
        expectedcellvalue2 = 7

        p.completedoubleemptycellssections()

        self.assertEqual(expectedcellvalue1, p.rows[4][1])
        self.assertEqual(expectedcellvalue2, p.rows[4][8])

        p = Sudoku("Two empty cells in column",
                   [[0, 7, 8, 3, 5, 9, 1, 2, 6], [6, 3, 9, 1, 2, 8, 7, 5, 4], [2, 5, 1, 4, 7, 6, 3, 9, 8],
                    [3, 6, 4, 7, 8, 2, 9, 1, 5], [0, 8, 5, 6, 3, 1, 2, 4, 7], [7, 1, 2, 9, 4, 5, 8, 6, 3],
                    [8, 2, 6, 5, 9, 3, 4, 7, 1], [1, 4, 3, 2, 6, 7, 5, 8, 9], [5, 9, 7, 8, 1, 4, 6, 3, 2]])
        expectedcellvalue1 = 4
        expectedcellvalue2 = 9

        p.completedoubleemptycellssections()

        self.assertEqual(expectedcellvalue1, p.columns[0][0])
        self.assertEqual(expectedcellvalue2, p.columns[0][4])

    def test_completeverticalblockemptycells(self):
        p = Sudoku("CLR puzzle",
                   [[2, 0, 0, 0, 7, 0, 9, 4, 0], [0, 3, 0, 6, 0, 2, 8, 0, 0], [1, 6, 0, 0, 0, 9, 7, 0, 2],
                    [4, 1, 0, 5, 0, 0, 6, 0, 3], [0, 0, 7, 3, 2, 0, 0, 0, 0], [3, 5, 0, 4, 0, 6, 1, 0, 9],
                    [9, 0, 1, 0, 0, 0, 3, 8, 4], [0, 0, 0, 0, 1, 8, 0, 6, 7], [0, 0, 6, 7, 0, 4, 5, 0, 1]])

        p.completeverticalblockemptycells()
        p.completehorizontalblockemptycells()
        while not p.ismatrixcomplete:
            p.completesingleemptycellssections()
            p.completedoubleemptycellssections()

        solved = p.ismatrixcomplete

        self.assertTrue(solved)

    def test_setmatrixvalue(self):
        actualboard = Sudoku("Test",
                             [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]])
        expectedboard = Sudoku("Test",
                               [[0, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]])

        actualboard.setmatrixvalue(0, 8, 8)
        actualboard.setmatrixvalue(7, 0, 3)

        self.assertEqual(expectedboard.rows, actualboard.rows)
        self.assertEqual(expectedboard.columns, actualboard.columns)
        self.assertEqual(expectedboard.blocks, actualboard.blocks)

    def test_get(self):
        p = Sudoku("Only one cell with value",
                   [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 4, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]])
        expectedvalue = 4

        self.assertEqual(expectedvalue, p.get(4, 2))

    def test_contains(self):
        p = Sudoku("Same value for intersecting row, column, and block",
                   [[4, 0, 0, 0, 0, 0, 0, 0, 0], [4, 0, 0, 0, 0, 0, 0, 0, 0], [4, 0, 0, 0, 0, 0, 4, 4, 4],
                    [4, 0, 0, 0, 0, 0, 0, 0, 0], [4, 0, 4, 0, 0, 0, 0, 0, 0], [4, 0, 0, 0, 0, 0, 4, 4, 4],
                    [4, 4, 4, 4, 4, 4, 4, 4, 4], [4, 0, 0, 0, 0, 0, 4, 4, 4], [4, 0, 0, 0, 0, 0, 4, 4, 4]])

        self.assertTrue(p.matrixcontainsvalue(6, 6, 4) and not p.matrixcontainsvalue(1, 1, 5))

    def test_completeblockemptycells(self):
        actualboard = testutil.loadpuzzlebyname("Actual for test block empty cells", "test_board_sudoku.txt")
        expectedboard = testutil.loadpuzzlebyname("Expected for test block empty cells", "test_board_sudoku.txt")

        actualboard.completeblockemptycells()
        
        self.assertEqual(expectedboard.rows, actualboard.rows, msg="There is  difference at the row level")
        self.assertEqual(expectedboard.columns, actualboard.columns, msg="There is  difference at the column level")
        self.assertEqual(expectedboard.blocks, actualboard.blocks, msg="There is  difference at the block level")
