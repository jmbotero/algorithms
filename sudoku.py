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
        for i, row in enumerate(self.rows):
            if row.count(0) == 1:
                j = row.index(0)
                diff = list(set(row).symmetric_difference(Sudoku.base_number_set_with_zero))
                if len(diff) == 1:
                    value = diff[0]
                    self.setmatrixvalue(i, j, value)

    def completeemptycellswithnotcontainedvalues(self):
        self.__changes = 0  # reset change tracking

        for i in range(Sudoku.matrix_height):
            row = self.rows[i]
            # first calculate a number's weight=empty cells which it could occupy
            weights = {}
            missingvalues = list(set(row).symmetric_difference(Sudoku.base_number_set_with_zero))
            for value in missingvalues:
                weight = 0
                emptycells = [idx for idx, v in enumerate(row) if v == 0]
                if emptycells is not None:
                    for j in emptycells:
                        match = self.sectioncontainsvalue(i, j, value)
                        if match:
                            weight += 1
                    if weight != 0:
                        weights[(value, (i, j))] = weight
            lightcells = [cell for cell, weight in weights.items() if weight == 1]
            # now fill those empty cells for which for certain value when adding it there it's weigth is 19meaning its only candidate for this cell)
            for cell in lightcells:
                val = cell[0]
                cellcoordinates = cell[1]
                self.setmatrixvalue(cellcoordinates[0], cellcoordinates[1], val)

    def completedoubleemptycellssections(self):
        self.__processdoubleemptycellsbyrow(self.rows, self.columns)
        self.__processdoubleemptycellsbycolumn(self.columns, self.rows)
        # self.__processdoubleemptycellsbyblock(self.blocks, self.rows)

    def completehorizontalblocksemptycells(self):
        self.__changes = 0  # reset change tracking
        for value in range(1, Sudoku.matrix_height + 1):
            # loop through block groups
            for block_rowid in range(0, Sudoku.matrix_height, Sudoku.block_height):
                self.__pocesshorizontalblockrow(block_rowid, value)
                # i = 0
                # selected_block = None
                # index_value_adjacentblocks = []
                # block_id = list(range(block_rowid, block_rowid + Sudoku.block_height))
                # # look for block without value in set of blocks in uberrow
                # block_range = block_id[:]
                # for i in block_range:
                #     block = self.blocks[i]
                #     if value in block:
                #         block_id.remove(i)
                #         index_value_adjacentblocks.append(block.index(value))
                # if len(block_id) == 1:
                #     i = block_id[0]
                #     selected_block = self.blocks[i]
                # # find empty cells in block
                # if selected_block is not None:
                #     emptycells = self.__gethorizontalblocksemptycells(selected_block, i, index_value_adjacentblocks,
                #                                                       value)
                #     for j in emptycells:
                #         self.setmatrixvalue(i, j, value, startfromblockcoordinates=True)

    def completeverticalblocksemptycells(self):
        self.__changes = 0  # reset change tracking
        for value in range(1, Sudoku.matrix_height + 1):
            # loop through block groups
            for block_rowid in range(Sudoku.block_height):
                self.__processverticalblockrow(block_rowid, value)
                # i = 0
                # selected_block = None
                # index_value_adjacentblocks = []
                # block_id = list(range(block_rowid, Sudoku.matrix_height, Sudoku.block_height))
                # # look for block without value in set of blocks in uberrow
                # block_range = block_id[:]
                # for i in block_range:
                #     block = self.blocks[i]
                #     if value in block:
                #         block_id.remove(i)
                #         index_value_adjacentblocks.append(block.index(value))
                # if len(block_id) == 1:
                #     i = block_id[0]
                #     selected_block = self.blocks[i]
                # # find empty cells in block
                # if selected_block is not None:
                #     emptycells = self.__getverticalblocksemptycells(selected_block, i, index_value_adjacentblocks, value)
                #     for j in emptycells:
                #         updated = self.setmatrixvalue(i, j, value, startfromblockcoordinates=True)
                #         # if updated:
                #         #     self.__processblockramifications(i, value)

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
                if (value in self.columns[adjacents[0]][3:6] and value in self.columns[adjacents[1]][6:9]) or (
                        value in self.columns[adjacents[0]][3:6] and value in self.columns[adjacents[1]][6:9]):
                    match = True
            elif i in [3, 4, 5]:
                if (value in self.columns[adjacents[0]][0:3] and value in self.columns[adjacents[1]][6:9]) or (
                        value in self.columns[adjacents[0]][0:3] and value in self.columns[adjacents[1]][6:9]):
                    match = True
            else:
                if (value in self.columns[adjacents[0]][0:3] and value in self.columns[adjacents[1]][3:6]) or (
                        value in self.columns[adjacents[0]][0:3] and value in self.columns[adjacents[1]][3:6]):
                    match = True

        return match

    def __isleftcenterrightmatch(self, i, j, value):
        match = False
        adjacents = self.__getdadjacentsectionindices(i)
        if adjacents is not None:
            if j in [0, 1, 2]:
                if (value in self.rows[adjacents[0]][3:6] and value in self.rows[adjacents[1]][6:9]) or (
                        value in self.rows[adjacents[0]][3:6] and value in self.rows[adjacents[1]][6:9]):
                    match = True
            elif j in [3, 4, 5]:
                if (value in self.rows[adjacents[0]][0:3] and value in self.rows[adjacents[1]][6:9]) or (
                        value in self.rows[adjacents[0]][0:3] and value in self.rows[adjacents[1]][6:9]):
                    match = True
            else:
                if (value in self.rows[adjacents[0]][0:3] and value in self.rows[adjacents[1]][3:6]) or (
                        value in self.rows[adjacents[0]][0:3] and value in self.rows[adjacents[1]][3:6]):
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

    @staticmethod
    def __getdadjacentsectionindices(i):
        indexranges = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        for irange in indexranges:
            if i in irange:
                irange.remove(i)
                return irange
        return None

    @staticmethod
    def __gethorizontalblock_rowid(block_i):
        if block_i in [0, 1, 2]:
            rowid = 0
        elif block_i in [3, 4, 5]:
            rowid = 1
        else:
            rowid = 2
        return rowid

    def __gethorizontalblocksemptycells(self, selected_block, block_i_index, index_value_in_adjacentblocks, value):
        selected_blockrow_indices = self.__gettopmiddlebottom_blockrowindices(index_value_in_adjacentblocks)
        if selected_blockrow_indices is not None:
            result = [idx for idx, value in enumerate(selected_block) if
                      value == 0 and idx in selected_blockrow_indices]
        else:
            result = []

        # if indices are a triad try to reduce them to a pair by checking columns
        if len(result) == 3:
            for block_j in result:
                j = self.blocktocellcoordinates(block_i_index, block_j)[1]
                if value in self.columns[j]:
                    result.remove(block_j)
        # check if indexes are pair and one of columns with indices contains value, then return no indices
        if len(result) == 2:
            if self.__belongtosame_rowindexset(result, 2):
                # results are block indices need to convert them to cell coordinates to check columns list
                column1 = self.blocktocellcoordinates(block_i_index, result[0])[1]
                column2 = self.blocktocellcoordinates(block_i_index, result[1])[1]
                if value not in self.columns[column1] and value not in self.columns[column2]:
                    result = []
        return result

    def __getverticalblocksemptycells(self, selected_block, block_i_index, index_value_in_adjacentblocks, value):
        selected_blockcolumn_indices = self.__getleftcenterright_blockcolumnindices(index_value_in_adjacentblocks)
        if selected_blockcolumn_indices is not None:
            result = [idx for idx, value in enumerate(selected_block) if
                      value == 0 and idx in selected_blockcolumn_indices]
        else:
            result = []

        # if indices are a triad try to reduce them to a pair by checking rows
        if len(result) == 3:
            for block_j in result:
                i = self.blocktocellcoordinates(block_i_index, block_j)[0]
                if value in self.rows[i]:
                    result.remove(block_j)
        # check if indexes are pair and one of row with indices contains value, then return no indices
        if len(result) == 2:
            if self.__belongtosame_columnindexset(result, 2):
                # results are block indices need to convert them to cell coordinates to check rows list
                row1 = self.blocktocellcoordinates(block_i_index, result[0])[0]
                row2 = self.blocktocellcoordinates(block_i_index, result[1])[0]
                if value not in self.rows[row1] and value not in self.rows[row2]:
                    result = []
        return result

    @staticmethod
    def __gettopmiddlebottom_blockrowindices(indices):
        result = None

        blockcolumn_index = [0, 1, 2]
        indexranges = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

        for index in indices:
            for i, irange in enumerate(indexranges):
                if index in irange:
                    if i in blockcolumn_index:
                        blockcolumn_index.remove(i)
        if len(blockcolumn_index) == 1:
            result = indexranges[blockcolumn_index[0]]

        return result

    @staticmethod
    def __getleftcenterright_blockcolumnindices(indices):
        result = None

        blockrow_index = [0, 1, 2]
        indexranges = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]

        for index in indices:
            for i, irange in enumerate(indexranges):
                if index in irange:
                    if i in blockrow_index:
                        blockrow_index.remove(i)
        if len(blockrow_index) == 1:
            result = indexranges[blockrow_index[0]]

        return result

    @staticmethod
    def __belongtosame_rowindexset(indices, tuplelength):
        indexranges = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

        tuplematch = False
        for r in indexranges:
            match_count = 0
            for i in indices:
                if i in r:
                    match_count += 1
            if match_count == tuplelength:
                tuplematch = True

        return tuplematch

    @staticmethod
    def __belongtosame_columnindexset(indices, tuplelength):
        indexranges = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]

        tuplematch = False
        for r in indexranges:
            match_count = 0
            for i in indices:
                if i in r:
                    match_count += 1
            if match_count == tuplelength:
                tuplematch = True

        return tuplematch

    def __pocesshorizontalblockrow(self, block_rowid, value):
        i = 0
        selected_block = None
        index_value_adjacentblocks = []
        block_id = list(range(block_rowid, block_rowid + Sudoku.block_height))
        # look for block without value in set of blocks in uberrow
        block_range = block_id[:]
        for i in block_range:
            block = self.blocks[i]
            if value in block:
                block_id.remove(i)
                index_value_adjacentblocks.append(block.index(value))
        if len(block_id) == 1:
            i = block_id[0]
            selected_block = self.blocks[i]
        # find empty cells in block
        if selected_block is not None:
            emptycells = self.__gethorizontalblocksemptycells(selected_block, i, index_value_adjacentblocks, value)
            for j in emptycells:
                self.setmatrixvalue(i, j, value, startfromblockcoordinates=True)

    def __processverticalblockrow(self, block_rowid, value):
        i = 0
        selected_block = None
        index_value_adjacentblocks = []
        block_id = list(range(block_rowid, Sudoku.matrix_height, Sudoku.block_height))
        # look for block without value in set of blocks in uberrow
        block_range = block_id[:]
        for i in block_range:
            block = self.blocks[i]
            if value in block:
                block_id.remove(i)
                index_value_adjacentblocks.append(block.index(value))
        if len(block_id) == 1:
            i = block_id[0]
            selected_block = self.blocks[i]
        # find empty cells in block
        if selected_block is not None:
            emptycells = self.__getverticalblocksemptycells(selected_block, i, index_value_adjacentblocks, value)
            for j in emptycells:
                updated = self.setmatrixvalue(i, j, value, startfromblockcoordinates=True)
                # if updated:
                #     self.__processblockramifications(i, value)

    def __processblockramifications(self, block_i, value):
        self.__pocesshorizontalblockrow(block_i, value)

    def __processdoubleemptycellsbyrow(self, bag: list, check_bag: list):
        self.__changes = 0  # reset change tracking
        for i, section in enumerate(bag):
            if section.count(0) == 2:
                missing_values = list(set(section).symmetric_difference(Sudoku.base_number_set_with_zero))
                emptycells = Mylist([idx for idx, item in enumerate(section) if item == 0])
                pair_match = [[False, False], [False, False]]
                #       a   b :missing_values
                # aa    T/F T/F
                # bb    T/F T/F
                # :emptycells
                if len(missing_values) == len(emptycells):
                    for x, val in enumerate(missing_values):
                        for y, j in enumerate(emptycells):
                            match = val in check_bag[j]
                            pair_match[x][y] = match

                v1: int = missing_values[0]
                v2: int = missing_values[1]
                j1: int = emptycells[0]
                j2: int = emptycells[1]

                # first value not contained only in right
                if pair_match[0][0] and not pair_match[0][1]:
                    # second value not contained in left
                    if not pair_match[1][0] and pair_match[1][1]:
                        # assign where not cpntained
                        self.setmatrixvalue(i, j1, v2, insert_check_overwrite=True)
                        self.setmatrixvalue(i, j2, v1, insert_check_overwrite=True)
                # first value not contained only in left
                elif not pair_match[0][0] and pair_match[0][1]:
                    # secpond value not contained only in right
                    if pair_match[1][0] and not pair_match[1][1]:
                        # assign where not cpntained
                        self.setmatrixvalue(i, j2, v1)
                        self.setmatrixvalue(i, j1, v2)

    def __processdoubleemptycellsbycolumn(self, bag: list, check_bag: list):
        self.__changes = 0  # reset change tracking
        for j, section in enumerate(bag):
            if section.count(0) == 2:
                missing_values = list(set(section).symmetric_difference(Sudoku.base_number_set_with_zero))
                emptycells = Mylist([idx for idx, item in enumerate(section) if item == 0])
                pair_match = [[False, False], [False, False]]
                #       a   b :missing_values
                # aa    T/F T/F
                # bb    T/F T/F
                # :emptycells
                if len(missing_values) == len(emptycells):
                    for x, val in enumerate(missing_values):
                        for y, i in enumerate(emptycells):
                            match = val in check_bag[i]
                            pair_match[x][y] = match

                v1: int = missing_values[0]
                v2: int = missing_values[1]
                i1: int = emptycells[0]
                i2: int = emptycells[1]

                # first value not contained only in right
                if pair_match[0][0] and not pair_match[0][1]:
                    # second value not contained in left
                    if not pair_match[1][0] and pair_match[1][1]:
                        # assign where not cpntained
                        self.setmatrixvalue(i1, j, v2, insert_check_overwrite=True)
                        self.setmatrixvalue(i2, j, v1, insert_check_overwrite=True)
                # first value not contained only in left
                elif not pair_match[0][0] and pair_match[0][1]:
                    # secpond value not contained only in right
                    if pair_match[1][0] and not pair_match[1][1]:
                        # assign where not cpntained
                        self.setmatrixvalue(i2, j, v1)
                        self.setmatrixvalue(i1, j, v2)


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
