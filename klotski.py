import copy
import numpy
from math import inf, nan, isnan
from event import Event

def manhattan_distance(position1, position2):
    return numpy.sum(list(map(abs, numpy.subtract(position1, position2))))


def closest_heuristic(table):
    return manhattan_distance(table.desired_position, table.get_block(table.goalblock).position)


def most_extreme_position(positions):
    extreme = (inf, inf)
    for position in positions:
        if position[1] < extreme[1]:
            extreme = position
        elif position[1] == extreme[1] and position[0] < extreme[0]:
            extreme = position
    
    return extreme

def update_blocks(block):
    for block_index in block.table.blocks:
        block.table.blocks[block_index].available_movements = \
            block.table.blocks[block_index].all_movements()


def character_to_code(character, characters):
    if(character == '-'):
        return nan  # wall

    if(character == '+'):
        return inf  # goal

    if(character == '.'):
        return 0  # empty

    if not character in characters:  # new block
        characters[character] = (len(characters) - 5)//2 + 1

    return characters[character]  # block


def create_block(index, character, shape, table):
    minX = minY = inf
    maxX = maxY = 0

    for (y, x) in shape:  # find boundaries
        if x < minX:
            minX = x
        if x > maxX:
            maxX = x
        if y < minY:
            minY = y
        if y > maxY:
            maxY = y

    w = maxX - minX + 1
    h = maxY - minY + 1

    # logical 2D array representing shape filled with false (not taken)
    s = [[False for x in range(w)] for y in range(h)]
    for (y, x) in shape:  # fill taken positions with true
        s[y-minY][x-minX] = True

    return KlotskiBlock(index, character, minX, minY, w, h, s, table)


def position_is_free(index, x, y, width, height, shape, table):
    # print('index: {}; x: {}; y: {}; width: {}; height: {}'
    #       .format(index, x, y, width, height))

    for b in range(height):
        for a in range(width):
            if y+b >= table.height or x+a >= table.width:
                return False

            # print(table[y+b][x+a])
            # print('Remove: {}'.format(shape[b][a] and not (  # this space in our shape is empty
            #         table[y+b][x+a] == 0 or  # this space on the table is empty
            #         # this space is taken by us (our old position)
            #         table[y+b][x+a] == index or
            #         table[y+b][x+a] == inf and table.goalblock == index)))
            # if neither is true from following:
            if shape[b][a] and not (  # this space in our shape is empty
                    table[y+b][x+a] == 0 or  # this space on the table is empty
                    # this space is taken by us (our old position)
                    table[y+b][x+a] == index or
                    table[y+b][x+a] == inf and table.goalblock == index):  # this space on the table is goal space and we are the goal block
                return False  # return false

    # print(shape)
    # print('valid position: {}'.format({'index': index, 'x': x, 'y': y}))
    return True


def find_one_from_position(index, x, y, width, height, shape, table):
    ret = set([])
    # print((y, x))
    x1 = x
    for y1 in range(max(y-1, 0), min(y+2, table.height)):  # vertical positions
        # print('position {}'.format((y1, x1)))
        if y1 != y and position_is_free(index, x1, y1, width, height, shape, table):
            ret.add((y1, x1))

    y1 = y
    for x1 in range(max(x-1, 0), min(x+2, table.width)):  # horizontal positions
        # print('position {}'.format((y1, x1)))
        if x1 != x and position_is_free(index, x1, y1, width, height, shape, table):
            ret.add((y1, x1))

    return ret


class KlotskiBlock:
    def __init__(self, index, character, x, y, width, height, shape, table, copy=False):
        self.index = index
        self.character = character
        self.x = x
        self.y = y
        self.position = (y, x)
        self.width = width
        self.height = height
        self.shape = shape
        self.table = table
        if not copy:
            self.available_movements = self.all_movements()

    def by_one_movements(self):
        return find_one_from_position(
            self.index,
            self.x,
            self.y,
            self.width,
            self.height,
            self.shape,
            self.table)

    def all_movements(self):
        # print()
        origin = (self.y, self.x)
        # print('{}'.format(self.index))
        ret = self.by_one_movements()  # get movements by one position
        # print(ret)
        new = ret  # they are all new
        while len(new) > 0:  # while there are new (unexplored) positions
            accessible = set([])

            for (y, x) in new:  # get all positions reachable from these positions by one movement
                accessible |= find_one_from_position(
                    self.index, x, y, self.width, self.height, self.shape, self.table)

            new = accessible - ret  # new positions that we didn't explore yet are equal to the difference of all positions and already explored positions
            ret |= new  # set new positions as already explored

        ret -= set([origin])
        # print(self.index)
        # print(ret)
        return ret
    

    def copy(self, table):
        block = KlotskiBlock(
            self.index, self.character,
            self.x, self.y, self.width, self.height,
            self.shape, table, copy=True)

        block.available_movements = self.available_movements
        return block


