from unittest import TestCase

import testutil


# noinspection SpellCheckingInspection
class TestSudoku(TestCase):

    def test_setmatrixvalue(self):
        actualboard = testutil.loadpuzzlebyname("Case 1:Actual for test set value", "test_board_sudoku.txt")
        expectedboard = testutil.loadpuzzlebyname("Case 1:Expected for test set value", "test_board_sudoku.txt")

        actualboard.setgridvalue(1, 3, 5)

        self.assertEqual(expectedboard.rows, actualboard.rows, msg="There is  difference at the row level")
        self.assertEqual(expectedboard.columns, actualboard.columns, msg="There is  difference at the column level")
        self.assertEqual(expectedboard.blocks, actualboard.blocks, msg="There is  difference at the block level")

        actualboard = testutil.loadpuzzlebyname("Case 2:Actual for test set value", "test_board_sudoku.txt")
        expectedboard = testutil.loadpuzzlebyname("Case 2:Expected for test set value", "test_board_sudoku.txt")

        actualboard.setgridvalue(7, 3, 5)
        actualboard.setgridvalue(1, 3, 5)

        self.assertEqual(expectedboard.rows, actualboard.rows, msg="There is  difference at the row level")
        self.assertEqual(expectedboard.columns, actualboard.columns, msg="There is  difference at the column level")
        self.assertEqual(expectedboard.blocks, actualboard.blocks, msg="There is  difference at the block level")

    def test_get(self):
        actualboard = testutil.loadpuzzlebyname("Actual for test get value", "test_board_sudoku.txt")
        expectedvalue = 4

        self.assertEqual(expectedvalue, actualboard.get(4, 2))

    def test_checkgridvalue(self):
        actualboard = testutil.loadpuzzlebyname(
            "Case 1:Actual for test contains value in intersecting row, column, and block", "test_board_sudoku.txt")

        self.assertTrue(actualboard.checkgridvalue(0, 7, 1))
        actualboard = testutil.loadpuzzlebyname(
            "Case 2:Actual for test contains value in intersecting row, column, and block", "test_board_sudoku.txt")

        self.assertFalse(actualboard.checkgridvalue(0, 7, 1))
