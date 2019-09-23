import argparse
import re

re_line1 = r"Running\s+(?P<agent>[^\s]+)\s+at\s+(?P<puzzle>[^\s]+);\s+using\s+seed:\s+(?P<seed>\d+)"
re_line2 = r"(?P<agent>[^\s]+)\s+-->\s+(?P<puzzle>[^\s]+):\s+(?P<success>[^\s]+)\s+result\s+with\s+(?P<steps>\d+)\s+steps\s+in\s+(?P<seconds>[^\s]+)s;\s+(?P<states>\d+)\s+visited\s+states."
re_line3 = r"Max\s+CPU:\s+(?P<cpu>[^\s]+)%"
re_line4 = r"Max\s+Memory:\s+(?P<memory>[^\s]+)%"

def process_lines(lines):
    print('Proccessing {} lines'.format(len(lines)))
    i = 0
    results = {}
    while i < len(lines):
        # Running random_agent.py at sample07.klotski; using seed: 228217
        if lines[i].startswith('_'):
            i+=1
            continue

        x = re.search(re_line1, lines[i])
        if x == None:
            print('Pattern not matched.')
            print(re_line1)
            print(lines[i])
            return

        agent, puzzle, _ = x.group('agent', 'puzzle', 'seed')
        if not agent in results:
            results[agent] = {}
        if not puzzle in results[agent]:
            results[agent][puzzle] = {
                'success': 0,
                'unsuccess': 0,
                'steps': 0,
                'seconds': 0,
                'states': 0,
                'runs': 0,
                'cpu': 0,
                'memory': 0
            }

        results[agent][puzzle]['runs'] += 1
        
        i+=1
        # random_agent                --> sample07.klotski: Successful   result with 107555 steps in  46.31s; 107555 visited states.

        x = re.search(re_line2, lines[i])
        if x == None:
            print('Pattern not matched.')
            print(re_line2)
            print(lines[i])
            return
        
        agent2, puzzle2, success, steps, seconds, states = \
            x.group('agent', 'puzzle', 'success', 'steps', 'seconds', 'states')
        if agent != (agent2 + '.py') or puzzle != puzzle2:
            print('Inconsitancy', agent, agent2, puzzle, puzzle2)
            return
        
        if success == 'Successful':
            results[agent][puzzle]['success'] += 1
        else:
            results[agent][puzzle]['unsuccess'] += 1
        results[agent][puzzle]['steps'] += int(steps)
        results[agent][puzzle]['seconds'] += float(seconds)
        results[agent][puzzle]['states'] += int(states)

        i += 1
        # Max CPU: 87.2%

        x = re.search(re_line3, lines[i])
        if x == None:
            print('Pattern not matched.')
            print(re_line3)
            print(lines[i])
            return

        cpu = x.group('cpu')
        results[agent][puzzle]['cpu'] += float(cpu)

        i += 1
        # Max Memory: 20.1%

        x = re.search(re_line4, lines[i])
        if x == None:
            print('Pattern not matched.')
            print(re_line4)
            print(lines[i])
            return

        memory = x.group('memory')
        results[agent][puzzle]['memory'] += float(memory)

        i += 1
    return results


def process_file(path):
    print('Processing {}'.format(path))
    lines = []
    with open(path) as f:
        lines = f.readlines()
    results = process_lines(lines)
    print()
    for agent in results:
        print(agent)
        for puzzle in results[agent]:
            print('\t{}'.format(puzzle))
            print('\t\tSuccess Rate: {}%'.format(100*results[agent][puzzle]['success']/results[agent][puzzle]['runs']))
            print('\t\tAverage Steps: {}'.format(results[agent][puzzle]['steps']//results[agent][puzzle]['runs']))
            print('\t\tAverage Time: {}s'.format(results[agent][puzzle]['seconds']//results[agent][puzzle]['runs']))
            print('\t\tAverage States: {}'.format(results[agent][puzzle]['states']//results[agent][puzzle]['runs']))
            print('\t\tAverage Cpu: {}%'.format(results[agent][puzzle]['cpu']//results[agent][puzzle]['runs']))
            print('\t\tAverage Memory: {}%'.format(results[agent][puzzle]['memory']//results[agent][puzzle]['runs']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process results of simulator")
    parser.add_argument('file', metavar="File", type=str, help='file to process')
    args = parser.parse_args()
    process_file(args.file)
    