from puzzle import EightPuzzle
from .search import dfs, bfs
import random

#parses text into running commands.     
def cmd(puzzle, txt):
    
    
    words = txt.lower()
    words = words.replace('\n', '')
    words = words.split(' ')
    for word in words:
        if word == '' or word == '\n' or word == '\t':
            words.remove(word)
    
    command = words[0].lower()
    
    if 'setstate' == command:
        status = puzzle.set_state(words[1:])
        
    
    elif 'printstate' == command:
        status = puzzle.print_state()
                    
    elif 'move' == command:
        status = puzzle.move(words[1])
            
        if status == 'MoveErr':
            print('Error: Invalid Move')
            return 'Error'
        elif status ==  'GridErr':
            print('Error: Trying to make move before grid has been initialized')
            return 'Error'
        elif status == 'DirErr':
            print('Error: Illegal move direction')
            return 'Error'

    elif 'scramblestate' == command:
        if len(words) != 2:
            print('Error: incorrect number of arguments passed')
            status = 'Error'
        else:
            status = puzzle.scramble_state(int(words[1]))
        
    elif 'solve' == command:
        algo = words[1]
        max = 1000
        if len(words) > 2:
            max = int(words[2].split('=')[1])
        
        if algo == 'dfs':
            status =  dfs(puzzle, max_nodes=max) 
        elif algo == 'bfs':
            status =  bfs(puzzle, max_nodes=max)
        else:
            print('Error: unknown search command')
            return 'Error'
    else:
        print(f'Invalid Command: {command}')
        return 'Error'
    
    print(command, ': ', status)
    return status
    