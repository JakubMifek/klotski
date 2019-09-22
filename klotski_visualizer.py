import sys
from klotski import KlotskiTable

def print_table(block):
    print(block.table)


def console(filename):
    table = KlotskiTable(filename)
    table.on_block_move.append(print_table)
    print(table)
    return table

def show_moves(filename):
    table = console(filename)
    goalblock = table.get_block(table.goalblock)
    print('Goalblock movements:')
    print(goalblock.available_movements)
    print('Goal position:')
    print(table.goalpositions)


switch = {
    'console': console,
    'show_moves': show_moves
#    'window': window
}


def main():
    mode = 'console'
    filename = 'input.klotski'

    if len(sys.argv) > 1:
        filename = sys.argv[1]

        if len(sys.argv) > 2:
            mode = sys.argv[2]

    switch[mode](filename)


if __name__ == '__main__':
    main()