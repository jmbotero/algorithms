from unittest import TestCase

from sudoku import Sudoku


# noinspection SpellCheckingInspection
class TestSudoku(TestCase):
    def test_horizontalblocktecnique(self):
        p = Sudoku("TMB puzzle",
                   [[4, 7, 8, 3, 0, 9, 1, 2, 0], [0, 0, 9, 1, 2, 8, 7, 5, 4], [2, 5, 1, 0, 7, 0, 3, 0, 8],
                    [3, 0, 4, 7, 8, 2, 9, 0, 5], [9, 0, 0, 6, 3, 0, 2, 4, 0], [7, 1, 2, 9, 0, 5, 8, 6, 0],
                    [8, 2, 6, 0, 9, 0, 4, 7, 1], [0, 4, 3, 0, 6, 7, 0, 0, 9], [5, 0, 0, 8, 1, 4, 0, 3, 2]])

        p.horizontalblocktecnique()
        p.completesingleemptycellssections()

        solved = p.ismatrixcomplete

        self.assertTrue(solved)

    def test_completesingleemptycellssections(self):
        p = Sudoku("One empty cells",
                   [[4, 7, 8, 3, 5, 9, 1, 2, 6], [6, 3, 9, 1, 2, 8, 7, 5, 4], [2, 5, 1, 4, 7, 6, 3, 9, 8],
                    [3, 6, 4, 7, 8, 2, 9, 1, 5], [9, 8, 0, 6, 3, 1, 2, 4, 7], [7, 1, 2, 9, 4, 5, 8, 6, 3],
                    [8, 2, 6, 5, 9, 3, 4, 7, 1], [1, 4, 3, 2, 6, 7, 5, 8, 9], [5, 9, 7, 8, 1, 4, 6, 3, 2]])
        expectedcellvalue = 5

        p.completesingleemptycellssections()

        self.assertEqual(expectedcellvalue, p.rows[4][2])

    def test_completedoubleemptycellssections(self):
        p = Sudoku("Two empty cells",
                   [[4, 7, 8, 3, 5, 9, 1, 2, 6], [6, 3, 9, 1, 2, 8, 7, 5, 4], [2, 5, 1, 4, 7, 6, 3, 9, 8],
                    [3, 6, 4, 7, 8, 2, 9, 1, 5], [9, 0, 5, 6, 3, 1, 2, 4, 0], [7, 1, 2, 9, 4, 5, 8, 6, 3],
                    [8, 2, 6, 5, 9, 3, 4, 7, 1], [1, 4, 3, 2, 6, 7, 5, 8, 9], [5, 9, 7, 8, 1, 4, 6, 3, 2]])
        expectedcellvalue1 = 8
        expectedcellvalue8 = 7

        p.completedoubleemptycellssections()

        self.assertEqual(expectedcellvalue1, p.rows[4][1])
        self.assertEqual(expectedcellvalue8, p.rows[4][8])

    def test_verticalblocktecnique(self):
        p = Sudoku("CLR puzzle",
                   [[2, 0, 0, 0, 7, 0, 9, 4, 0], [0, 3, 0, 6, 0, 2, 8, 0, 0], [1, 6, 0, 0, 0, 9, 7, 0, 2],
                    [4, 1, 0, 5, 0, 0, 6, 0, 3], [0, 0, 7, 3, 2, 0, 0, 0, 0], [3, 5, 0, 4, 0, 6, 1, 0, 9],
                    [9, 0, 1, 0, 0, 0, 3, 8, 4], [0, 0, 0, 0, 1, 8, 0, 6, 7], [0, 0, 6, 7, 0, 4, 5, 0, 1]])

        p.verticalblocktecnique()
        p.horizontalblocktecnique()
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
        self.assertEqual(expectedboard.blocks, actualboard.blocks                             )

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

        self.assertTrue(p.contains(6, 6, 4) and not p.contains(1, 1, 5))
