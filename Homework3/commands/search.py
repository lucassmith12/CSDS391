from collections import deque
from copy import deepcopy
from puzzle import EightPuzzle
from heapq import heapify, heappush, heappop

goal = [[0,1,2],[3,4,5],[6,7,8]]



def a_star(original_puzzle, heur, max_nodes=1000):
    visited = set()
    priority_q = []
    heapify(priority_q)
    nodes = 1

    if heur == 'h1':
        heuristic = heuristic1
    elif heur == 'h2':
        heuristic = heuristic2
    else:
        return 'Error: invalid heuristic'
    #Heap is ordered by heuristic, then move order, then in order they were added to the queue
    heappush(priority_q, (heuristic(original_puzzle.grid)+ len(original_puzzle.ancestors), 
                          -1, nodes, original_puzzle))
    while len(priority_q) != 0 and nodes <= max_nodes:
        node = heappop(priority_q)[3]
        
        if node.grid == goal:
            return print_results(node.ancestors, nodes)

        
        #lists are unhashable, have to use a string of numbers instead
        visited.add(linear(node.grid))

        for move in node.find_moves():
            child = deepcopy(node)
            child.move(move)
            child.ancestors.append(' '.join(['move', move]))
            
            if linear(child.grid) not in visited:
                heappush(priority_q, (heuristic(child.grid) + len(child.ancestors), move_to_num(move), nodes, child))
                nodes +=1
    return 'Error: max nodes reached'

#Helper to convert grid into a string literal of numbers to hash into a set
def linear(grid) -> str:
    string = ''
    for row in grid:
        for item in row:
            string += str(item)
    return string

#returns move order 0 = left, 1=right, 2=up, 3=down to preserve order
def move_to_num(move)-> int:
    if move == 'left': 
        return 0
    elif move == 'right': 
        return 1
    elif move == 'up': 
        return 2
    else: 
        return 3

    
    


def heuristic1(grid) -> int:
    count = 0
    for i in range(3):
        for j in range(3):
            if grid[i][j] != 3*i + j and grid[i][j] != 0:
                count+=1
    return count


def heuristic2(grid) -> int:
    displacement = 0 
    for i in range(3):
        for j in range(3):
            num = grid[i][j] 
            if num != 0:
                #horizontal displacement from goal
                dx = abs((num%3) - j)
                #vertical displacement from goal
                dy = abs((int(num/3)) - i)
                displacement += dx + dy
    return displacement






def bfs(original_puzzle, max_nodes=1000):
    nodes = 1
    if original_puzzle.grid == goal:
        return print_results(original_puzzle.ancestors, nodes)
   
    puzzle = deepcopy(original_puzzle)
    queue = deque()

    queue.append(puzzle)
    while len(queue) != 0:
        if nodes > max_nodes:
            print('Error: max nodes reached')
            return 'Error'
        node = queue.popleft()
        for move in node.find_moves():
            nodes +=1
            
            child = deepcopy(node)
            child.ancestors.append(' '.join(['move', move]))
            child.move(move)
            if child.grid == goal:
                return print_results(child.ancestors, nodes)
            elif nodes >= max_nodes:
                print('Error: max nodes reached')
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
    return 'Success\n'