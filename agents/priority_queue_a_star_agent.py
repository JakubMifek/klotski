import copy
import numpy
from random import randint
from sortedcollections import SortedList
from math import inf


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

    
    def reconstruct_path(self, came_from, target):
        moves = []
        while target in came_from:
            pred = came_from[target]
            moves.append(pred[1])
            target = pred[0]

        return list(reversed(moves))


    def solve(self, table):
        table.heuristic = manhattan_heuristic
        self.timeout = False

        visited = 0
        closed_states = set([])
        came_from = {} # for path reconstruction
        gscores = { str(table): 0 }
        open_states = SortedList(key=lambda key: 1000000-key[0])
        open_states.add((0, table))

        while len(open_states) > 0 and not self.timeout:
            current = open_states.pop()[1]
            c = str(current)
            visited += 1

            if current.is_solved():
                return { 'moves': self.reconstruct_path(came_from, c), 'visited': visited }
            
            closed_states.add(c)
            gscore = gscores[c]

            for block in current.blocks:
                if self.timeout:
                    break

                block = current.get_block(block)
                for move in block.available_movements:
                    if self.timeout:
                        break

                    #neighbor = current.copy()
                    neighbor = copy.deepcopy(current)
                    neighbor.heuristic = manhattan_heuristic
                    neighbor.move_block(block.index, move)
                    #simulate_movement(neighbor, block.index, move)
                    
                    n = str(neighbor)

                    if n in closed_states:
                        continue

                    tenative_gscore = gscore + 1
                    tenative_fscore = tenative_gscore + neighbor.heuristic(neighbor)

                    if not any(state == neighbor for (fscore, state) in open_states):
                        open_states.add((tenative_fscore, neighbor))
                    elif tenative_gscore >= gscores[n]:
                        continue
                    
                    came_from[n] = (c, { 'block': block.index, 'position': move })
                    gscores[n] = tenative_gscore

        return { 'moves': [], 'visited': visited }