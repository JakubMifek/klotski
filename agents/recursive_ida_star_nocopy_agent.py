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

    def search(self, table, path, depth, bound):
        self.visited += 1

        f = depth + manhattan_heuristic(table)
        if f > bound:
            return f

        if table.is_solved():
            return 0

        if self.timeout:
            return inf

        m = inf
        items = []
        goalblock = table.goalblock

        for block in table.blocks:
            if self.timeout:
                return inf

            if len(path) > 0 and block == path[-1]['block']:
                continue

            block = table.get_block(block)
            for move in block.available_movements:
                if self.timeout:
                    return inf

                items.append(({'block': block.index, 'position': move, 'original_position': block.position}, depth + (
                    manhattan_distance(move, table.desired_position) if block.index == table.goalposition else table.heuristic(table))))

        items.sort(key=lambda x: x[1], reverse=True)

        for item in items:
            b = item[0]['block']
            p = item[0]['position']
            op = item[0]['original_position']

            path.append(item[0])
            table.move_block(b, p)

            t = self.search(table, path, depth +
                            manhattan_distance(p, op), bound)
            if t == 0:
                return 0
            if t < m:
                m = t

            table.move_block(b, op)
            path.pop()

        return m

    def solve(self, table):
        if type(table) is not KlotskiTable:
            raise TypeError()

        table.heuristic = manhattan_heuristic
        self.timeout = False
        self.visited = 0

        bound = manhattan_heuristic(table)
        path = []

        while not self.timeout:
            result = self.search(table, path, 0, bound)

            if result == 0:
                break

            if result == inf:
                return {'moves': [], 'visited': self.visited}

            bound = result

        moves = [move for move in path if move != None]
        return {'moves': moves, 'visited': self.visited}
