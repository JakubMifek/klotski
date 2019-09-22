import os
import importlib
import copy
from math import inf
from time import time as time
from klotski import KlotskiTable
from threading import Timer

puzzles = 'puzzles'
agents = 'agents'
timelimit = 240

def set_timeout(agent):
    agent.set_timeout()

def verify_solution(table, steps):
    for step in steps:
        table.move_block(step['block'], step['position'])
    
    return table.is_solved()

def run_simulation(agent, puzzle):
    puzzle_path = '{}/{}'.format(puzzles, puzzle)
    agent_path = '{}.{}'.format(agents, '.'.join(agent.split('.')[:-1]))

    print('Running {} at {}...'.format(agent, puzzle))

    table = KlotskiTable(puzzle_path)
    module = importlib.import_module(agent_path)
    agent = getattr(module, 'Agent')()

    result = {
        'time': 0,
        'steps': [],
        'visited': 0,
        'success': False
    }
    
    t = Timer(timelimit, set_timeout, (agent,))

    start_time = time()
    t.start()
    r = agent.solve(table)
    end_time = time()
    t.cancel()

    result['steps'] = r['moves']
    result['visited'] = r['visited']
    
    result['time'] = round(end_time - start_time, 2)
    table = KlotskiTable(puzzle_path)

    result['success'] = verify_solution(table, result['steps'])
    
    print('{0:27s} --> {1}: {2:12s} result with {3:6d} steps in {4:6.2f}s; {5:6d} visited states.'.format(
        agent_path.split('.')[-1],
        puzzle_path.split('/')[-1],
        'Successful' if result['success'] else 'Unsuccessful', 
        len(result['steps']),
        result['time'],
        result['visited']))

    return result


def solve_all_puzzles(agent):
    results = {}
    for puzzle in os.listdir(puzzles):
        results[puzzle] = run_simulation(agent, puzzle)
    
    return results


def run_tournament():
    results = {}
    for agent in os.listdir(agents):
        if agent != '__init__.py' and agent != '__pycache__':
            results[agent] = solve_all_puzzles(agent)

    return results


if __name__ == '__main__':
    #print(run_tournament())
    run_tournament()