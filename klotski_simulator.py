import os
import importlib
import copy
import psutil
import threading
import numpy
import random
from math import inf, nan
import time
from klotski import KlotskiTable
from threading import Timer

puzzles = 'puzzles'
agents = 'agents'
timelimit = 3*60
total = 20

def set_timeout(agent):
    agent.set_timeout()

def verify_solution(table, steps):
    for step in steps:
        table.move_block(step['block'], step['position'])
    
    return table.is_solved()

def measure_usage(result, agent):
    while not agent.finished:
        result['memory'].append(psutil.virtual_memory()[2])
        result['cpu'].append(psutil.cpu_percent())
        time.sleep(0.05)

def run_simulation(agent, puzzle, seed):
    numpy.random.seed(seed)
    random.seed(seed)

    puzzle_path = '{}/{}'.format(puzzles, puzzle)
    agent_path = '{}.{}'.format(agents, '.'.join(agent.split('.')[:-1]))

    print('Running {} at {}; using seed: {}'.format(agent, puzzle, seed))

    table = KlotskiTable(puzzle_path)
    module = importlib.import_module(agent_path)
    agent = getattr(module, 'Agent')()

    result = {
        'time': 0,
        'steps': [],
        'visited': 0,
        'success': False,
        'cpu': [0],
        'memory': [0]
    }
    
    t = Timer(timelimit, set_timeout, (agent,))
    t1 = threading.Thread(target=measure_usage, args=(result,agent))

    agent.finished = False
    t1.start()

    start_time = time.time()
    t.start()
    try:
        r = agent.solve(table)    
    except:
        print('An error occured')
        r = {
            'moves': [],
            'visited': 0,
        }
    end_time = time.time()
    t.cancel()

    agent.finished = True
    t1.join()

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
    print('Max CPU: {}%\nMax Memory: {}%'.format(max(result['cpu']),max(result['memory'])))
    # print(result['steps'])

    return result


def solve_all_puzzles(agent, seed):
    results = {}
    for puzzle in os.listdir(puzzles):
        results[puzzle] = run_simulation(agent, puzzle, seed)
    
    return results


def run_tournament():
    results = {}
    for i in range(total):
        print('______________________')
        print('______ ROUND {:2d} ______'.format(i+1))
        print('______________________')
        seed = random.randint(0, 1000000)
        for agent in os.listdir(agents):
            if agent != '__init__.py' and agent != '__pycache__':
                results[agent] = solve_all_puzzles(agent, seed)

    return results


if __name__ == '__main__':
    #print(run_tournament())
    run_tournament()