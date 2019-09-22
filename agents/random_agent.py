from random import randint

class Agent:
    def set_timeout(self):
        self.timeout = True
        return


    def get_move(self, table):
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

    def solve(self, table):
        self.timeout = False
        moves = []
        m = 0
        while not table.is_solved() and not self.timeout:
            move = self.get_move(table)
            moves.append(move)
            table.move_block(move['block'], move['position'])
            m += 1
        
        return { 'moves': moves, 'visited': len(moves) }