class KlotskiTable:
    def __init__(self, filename):
        if filename != None:
            self.loadtable(filename)

        self.on_solved = Event()
        self.on_block_move = Event()
        self.heuristic = closest_heuristic

        self.on_block_move.append(lambda block: update_blocks(block))


    def __getitem__(self, index):
        if type(index) is int:
            return self.table[index]

        if type(index) is tuple:
            return self.table[index[0]][index[1]]

        raise Exception(
            "Expected integer or tuple but got {}.".format(type(index)))


    def __str__(self):
        digits = 1
        while 10 ^ digits < len(self.blocks):
            digits += 1

        ret = []
        for i in range(len(self.table)):
            ret.append(' ; '.join(['{0:3.0f}'.format(x)
                                   for x in self.table[i]]))

        return '\n'.join(ret)


    def __ge__(self, other):
        return self.heuristic(self) >= self.heuristic(other)
    

    def __gt__(self, other):
        return self.heuristic(self) >  self.heuristic(other)

    
    def __le__(self, other):
        return self.heuristic(self) <= self.heuristic(other)

    
    def __lt__(self, other):
        return self.heuristic(self) <  self.heuristic(other)


    def __eq__(self, other):
        return str(self) == str(other)

    
    def __ne__(self, other):
        return str(self) != str(other)


    def set_heuristic(self, heuristic):
        self.heuristic = heuristic


    def get_block(self, index):
        return self.blocks[index]


    def is_solved(self):
        goalblock = self.get_block(self.goalblock)  # get the goal block

        for y in range(goalblock.height):  # for its height
            for x in range(goalblock.width):  # for its width
                if (goalblock.y + y, goalblock.x + x) not in self.goalpositions and goalblock.shape[y][x]:
                    return False  # if the "pixel" of the block is not in any of goal positions, return False

        self.on_solved(self)

        return True


    def get_move_heuristic_value(self, block_index, position):
        block = self.get_block(block_index)
        if not position in block.available_movements:
            raise Exception("Movement to position not available.")

        (blocky, blockx) = position
        for y in range(block.height):
            for x in range(block.width):
                if block.shape[y][x]:
                    # clear my position
                    self.table[block.y + y][block.x +
                                            x] = inf if self.original_table[block.y + y][block.x + x] == inf else 0

        for y in range(block.height):
            for x in range(block.width):
                if block.shape[y][x]:
                    self.table[blocky + y][blockx +
                                           x] = block.index  # set new position

        position = block.position
        block.y = blocky
        block.x = blockx
        block.position = (y, x)

        heuristic_value = self.heuristic(self)

        (blocky, blockx) = position
        for y in range(block.height):
            for x in range(block.width):
                if block.shape[y][x]:
                    # clear my position
                    self.table[block.y + y][block.x +
                                            x] = inf if self.original_table[block.y + y][block.x + x] == inf else 0

        for y in range(block.height):
            for x in range(block.width):
                if block.shape[y][x]:
                    self.table[blocky + y][blockx +
                                           x] = block.index  # set new position

        block.y = blocky
        block.x = blockx
        block.position = (y, x)

        return heuristic_value

    def move_block(self, block_index, position):
        block = self.get_block(block_index)
        if not position in block.available_movements:  # is position reachable?
            raise Exception("Movement to position not available.")

        (blocky, blockx) = position
        for y in range(block.height):
            for x in range(block.width):
                if block.shape[y][x]:
                    # clear my position
                    self.table[block.y + y][block.x +
                                            x] = inf if self.original_table[block.y + y][block.x + x] == inf else 0

        for y in range(block.height):
            for x in range(block.width):
                if block.shape[y][x]:
                    self.table[blocky + y][blockx +
                                           x] = block.index  # set new position

        block.y = blocky
        block.x = blockx
        block.position = (block.y, block.x)

        self.on_block_move(block)


    def loadtable(self, filename):
        with open(filename) as f:
            lines = f.readlines()  # file is short so it's ok
            parts = lines[0].split()  # split sizes
            height = int(parts[0])  # height of table
            width = int(parts[1])  # width of table
            goalpositions = set([])  # empty set of goal positions

            # init table (all positions non-reachable -- walls)
            table = [[nan for x in range(width)] for y in range(height)]
            characters = { nan: '-', inf: '+', '.': 0, 0: '.', '-': nan, '+': inf }
            for y in range(height):
                for x in range(width):
                    # translate characters into digits
                    table[y][x] = character_to_code(lines[y+1][x], characters)
                    characters[table[y][x]] = lines[y+1][x]
                    if(lines[y+1][x] == '+'):  # goal position
                        goalpositions.add((y, x))

            # read which block should end in goal position
            goalblock = character_to_code(lines[len(lines) - 1], characters)

            self.goalpositions = goalpositions
            self.goalblock = goalblock
            self.width = width
            self.height = height
            self.table = table
            self.original_table = copy.deepcopy(table)
            self.filename = filename
            self.characters = characters
            self.desired_position = most_extreme_position(goalpositions)

            shapes = {}  # shapes of blocks represented as logical 2D array
            for y in range(height):
                for x in range(width):
                    if table[y][x] != 0 and table[y][x] != inf and not isnan(table[y][x]):
                        if table[y][x] not in shapes:
                            shapes[table[y][x]] = set([])

                        shapes[table[y][x]].add((y, x))

            blocks = {index: create_block(index, self.characters[index], shapes[index], self)
                      for index in shapes}  # create blocks from shapes

            self.blocks = blocks

    def copy(self):
        table = KlotskiTable(None)
        
        table.goalpositions = self.goalpositions
        table.goalblock = self.goalblock
        table.width = self.width
        table.height = self.height
        table.original_table = self.original_table
        table.filename = self.filename
        table.characters = self.characters
        table.desired_position = self.desired_position

        table.table = copy.deepcopy(self.table)
        table.blocks = { index: self.blocks[index].copy(table) for index in self.blocks }

        return table
