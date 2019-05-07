from unittest import TestCase

import testutil


# noinspection SpellCheckingInspection
class TestSudoku(TestCase):

    def test_completesingleemptycellssections(self):
        actualboard = testutil.loadpuzzlebyname("Case 1:Actual for test single empty cell fill",
                                                "test_board_sudoku.txt")
        expectedboard = testutil.loadpuzzlebyname("Case 1:Expected for test single empty cell fill",
                                                  "test_board_sudoku.txt")

        actualboard.completesingleemptycellssections()

        self.assertEqual(expectedboard.rows, actualboard.rows, msg="There is  difference at the row level")
        self.assertEqual(expectedboard.columns, actualboard.columns, msg="There is  difference at the column level")
        self.assertEqual(expectedboard.blocks, actualboard.blocks, msg="There is  difference at the block level")

        actualboard = testutil.loadpuzzlebyname("Case 2:Actual for test single empty cell fill",
                                                "test_board_sudoku.txt")
        expectedboard = testutil.loadpuzzlebyname("Case 2:Expected for test single empty cell fill",
                                                  "test_board_sudoku.txt")

        actualboard.completesingleemptycellssections()

        self.assertEqual(expectedboard.rows, actualboard.rows, msg="There is  difference at the row level")
        self.assertEqual(expectedboard.columns, actualboard.columns, msg="There is  difference at the column level")
        self.assertEqual(expectedboard.blocks, actualboard.blocks, msg="There is  difference at the block level")

    def test_completedoubleemptycellssections(self):
        actualboard = testutil.loadpuzzlebyname("Case 1:Actual for test double empty cell fill",
                                                "test_board_sudoku.txt")
        expectedboard = testutil.loadpuzzlebyname("Case 1:Expected for test double empty cell fill",
                                                  "test_board_sudoku.txt")

        actualboard.completedoubleemptycellssections()

        self.assertEqual(expectedboard.rows, actualboard.rows, msg="There is  difference at the row level")
        self.assertEqual(expectedboard.columns, actualboard.columns, msg="There is  difference at the column level")
        self.assertEqual(expectedboard.blocks, actualboard.blocks, msg="There is  difference at the block level")

        actualboard = testutil.loadpuzzlebyname("Case 2:Actual for test double empty cell fill",
                                                "test_board_sudoku.txt")
        expectedboard = testutil.loadpuzzlebyname("Case 2:Expected for test double empty cell fill",
                                                  "test_board_sudoku.txt")

        actualboard.completedoubleemptycellssections()

        self.assertEqual(expectedboard.rows, actualboard.rows, msg="There is  difference at the row level")
        self.assertEqual(expectedboard.columns, actualboard.columns, msg="There is  difference at the column level")
        self.assertEqual(expectedboard.blocks, actualboard.blocks, msg="There is  difference at the block level")

    def test_setmatrixvalue(self):
        actualboard = testutil.loadpuzzlebyname("Case 1:Actual for test set value", "test_board_sudoku.txt")
        expectedboard = testutil.loadpuzzlebyname("Case 1:Expected for test set value", "test_board_sudoku.txt")

        actualboard.setmatrixvalue(1, 3, 5)

        self.assertEqual(expectedboard.rows, actualboard.rows, msg="There is  difference at the row level")
        self.assertEqual(expectedboard.columns, actualboard.columns, msg="There is  difference at the column level")
        self.assertEqual(expectedboard.blocks, actualboard.blocks, msg="There is  difference at the block level")

        actualboard = testutil.loadpuzzlebyname("Case 2:Actual for test set value", "test_board_sudoku.txt")
        expectedboard = testutil.loadpuzzlebyname("Case 2:Expected for test set value", "test_board_sudoku.txt")

        actualboard.setmatrixvalue(7, 3, 5)
        actualboard.setmatrixvalue(1, 3, 5)

        self.assertEqual(expectedboard.rows, actualboard.rows, msg="There is  difference at the row level")
        self.assertEqual(expectedboard.columns, actualboard.columns, msg="There is  difference at the column level")
        self.assertEqual(expectedboard.blocks, actualboard.blocks, msg="There is  difference at the block level")

    def test_get(self):
        actualboard = testutil.loadpuzzlebyname("Actual for test get value", "test_board_sudoku.txt")
        expectedvalue = 4

        self.assertEqual(expectedvalue, actualboard.get(4, 2))

    def test_contains(self):
        actualboard = testutil.loadpuzzlebyname(
            "Case 1:Actual for test contains value in intersecting row, column, and block", "test_board_sudoku.txt")

        self.assertTrue(actualboard.sectioncontainsvalue(0, 7, 1))
        actualboard = testutil.loadpuzzlebyname(
            "Case 2:Actual for test contains value in intersecting row, column, and block", "test_board_sudoku.txt")

        self.assertFalse(actualboard.sectioncontainsvalue(0, 7, 1))

    def test_completehorizontalblocksemptycells(self):
        actualboard = testutil.loadpuzzlebyname("Case 1:Actual for test horizontal block empty cells",
                                                "test_board_sudoku.txt")
        expectedboard = testutil.loadpuzzlebyname("Case 1:Expected for test horizontal block empty cells",
                                                  "test_board_sudoku.txt")

        actualboard.completehorizontalblocksemptycells()

        self.assertEqual(expectedboard.rows, actualboard.rows, msg="There is  difference at the row level")
        self.assertEqual(expectedboard.columns, actualboard.columns, msg="There is  difference at the column level")
        self.assertEqual(expectedboard.blocks, actualboard.blocks, msg="There is  difference at the block level")

        actualboard = testutil.loadpuzzlebyname("Case 2:Actual for test horizontal block empty cells",
                                                "test_board_sudoku.txt")
        expectedboard = testutil.loadpuzzlebyname("Case 2:Expected for test horizontal block empty cells",
                                                  "test_board_sudoku.txt")

        actualboard.completehorizontalblocksemptycells()

        self.assertEqual(expectedboard.rows, actualboard.rows, msg="There is  difference at the row level")
        self.assertEqual(expectedboard.columns, actualboard.columns, msg="There is  difference at the column level")
        self.assertEqual(expectedboard.blocks, actualboard.blocks, msg="There is  difference at the block level")

    def test_completeverticalblocksemptycells(self):
        actualboard = testutil.loadpuzzlebyname("Case 1:Actual for test vertical block empty cells",
                                                "test_board_sudoku.txt")
        expectedboard = testutil.loadpuzzlebyname("Case 1:Expected for test vertical block empty cells",
                                                  "test_board_sudoku.txt")

        actualboard.completeverticalblocksemptycells()

        self.assertEqual(expectedboard.rows, actualboard.rows, msg="There is  difference at the row level")
        self.assertEqual(expectedboard.columns, actualboard.columns, msg="There is  difference at the column level")
        self.assertEqual(expectedboard.blocks, actualboard.blocks, msg="There is  difference at the block level")

        actualboard = testutil.loadpuzzlebyname("Case 2:Actual for test vertical block empty cells",
                                                "test_board_sudoku.txt")
        expectedboard = testutil.loadpuzzlebyname("Case 2:Expected for test vertical block empty cells",
                                                  "test_board_sudoku.txt")

        actualboard.completeverticalblocksemptycells()

        self.assertEqual(expectedboard.rows, actualboard.rows, msg="There is  difference at the row level")
        self.assertEqual(expectedboard.columns, actualboard.columns, msg="There is  difference at the column level")
        self.assertEqual(expectedboard.blocks, actualboard.blocks, msg="There is  difference at the block level")
