import random
from enum import Enum
from typing import List, Any


class Color(Enum):
    red = "\033[1;31;m"
    green = "\033[1;32;m"
    reset = "\033[m"


"""
    Subclassing basic type list to add extension method
"""


# noinspection SpellCheckingInspection
class Mylist(list):
    def removeandgetnext(self, value):
        i = self.index(value)
        self.remove(value)
        if i > len(self):
            if len(self) == 0:
                return -1
            else:
                return 0
        else:
            return i


# noinspection SpellCheckingInspection
class Sudoku:
    matrix_height = 9
    block_height = 3
    base_number_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    base_number_set_with_zero = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

    def __init__(self, name, rows=None):
        # Matrix definitions:
        # rows: horizontal 0..8 list
        # columns: vertical 0..8 list
        # blocks:  0,1,2
        #          3,4,5
        #          6,7,8 list
        self.boardname = name
        self.__changes = 0
        self.emptycellcount = 0
        self.coordinates = {}
        self.columns = []
        self.rows = []
        self.blocks = []
        if rows is not None and self.ismatrixvalid(rows):
            # populate rows
            self.rows = rows[:]  # copy list by slicing
            # populate columns
            if len(self.rows) == Sudoku.matrix_height:
                self.__populatecolumns()
            # populate blocks
            self.__setblocktocellcoordinatemapping()
            if len(self.rows) == Sudoku.matrix_height:
                self.__populateblocks()

            self.__countemptycells()
        elif rows is None or (isinstance(rows, list) and len(rows) == 0):
            self.createemptyboard()
        elif rows is not None:
            raise ValueError("Set of rows provided generate an invalid matrix.")

    def createemptyboard(self):
        for i in range(Sudoku.matrix_height):
            row = [0] * Sudoku.matrix_height
            self.rows.append(row)
        for i in range(Sudoku.matrix_height):
            col = [0] * Sudoku.matrix_height
            self.columns.append(col)
        for i in range(Sudoku.matrix_height):
            block = [0] * Sudoku.matrix_height
            self.blocks.append(block)
        self.emptycellcount = Sudoku.matrix_height * Sudoku.matrix_height
        self.__setblocktocellcoordinatemapping()

    def celltoblockccoordinates(self, i, j):
        return self.coordinates[(i, j)]

    def blocktocellcoordinates(self, i, j):
        value = None
        for cellcoordinates, blockcoordinates in self.coordinates.items():
            if blockcoordinates == (i, j):
                value = cellcoordinates
                break
        return value

    @staticmethod
    def ismatrixvalid(rows):
        if len(rows) != Sudoku.matrix_height:
            return False
        else:
            for row in rows:
                if not isinstance(row, list) and len(row) != Sudoku.matrix_height:
                    return False
                elif isinstance(row, list) and len(row) == Sudoku.matrix_height:
                    for n in row:  # only allow '0' to be duplicate and only allow valid numbers
                        if n != 0 and row.count(n) > 1 and n not in Sudoku.base_number_set:
                            return False
        return True

    @property
    def ismatrixcomplete(self):
        rowmatch = True

        for row in self.rows:
            diff = set(row).symmetric_difference(Sudoku.base_number_set)
            if len(diff) > 0:
                rowmatch = False
                break

        return rowmatch and self.emptycellcount == 0

    @property
    def ismatrixsolved(self):
        return self.ismatrixcomplete and self.__changes == 0

    def setmatrixvalue(self, i, j, value, overwrite=False, startfromblockcoordinates=False):
        if startfromblockcoordinates:
            blockcoordinates = self.blocktocellcoordinates(i, j)
            arg_block_i = i
            arg_block_j = j
            i = blockcoordinates[0]
            j = blockcoordinates[1]

        if not self.matrixcontainsvalue(i, j, value):
            zeroupdated = False
            if self.rows[i][j] == 0 or overwrite:
                if self.rows[i][j] == 0:
                    zeroupdated = True
                self.rows[i][j] = value
            if self.columns[j][i] == 0 or overwrite:
                if self.columns[j][i] == 0:
                    zeroupdated = True
                self.columns[j][i] = value
            if zeroupdated:
                self.emptycellcount -= 1
            if value == 0 and overwrite:
                self.emptycellcount += 1
            # reset blocks
            if startfromblockcoordinates:
                block_i = arg_block_i
                block_j = arg_block_j
            else:
                blockcoordinates = self.coordinates[(i, j)]
                block_i = blockcoordinates[0]
                block_j = blockcoordinates[1]
            if self.blocks[block_i][block_j] == 0 or overwrite:
                self.blocks[block_i][block_j] = value

            if zeroupdated:
                self.__changes += 1

    def matrixcontainsvalue(self, i, j, value):
        row_contains = value in self.rows[i]
        column_contains = value in self.columns[j]

        blockcoordinates = self.celltoblockccoordinates(i, j)
        block_contains = value in self.blocks[blockcoordinates[0]]

        return row_contains or column_contains or block_contains

    def get(self, i, j):
        return self.rows[i][j]

    def tostring(self, label=None, color=Color.reset):
        result = ""
        matrix = ""
        for i in range(Sudoku.matrix_height):
            matrix += "\t"
            for j in range(Sudoku.matrix_height):
                matrix += str(self.rows[i][j]) + " "
                if (j + 1) % Sudoku.block_height == 0:
                    matrix += " "
            matrix += "\n"
            if (i + 1) % Sudoku.block_height == 0:
                matrix += "\n"
                if label is None:
                    result = color.value + self.boardname + "\n" + matrix + Color.reset.value
                else:
                    result = color.value + label + "\n" + matrix + Color.reset.value
        return result

    def completesingleemptycellssections(self):
        self.__changes = 0  # reset change tracking
        # process rows
        i = 0
        for row in self.rows:
            if row.count(0) == 1:
                j = row.index(0)
                diff = list(set(row).symmetric_difference(Sudoku.base_number_set_with_zero))
                value = diff[0]
                if len(diff) > 1:
                    raise ValueError(
                        "Found more than one missing value (" + str(value) + ") in row (" + str(i) + ") = [" + ','.join(
                            [str(v) for v in row]) + "], just expected one.")
                if not self.matrixcontainsvalue(i, j, value):  # value not in row and value not in self.columns[j]:
                    self.setmatrixvalue(i, j, value)
            i += 1
        # process columns
        j = 0
        for col in self.columns:
            if col.count(0) == 1:
                i = col.index(0)
                diff = list(set(col).symmetric_difference(Sudoku.base_number_set_with_zero))
                value = diff[0]
                if len(diff) > 1:
                    raise ValueError("Found more than one missing value (" + str(value) + ") in column (" + str(
                        j) + ") = [" + ','.join([str(v) for v in col]) + "], just expected one.")
                if not self.matrixcontainsvalue(i, j, value):  # value not in col and value not in self.rows[i]:
                    self.setmatrixvalue(i, j, value)
            j += 1
        # process.blocks
        i = 0
        for block in self.blocks:
            if block.count(0) == 1:
                j = block.index(0)
                diff = list(set(block).symmetric_difference(Sudoku.base_number_set_with_zero))
                value = diff[0]
                if len(diff) > 1:
                    raise ValueError("Found more than one missing value (" + str(value) + ") in block (" + str(
                        i) + ") = [" + ','.join([str(v) for v in block]) + "], just expected one.")
                cellcoordinates = self.blocktocellcoordinates(i, j)
                if not self.matrixcontainsvalue(cellcoordinates[0], cellcoordinates[1], value):  # value not in block:
                    self.setmatrixvalue(cellcoordinates[0], cellcoordinates[1], value)
            i += 1

    def completedoubleemptycellssections(self):
        self.__changes = 0  # reset change tracking
        # process rows
        for i, row in enumerate(self.rows):
            if row.count(0) == 2:
                missings = list(set(row).symmetric_difference(Sudoku.base_number_set_with_zero))
                zero_indexes = Mylist([idx for idx, item in enumerate(row) if item == 0])
                j_a = zero_indexes[0]
                j_b = zero_indexes[1]
                a = missings[0]
                b = missings[1]
                a_in_firstindex = self.matrixcontainsvalue(i, j_a, a)
                a_in_secondindex = self.matrixcontainsvalue(i, j_b, a)
                b_in_firstindex = self.matrixcontainsvalue(i, j_a, b)
                b_in_secondindex = self.matrixcontainsvalue(i, j_b, b)
                if not a_in_firstindex and not b_in_secondindex:
                    self.setmatrixvalue(i, j_a, a)
                    self.setmatrixvalue(i, j_b, b)
                elif not a_in_secondindex and not b_in_firstindex:
                    self.setmatrixvalue(i, j_b, a)
                    self.setmatrixvalue(i, j_a, b)
        # process columns
        for j, column in enumerate(self.columns):
            if column.count(0) == 2:
                missings = Mylist(list(set(column).symmetric_difference(Sudoku.base_number_set_with_zero)))
                zero_indexes = Mylist([idx for idx, item in enumerate(column) if item == 0])
                i_a = zero_indexes[0]
                i_b = zero_indexes[1]
                a = missings[0]
                b = missings[1]
                a_in_firstindex = self.matrixcontainsvalue(i_a, j, a)
                a_in_secondindex = self.matrixcontainsvalue(i_b, j, a)
                b_in_firstindex = self.matrixcontainsvalue(i_a, j, b)
                b_in_secondindex = self.matrixcontainsvalue(i_b, j, b)
                if not a_in_firstindex and not b_in_secondindex:
                    self.setmatrixvalue(i_a, j, a)
                    self.setmatrixvalue(i_b, j, b)
                elif not a_in_secondindex and not b_in_firstindex:
                    self.setmatrixvalue(i_b, j, a)
                    self.setmatrixvalue(i_a, j, b)

    def completeblockemptycells(self):
        self.__changes = 0  # reset change tracking
        for value in range(1, Sudoku.matrix_height + 1):
            i = 0
            # loop through block groups
            for b in range(0, Sudoku.matrix_height, Sudoku.block_height):
                selected_block = None
                index_value_adjacentblocks = []
                block_id = list(range(b, b + Sudoku.block_height))
            # look for block without value in set of blocks in uberrow
                for i in range(b, b + Sudoku.block_height):
                    block = self.blocks[i]
                    if value in block:
                        block_id.remove(i)
                        index_value_adjacentblocks.append(block.index(value))
                if len(block_id) == 1:
                    i = block_id[0]
                    selected_block = self.blocks[i]
            # find empty cells in block
                if selected_block is not None:
                    emptycells = self.__getblockemptycells(selected_block, index_value_adjacentblocks)
                    for j in emptycells:
                        self.setmatrixvalue(i, j, value, startfromblockcoordinates=True)

    def completeverticalblockemptycells(self):
        self.__changes = 0  # reset change tracking
        # Analyze blocks left, center, right
        for index in range(Sudoku.block_height):
            for i in range(self.matrix_height):
                value = i + 1
                empty_cells = self.__getverticalblockemptycells(index, value)
                if empty_cells is not None and len(empty_cells) > 0:
                    for row, col in empty_cells.items():
                        if not self.matrixcontainsvalue(row, col, value):
                            self.setmatrixvalue(row, col, value)

    def resetchangetrackingcount(self):
        self.__changes = 0

    @property
    def haschanged(self):
        return self.__changes > 0

    def __istopmiddlebottommatch(self, i, j, value):
        match = False
        adjacents = self.__getdadjacentsectionindices(j)
        if adjacents is not None:
            if i in [0, 1, 2]:
                if (value in self.columns[adjacents[0]][3:6] and value in self.columns[adjacents[1]][6:9]) or (value in self.columns[adjacents[0]][3:6] and value in self.columns[adjacents[1]][6:9]):
                    match = True
            elif i in [3, 4, 5]:
                if (value in self.columns[adjacents[0]][0:3] and value in self.columns[adjacents[1]][6:9]) or (value in self.columns[adjacents[0]][0:3] and value in self.columns[adjacents[1]][6:9]):
                    match = True
            else:
                if (value in self.columns[adjacents[0]][0:3] and value in self.columns[adjacents[1]][3:6]) or (value in self.columns[adjacents[0]][0:3] and value in self.columns[adjacents[1]][3:6]):
                    match = True

        return match

    def __isleftcenterrightmatch(self, i, j, value):
        match = False
        adjacents = self.__getdadjacentsectionindices(i)
        if adjacents is not None:
            if j in [0, 1, 2]:
                if (value in self.rows[adjacents[0]][3:6] and value in self.rows[adjacents[1]][6:9]) or (value in self.rows[adjacents[0]][3:6] and value in self.rows[adjacents[1]][6:9]):
                    match = True
            elif j in [3, 4, 5]:
                if (value in self.rows[adjacents[0]][0:3] and value in self.rows[adjacents[1]][6:9]) or (value in self.rows[adjacents[0]][0:3] and value in self.rows[adjacents[1]][6:9]):
                    match = True
            else:
                if (value in self.rows[adjacents[0]][0:3] and value in self.rows[adjacents[1]][3:6]) or (value in self.rows[adjacents[0]][0:3] and value in self.rows[adjacents[1]][3:6]):
                    match = True

        return match

    def __countemptycells(self):
        count = 0
        for row in self.rows:
            count += row.count(0)
        self.emptycellcount = count

    def __setblocktocellcoordinatemapping(self):
        # todo: replace hard-coding with loops
        # for i in range(Sudoku.matrix_height):
        #     for j in range(Sudoku.matrix_height):
        #         block_i = self.__getrowshift(i) * Sudoku.block_height + self.__getrowshift(i)
        #         block_j = self.__getrowshift(i) * Sudoku.block_height + self.__getcolumnshift(j)
        #         cellcoordinates = (i, j)
        #         blockcoordinates = (block_i, block_j)
        #         self.coordinates[cellcoordinates] = blockcoordinates

        # cellcoordinates(i=up/down,j=left/right)
        # dict(celllcoordinates, blokcoordinatess)
        self.coordinates[(0, 0)] = (0, 0)
        self.coordinates[(0, 1)] = (0, 1)
        self.coordinates[(0, 2)] = (0, 2)
        self.coordinates[(0, 3)] = (1, 0)
        self.coordinates[(0, 4)] = (1, 1)
        self.coordinates[(0, 5)] = (1, 2)
        self.coordinates[(0, 6)] = (2, 0)
        self.coordinates[(0, 7)] = (2, 1)
        self.coordinates[(0, 8)] = (2, 2)

        self.coordinates[(1, 0)] = (0, 3)
        self.coordinates[(1, 1)] = (0, 4)
        self.coordinates[(1, 2)] = (0, 5)
        self.coordinates[(1, 3)] = (1, 3)
        self.coordinates[(1, 4)] = (1, 4)
        self.coordinates[(1, 5)] = (1, 5)
        self.coordinates[(1, 6)] = (2, 3)
        self.coordinates[(1, 7)] = (2, 4)
        self.coordinates[(1, 8)] = (2, 5)

        self.coordinates[(2, 0)] = (0, 6)
        self.coordinates[(2, 1)] = (0, 7)
        self.coordinates[(2, 2)] = (0, 8)
        self.coordinates[(2, 3)] = (1, 6)
        self.coordinates[(2, 4)] = (1, 7)
        self.coordinates[(2, 5)] = (1, 8)
        self.coordinates[(2, 6)] = (2, 6)
        self.coordinates[(2, 7)] = (2, 7)
        self.coordinates[(2, 8)] = (2, 8)

        self.coordinates[(3, 0)] = (3, 0)
        self.coordinates[(3, 1)] = (3, 1)
        self.coordinates[(3, 2)] = (3, 2)
        self.coordinates[(3, 3)] = (4, 0)
        self.coordinates[(3, 4)] = (4, 1)
        self.coordinates[(3, 5)] = (4, 2)
        self.coordinates[(3, 6)] = (5, 0)
        self.coordinates[(3, 7)] = (5, 1)
        self.coordinates[(3, 8)] = (5, 2)

        self.coordinates[(4, 0)] = (3, 3)
        self.coordinates[(4, 1)] = (3, 4)
        self.coordinates[(4, 2)] = (3, 5)
        self.coordinates[(4, 3)] = (4, 3)
        self.coordinates[(4, 4)] = (4, 4)
        self.coordinates[(4, 5)] = (4, 5)
        self.coordinates[(4, 6)] = (5, 3)
        self.coordinates[(4, 7)] = (5, 4)
        self.coordinates[(4, 8)] = (5, 5)

        self.coordinates[(5, 0)] = (3, 6)
        self.coordinates[(5, 1)] = (3, 7)
        self.coordinates[(5, 2)] = (3, 8)
        self.coordinates[(5, 3)] = (4, 6)
        self.coordinates[(5, 4)] = (4, 7)
        self.coordinates[(5, 5)] = (4, 8)
        self.coordinates[(5, 6)] = (5, 6)
        self.coordinates[(5, 7)] = (5, 7)
        self.coordinates[(5, 8)] = (5, 8)

        self.coordinates[(6, 0)] = (6, 0)
        self.coordinates[(6, 1)] = (6, 1)
        self.coordinates[(6, 2)] = (6, 2)
        self.coordinates[(6, 3)] = (7, 0)
        self.coordinates[(6, 4)] = (7, 1)
        self.coordinates[(6, 5)] = (7, 2)
        self.coordinates[(6, 6)] = (8, 0)
        self.coordinates[(6, 7)] = (8, 1)
        self.coordinates[(6, 8)] = (8, 2)

        self.coordinates[(7, 0)] = (6, 3)
        self.coordinates[(7, 1)] = (6, 4)
        self.coordinates[(7, 2)] = (6, 5)
        self.coordinates[(7, 3)] = (7, 3)
        self.coordinates[(7, 4)] = (7, 4)
        self.coordinates[(7, 5)] = (7, 5)
        self.coordinates[(7, 6)] = (8, 3)
        self.coordinates[(7, 7)] = (8, 4)
        self.coordinates[(7, 8)] = (8, 5)

        self.coordinates[(8, 0)] = (6, 6)
        self.coordinates[(8, 1)] = (6, 7)
        self.coordinates[(8, 2)] = (6, 8)
        self.coordinates[(8, 3)] = (7, 6)
        self.coordinates[(8, 4)] = (7, 7)
        self.coordinates[(8, 5)] = (7, 8)
        self.coordinates[(8, 6)] = (8, 6)
        self.coordinates[(8, 7)] = (8, 7)
        self.coordinates[(8, 8)] = (8, 8)

    def __populatecolumns(self):
        # transpose through list comprehension
        self.columns = [[self.rows[j][i] for j in range(len(self.rows))] for i in range(len(self.rows[0]))]

    def __populateblocks(self):
        # create empty block lists first
        self.blocks = []
        for i in range(Sudoku.matrix_height):
            block = [0] * Sudoku.matrix_height
            self.blocks.append(block)
        for cellcoordinates, blockcoordinates in self.coordinates.items():
            value = self.rows[cellcoordinates[0]][cellcoordinates[1]]
            self.blocks[blockcoordinates[0]][blockcoordinates[1]] = value

    def __getverticalblockemptycells(self, colindex, value):
        empty = {}
        block_cols = set(range(Sudoku.block_height))
        # first find block column without value
        selected_block = -1
        # get three blocks in colindex vertical
        for blockindex in [colindex, colindex + Sudoku.block_height, colindex + (2 * Sudoku.block_height)]:
            block = self.blocks[blockindex]
            if value not in block:
                selected_block = blockindex
            else:
                colshift = self.__getcolumnshift(block.index(value))
                if colshift in block_cols:
                    block_cols.remove(colshift)
        if len(block_cols) > 1:
            return None  # if value was missing in more than two blocks, skip it
        elif len(block_cols) == 0 and selected_block == -1:
            return None  # value found in all blocks so do nothing
        else:
            # row without value (block_rows should only have one value, so there is only one shift)
            selected_col_shift = list(block_cols)[0]  # store so we only look for empty cells in this row
            selected_col = colindex * Sudoku.block_height + selected_col_shift
        # then in column without value get empty cells
        if selected_block != -1:
            block = self.blocks[selected_block]
            if value not in block:
                for cellindex in range(len(block)):
                    cell = block[cellindex]
                    colshift = self.__getcolumnshift(cellindex)
                    rowshift = self.__getrowshift(cellindex)
                    # if cell is empty, add pair row,col to dictionary
                    if cell == 0 and colshift == selected_col_shift:
                        row = self.__getrowshift(selected_block) * Sudoku.block_height + rowshift
                        # only add cells in same column
                        if len(empty) == 0 or (len(empty) > 0 and selected_col in empty.values()):
                            empty[row] = selected_col
        return empty

    @staticmethod
    def __getrowshift(index):
        if index in [0, 1, 2]:
            shift = 0
        elif index in [3, 4, 5]:
            shift = 1
        else:
            shift = 2
        return shift

    @staticmethod
    def __getcolumnshift(index):
        if index in [0, 3, 6]:
            shift = 0
        elif index in [1, 4, 7]:
            shift = 1
        else:
            shift = 2
        return shift

    @staticmethod
    def __getdadjacentsectionindices(i):
        indexranges = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        for irange in indexranges:
            if i in irange:
                irange.remove(i)
                return irange
        return None

    def __getblockemptycells(self, selected_block, index_value_in_adjacentblocks):
        selected_blockrow_indices = self.__getblockrowindices(index_value_in_adjacentblocks)
        result = [idx for idx, value in enumerate(selected_block) if value == 0 and idx in selected_blockrow_indices]

        return result

    @staticmethod
    def __getblockrowindices(indices):
        result = None

        blockrow_index = [0, 1, 2]
        indexranges = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

        for index in indices:
            for i, irange in enumerate(indexranges):
                if index in irange:
                    blockrow_index.remove(i)
        if len(blockrow_index) == 1:
            result = indexranges[blockrow_index[0]]

        return result


# noinspection SpellCheckingInspection
class SudokuSolution:

    def __init__(self, name, rows, columns, board):
        self.boardname = name
        self.columns = columns
        self.rows = rows
        self.preboard = board
        self.postboard = ""
        self.solved = False

    def logsolution(self, board, solution):
        self.postboard = board
        self.solved = solution
