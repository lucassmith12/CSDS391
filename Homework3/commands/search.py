from collections import deque
from copy import deepcopy
from puzzle import EightPuzzle


goal = [[0,1,2],[3,4,5],[6,7,8]]
def bfs(original_puzzle, max_nodes: 1000):
    nodes = 1
    if original_puzzle.grid == goal:
        return print_results(original_puzzle.ancestors, nodes)
   
    puzzle = deepcopy(original_puzzle)
    queue = deque()

    queue.append(puzzle)
    while len(queue) != 0:
        node = queue.popleft()
        for move in node.find_moves():
            nodes +=1
            
            child = deepcopy(node)
            child.ancestors.append(' '.join(['move', move]))
            child.move(move)
            if child.grid == goal:
                return print_results(child.ancestors, nodes)
            elif nodes >= max_nodes:
                return 'Error'
            else:
                queue.append(deepcopy(child))


#Runs recursive dfs on a puzzle
def dfs(original_puzzle, max_nodes=1000):
    puzzle = deepcopy(original_puzzle) 
    results = dfs_helper(puzzle, max_nodes, 1)
    
    if results == 'Error':
        print(f'Error: maxnodes limit ({max_nodes}) reached')
        return 'Error'
    elif type(results) is type(list()):
        print('Solution Found')
        return print_results(results[0],results[1])
    else: 
        print('Error occurred')



#recursive caller for dfs
def dfs_helper(puzzle, max, nodes):
    if nodes > max:
        return 'Error'
    elif puzzle.grid == goal:
        return ['Found']
    
    stack = puzzle.find_moves()
    for move in stack:
        nodes +=1
        child = EightPuzzle()
        child.copy(puzzle)
        child.move(move)
        subtree = dfs_helper(child, max, nodes)
        if subtree == 'Error':
            return 'Error'
        elif subtree[0] == 'Found':
            return (subtree.append(move), nodes)
        
        
#Format search results    
def print_results(ancestors, nodes):
    print(f'Nodes created during search: {nodes}')
    print(f'Solution length: {len(ancestors)}')
    print('Solution:')
    for ancestor in ancestors:
        print(ancestor)
    return 'Success'