from enum import Enum


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
    def __init__(self, name, rows=None):
        # Matrix definitions:
        # rows: horizontal 0..8 list
        # columns: vertical 0..8 list
        # blocks:  0,1,2
        #          3,4,5
        #          6,7,8 list
        if rows:
            self.matrix_height = len(rows)
            x = int(self.matrix_height ** 0.5)
            if x * x == self.matrix_height:
                self.block_height = x
            else:
                self.block_height = self.matrix_height
        else:
            self.matrix_height = 9
            self.block_height = 3

        self.base_number_set = set([i for i in range(1, self.matrix_height + 1)])
        self.base_number_set_with_zero = set([i for i in range(self.matrix_height + 1)])

        self.name = name
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
            if len(self.rows) == self.matrix_height:
                self.__populatecolumns()
            # populate blocks
            self.__setblocktocellcoordinatemapping()
            if len(self.rows) == self.matrix_height:
                self.__populateblocks()

            self.__countemptycells()
        elif rows is None or (isinstance(rows, list) and len(rows) == 0):
            self.createemptygrid()
        elif rows is not None:
            raise ValueError("Set of rows provided generate an invalid matrix.")

    def createemptygrid(self):
        for i in range(self.matrix_height):
            row = [0] * self.matrix_height
            self.rows.append(row)
        for i in range(self.matrix_height):
            col = [0] * self.matrix_height
            self.columns.append(col)
        for i in range(self.matrix_height):
            block = [0] * self.matrix_height
            self.blocks.append(block)
        self.emptycellcount = self.matrix_height * self.matrix_height
        self.__setblocktocellcoordinatemapping()

    def copygrid(self):
        result = [row[:] for row in self.rows]
        return result

    def celltoblockccoordinates(self, i, j):
        return self.coordinates[(i, j)]

    def blocktocellcoordinates(self, i, j):
        value = None
        for cellcoordinates, blockcoordinates in self.coordinates.items():
            if blockcoordinates == (i, j):
                value = cellcoordinates
                break
        return value

    def ismatrixvalid(self, rows):
        if len(rows) != self.matrix_height:
            return False
        else:
            for row in rows:
                if not isinstance(row, list) and len(row) != self.matrix_height:
                    return False
                elif isinstance(row, list) and len(row) == self.matrix_height:
                    for n in row:  # only allow '0' to be duplicate and only allow valid numbers
                        if (n != 0 and row.count(n) > 1) and n not in self.base_number_set:
                            return False
        return True

    @property
    def ismatrixcomplete(self):
        valid_row = True

        for row in self.rows:
            unique_values = set(row)
            missing_values = set(row).symmetric_difference(self.base_number_set)
            if len(missing_values) > 0 and len(unique_values) == len(row):
                valid_row = False
                break

        return valid_row

    @property
    def ismatrixsolved(self):
        return self.ismatrixcomplete and sum([row.count(0) for row in self.rows]) == 0

    def setmatrixvalue(self, i, j, value, overwrite=False, startfromblockcoordinates=False,
                       insert_check_overwrite=None):
        global arg_block_i, arg_block_j
        if startfromblockcoordinates:
            blockcoordinates = self.blocktocellcoordinates(i, j)
            arg_block_i = i
            arg_block_j = j
            i = blockcoordinates[0]
            j = blockcoordinates[1]

        if insert_check_overwrite is None:
            check = not self.sectioncontainsvalue(i, j, value)
        else:
            check = insert_check_overwrite

        if check:
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

            return zeroupdated

    def sectioncontainsvalue(self, i, j, value):
        row_contains = value in self.rows[i]
        column_contains = value in self.columns[j]

        # only check block contain if there are blocks
        if self.block_height != self.matrix_height:
            blockcoordinates = self.celltoblockccoordinates(i, j)
            block_contains = value in self.blocks[blockcoordinates[0]]

            return row_contains or column_contains or block_contains
        else:
            return row_contains or column_contains

    def get(self, i, j):
        return self.rows[i][j]

    def tostring(self, label=None, color=Color.reset):
        result = ""
        matrix = ""
        for i in range(self.matrix_height):
            matrix += "\t"
            for j in range(self.matrix_height):
                matrix += str(self.rows[i][j]) + " "
                if (j + 1) % self.block_height == 0:
                    matrix += " "
            matrix += "\n"
            if (i + 1) % self.block_height == 0:
                matrix += "\n"
                if label is None:
                    result = color.value + self.boardname + "\n" + matrix + Color.reset.value
                else:
                    result = color.value + label + "\n" + matrix + Color.reset.value
        return result

    def resetchangetrackingcount(self):
        self.__changes = 0

    @property
    def haschanged(self):
        return self.__changes > 0

    def __countemptycells(self):
        count = 0
        for row in self.rows:
            count += row.count(0)
        self.emptycellcount = count

    def __setblocktocellcoordinatemapping(self):
        # dict(celllcoordinates, blockcoordinatess)

        # first check if there are blocks
        if self.block_height != self.matrix_height:
            # cellcoordinates(i=up/down,j=left/right)
            for i in range(self.matrix_height):
                for j in range(self.matrix_height):
                    block_i = self.__gethorizontalshift(i) * self.block_height + self.__gethorizontalshift(j)
                    block_j = self.__getverticalshift(i) * self.block_height + self.__getverticalshift(j)
                    cellcoordinates = (i, j)
                    blockcoordinates = (block_i, block_j)
                    self.coordinates[cellcoordinates] = blockcoordinates
        else:
            for i in range(self.matrix_height):
                for j in range(self.matrix_height):
                    block_i = 0
                    block_j = (i * self.matrix_height) + j
                    cellcoordinates = (i, j)
                    blockcoordinates = (block_i, block_j)
                    self.coordinates[cellcoordinates] = blockcoordinates

        # self.coordinates[(0, 0)] = (0, 0)
        # self.coordinates[(0, 1)] = (0, 1)
        # self.coordinates[(0, 2)] = (0, 2)
        # self.coordinates[(0, 3)] = (1, 0)
        # self.coordinates[(0, 4)] = (1, 1)
        # self.coordinates[(0, 5)] = (1, 2)
        # self.coordinates[(0, 6)] = (2, 0)
        # self.coordinates[(0, 7)] = (2, 1)
        # self.coordinates[(0, 8)] = (2, 2)
        #
        # self.coordinates[(1, 0)] = (0, 3)
        # self.coordinates[(1, 1)] = (0, 4)
        # self.coordinates[(1, 2)] = (0, 5)
        # self.coordinates[(1, 3)] = (1, 3)
        # self.coordinates[(1, 4)] = (1, 4)
        # self.coordinates[(1, 5)] = (1, 5)
        # self.coordinates[(1, 6)] = (2, 3)
        # self.coordinates[(1, 7)] = (2, 4)
        # self.coordinates[(1, 8)] = (2, 5)
        #
        # self.coordinates[(2, 0)] = (0, 6)
        # self.coordinates[(2, 1)] = (0, 7)
        # self.coordinates[(2, 2)] = (0, 8)
        # self.coordinates[(2, 3)] = (1, 6)
        # self.coordinates[(2, 4)] = (1, 7)
        # self.coordinates[(2, 5)] = (1, 8)
        # self.coordinates[(2, 6)] = (2, 6)
        # self.coordinates[(2, 7)] = (2, 7)
        # self.coordinates[(2, 8)] = (2, 8)
        #
        # self.coordinates[(3, 0)] = (3, 0)
        # self.coordinates[(3, 1)] = (3, 1)
        # self.coordinates[(3, 2)] = (3, 2)
        # self.coordinates[(3, 3)] = (4, 0)
        # self.coordinates[(3, 4)] = (4, 1)
        # self.coordinates[(3, 5)] = (4, 2)
        # self.coordinates[(3, 6)] = (5, 0)
        # self.coordinates[(3, 7)] = (5, 1)
        # self.coordinates[(3, 8)] = (5, 2)
        #
        # self.coordinates[(4, 0)] = (3, 3)
        # self.coordinates[(4, 1)] = (3, 4)
        # self.coordinates[(4, 2)] = (3, 5)
        # self.coordinates[(4, 3)] = (4, 3)
        # self.coordinates[(4, 4)] = (4, 4)
        # self.coordinates[(4, 5)] = (4, 5)
        # self.coordinates[(4, 6)] = (5, 3)
        # self.coordinates[(4, 7)] = (5, 4)
        # self.coordinates[(4, 8)] = (5, 5)
        #
        # self.coordinates[(5, 0)] = (3, 6)
        # self.coordinates[(5, 1)] = (3, 7)
        # self.coordinates[(5, 2)] = (3, 8)
        # self.coordinates[(5, 3)] = (4, 6)
        # self.coordinates[(5, 4)] = (4, 7)
        # self.coordinates[(5, 5)] = (4, 8)
        # self.coordinates[(5, 6)] = (5, 6)
        # self.coordinates[(5, 7)] = (5, 7)
        # self.coordinates[(5, 8)] = (5, 8)
        #
        # self.coordinates[(6, 0)] = (6, 0)
        # self.coordinates[(6, 1)] = (6, 1)
        # self.coordinates[(6, 2)] = (6, 2)
        # self.coordinates[(6, 3)] = (7, 0)
        # self.coordinates[(6, 4)] = (7, 1)
        # self.coordinates[(6, 5)] = (7, 2)
        # self.coordinates[(6, 6)] = (8, 0)
        # self.coordinates[(6, 7)] = (8, 1)
        # self.coordinates[(6, 8)] = (8, 2)
        #
        # self.coordinates[(7, 0)] = (6, 3)
        # self.coordinates[(7, 1)] = (6, 4)
        # self.coordinates[(7, 2)] = (6, 5)
        # self.coordinates[(7, 3)] = (7, 3)
        # self.coordinates[(7, 4)] = (7, 4)
        # self.coordinates[(7, 5)] = (7, 5)
        # self.coordinates[(7, 6)] = (8, 3)
        # self.coordinates[(7, 7)] = (8, 4)
        # self.coordinates[(7, 8)] = (8, 5)
        #
        # self.coordinates[(8, 0)] = (6, 6)
        # self.coordinates[(8, 1)] = (6, 7)
        # self.coordinates[(8, 2)] = (6, 8)
        # self.coordinates[(8, 3)] = (7, 6)
        # self.coordinates[(8, 4)] = (7, 7)
        # self.coordinates[(8, 5)] = (7, 8)
        # self.coordinates[(8, 6)] = (8, 6)
        # self.coordinates[(8, 7)] = (8, 7)
        # self.coordinates[(8, 8)] = (8, 8)

    def __populatecolumns(self):
        # transpose through list comprehension
        self.columns = [[self.rows[j][i] for j in range(len(self.rows))] for i in range(len(self.rows[0]))]

    def __populateblocks(self):
        # create empty block lists first
        self.blocks = []
        # first check if there are blocks
        if self.block_height != self.matrix_height:
            for i in range(self.matrix_height):
                block = [0] * self.matrix_height
                self.blocks.append(block)
        else:
            block = [0] * (self.matrix_height ** 2)
            self.blocks.append(block)

        # second populate block list
        for cellcoordinates, blockcoordinates in self.coordinates.items():
            value = self.rows[cellcoordinates[0]][cellcoordinates[1]]
            self.blocks[blockcoordinates[0]][blockcoordinates[1]] = value

    '''
    Calculate horizontal index (row) shfting to generate block coordinate mapping
    '''
    def __gethorizontalshift(self, k):
        # build ranges dynamically based on block_height
        indexranges = []
        for i in range(self.block_height):
            zero = i * self.block_height
            rng = []
            for j in range(zero, zero + self.block_height):
                rng.append(j)
            indexranges.append(rng)

        for shift, indexrange in enumerate(indexranges):
            if k in indexrange:
                return shift
        return None

    '''
    Calculate vertical index (column)  shfting to generate block coordinate mapping
    '''
    def __getverticalshift(self, k):
        # build ranges dynamically based on block_height
        indexranges = []
        for i in range(self.block_height):
            upper = i + 2 * self.block_height + 1
            rng = []
            for j in range(i, upper, self.block_height):
                rng.append(j)
            indexranges.append(rng)

        for shift, indexrange in enumerate(indexranges):
            if k in indexrange:
                return shift
        return None


# noinspection SpellCheckingInspection
class SudokuSolution:

    def __init__(self, name, rows, columns, grid):
        self.boardname = name
        self.columns = columns
        self.rows = rows
        self.pregrid = grid
        self.postgrid = ""
        self.solved = False

    def logsolution(self, grid, solution):
        self.postgrid = grid
        self.solved = solution
