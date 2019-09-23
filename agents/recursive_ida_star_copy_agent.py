import numpy
from klotski import KlotskiTable
from random import randint
from math import inf
from enum import Enum


def manhattan_distance(position1, position2):
    return numpy.sum(list(map(abs, numpy.subtract(position1, position2))))


def manhattan_heuristic(table):
    return manhattan_distance(table.desired_position, table.get_block(table.goalblock).position)


class Agent:
    def __init__(self):
        self.timeout = False

    def set_timeout(self):
        self.timeout = True

    def get_move(self, table):
        moves = self.solve(table)
        if len(moves) == 0:
            moves = []
            while len(moves) == 0:
                block_index = randint(1, len(table.blocks))
                block = table.get_block(block_index)
                moves = list(block.available_movements)

            move_index = randint(0, len(moves)-1)
            move = moves[move_index]
            return {
                'block': block_index,
                'position': move
            }

        return moves[0]

    def search(self, path, depth, bound):
        node = path[len(path) - 1][0]
        self.visited += 1

        if node.is_solved():
            return 0

        if self.timeout:
            return inf

        f = depth + 1
        if f > bound:
            return f

        m = inf
        items = []

        for block in node.blocks:
            if self.timeout:
                return inf

            block = node.get_block(block)
            op = block.position

            for move in block.available_movements:
                if self.timeout:
                    return inf

                p = move
                neighbor = node.copy()
                neighbor.move_block(block.index, move)
                s = str(neighbor)

                if any([str(table) == s for (table, _) in path]):
                    continue

                items.append((neighbor, {'block': block.index, 'position': p,
                                         'original_position': op}, depth + manhattan_heuristic(neighbor)))

        items.sort(key=lambda x: x[2])
        
        for item in items:
            path.append((item[0], item[1]))

            t = self.search(path, depth + 1, bound)
            if t == 0:
                return 0
            if t < m:
                m = t

            path.pop()

        return m

    def solve(self, table):
        if type(table) is not KlotskiTable:
            raise TypeError()

        table.heuristic = manhattan_heuristic
        self.timeout = False
        self.visited = 0

        bound = 1

        while not self.timeout:
            path = [(table, None)]
            result = self.search(path, 0, bound)

            if result == 0:
                break

            if result == inf:
                return {'moves': [], 'visited': self.visited}

            bound += 1

        moves = [move for (_, move) in path if move != None]
        return {'moves': moves, 'visited': self.visited}
