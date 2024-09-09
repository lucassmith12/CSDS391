'''
Lucas Smith
CSDS391: Intro to AI
Case ID: ljs174
Homework 2 Submission
'''
import EightPuzzle


goal = [[0,1,2],[3,4,5],[6,7,8]]
def bfs(original_puzzle, max_nodes=1000):
    nodes = 1
    if original_puzzle.grid == goal:
        return print_results(original_puzzle.ancestors, nodes)
   
    puzzle = EightPuzzle()
    puzzle.copy(original_puzzle)
    queue = list()

    queue.append(puzzle)
    while len(queue) != 0:
        node = queue.pop()
        for move in node.find_moves():
            nodes +=1
            queue.append(move)
            child = EightPuzzle()
            child.copy(node)
            child.ancestors.append(move)
            if child.grid == goal:
                return child.ancestors
            elif nodes >= max_nodes:
                return 'Error'
            
            
#Runs recursive dfs on a puzzle
def dfs(original_puzzle, max_nodes=1000):
    puzzle = EightPuzzle()
    puzzle.copy(original_puzzle) 
    status = dfs_helper(puzzle, max_nodes, 1)
    
    if status == 'Error':
        print(f'Error: maxnodes limit ({max_nodes}) reached')
        return 'Error'
    elif status > 0 :
        print('Solution Found')
        return 'Success'
    else: 
        print('Error occurred')



def dfs(original_puzzle, max_nodes=1000):
    node = EightPuzzle()
    node.copy(original_puzzle) 
    if max_nodes== 0:
        print('Error: maxnodes limit reached, search terminated')
    if node.grid == goal:
        print('Solution Found')
        return print_results(list(), 1)
    else:
        results = dfs_helper(original_puzzle, max_nodes, 1)
        return print_results(results[0],results[1])


#recursive caller for dfs
def dfs_helper(puzzle, max, nodes):
    if nodes > max:
        return 'Error'
    elif puzzle.grid == goal:
        return ['Found']
    
    queue = puzzle.find_moves()
    for move in queue:
        nodes +=1
        child = EightPuzzle()
        child.copy(puzzle)
        child.move(move)
        subtree = dfs_helper(child, max, nodes)
        if subtree == 'Error':
            return 'Error'
        elif subtree[0] == 'Found':
            return (subtree.append(move), nodes)
        
        queue.append(child.find_moves())
    
def print_results(ancestors, nodes):
    print(f'Nodes created during search: {nodes}')
    print(f'Solution length: {len(ancestors)}')
    print('Solution:')
    for ancestor in ancestors:
        print(ancestor)
