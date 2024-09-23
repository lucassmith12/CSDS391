from puzzle import EightPuzzle
from .search import dfs, bfs, a_star

#parses text into running commands.     
def cmd(puzzle, txt):
    
    commands = parse_cmd(txt)
    command = commands[0]
    params = commands[1:]
    status = 'Error'
    if 'setstate' == command:
        status = puzzle.set_state(params)
        
    elif 'printstate' == command:
        status = puzzle.print_state()
                    
    elif 'move' == command:
        status = process_move(puzzle, params)

    elif 'scramblestate' == command:
        if len([params]) != 2:
            print('Error: incorrect number of arguments passed')
            status = 'Error'
        else:
            status = puzzle.scramble_state(int(params[0]))
        
    elif 'solve' == command:
        algo = params[0]
        nodes = 1000
        heuristic = None
        for index in range(1,len(params)):
            if 'nodes=' in params[index]:
                nodes = int(params[index].split('=')[1])
            elif 'h1' in params[index]:
                heuristic = 'h1'
            elif 'h2' in params[index]:
                heuristic = 'h2'
            else: 
                print('Error in solve method')
                return 'Error'
            
        status = search(puzzle, algo, nodes, heuristic)
        
    else:
        print(f'Invalid Command: {command}')
        return 'Error'
    
    print(command, ': ', status)
    return status
    

def parse_cmd(txt):
    words = txt.lower()
    words = words.replace('\n', '')
    words = words.split(' ')
    for word in words:
        if word == '' or word == '\n' or word == '\t':
            words.remove(word)
    
    return words

def process_move(puzzle, params):
    status = puzzle.move(params[0])
    if status == 'MoveErr':
        print('Error: Invalid Move')
        return 'Error'
    elif status ==  'GridErr':
        print('Error: Trying to make move before grid has been initialized')
        return 'Error'
    elif status == 'DirErr':
        print('Error: Illegal move direction')
        return 'Error'
    else:
        return status 
    
def search(puzzle, algo, nodes, heuristic):
    if algo == 'dfs':
        status =  dfs(puzzle, max_nodes=nodes) 
    elif algo == 'bfs':
        status =  bfs(puzzle, max_nodes=nodes)
    elif algo == 'a*':
        status = a_star(puzzle, heuristic, max_nodes=nodes)
    else:
        print('Error: unknown search command')
        status = 'Error'
    return status
