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
            return (node.ancestors, nodes)

        
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
        return (original_puzzle.ancestors, nodes)
   
    puzzle = deepcopy(original_puzzle)
    queue = deque()

    queue.append(puzzle)
    while len(queue) != 0:
        if nodes > max_nodes:
            print('Error: max nodes reached')
            return 'Error', max_nodes
        node = queue.popleft()
        for move in node.find_moves():
            nodes +=1
            
            child = deepcopy(node)
            child.ancestors.append(' '.join(['move', move]))
            child.move(move)
            if child.grid == goal:
                return (child.ancestors, nodes)
            elif nodes >= max_nodes:
                print('Error: max nodes reached')
                return 'Error', max_nodes
            else:
                queue.append(deepcopy(child))


def dfs(original_puzzle, max_nodes=1000):
    puzzle = deepcopy(original_puzzle)  
    #build our stack as a list of states defined by the puzzle and the moves to get there
    stack = [(puzzle, [])]  
    visited = set()            
    nodes = 1                  
    while len(stack) != 0:
        current_puzzle, path = stack.pop()

        if nodes > max_nodes:
            print(f'Error: max nodes limit ({max_nodes}) reached')
            return 'Error', max_nodes

        if current_puzzle.grid == goal:
            return path, nodes

        visited.add(linear(current_puzzle.grid))

        for move in current_puzzle.find_moves():
            child_puzzle = deepcopy(current_puzzle)
            child_puzzle.move(move)

            if linear(child_puzzle.grid) not in visited:
                nodes += 1
                stack.append((child_puzzle, path + ['move ' + move] ))

    print('Error: algorithm found no solution')
    return 'Error', nodes
        
def find_branching_factor(depth, nodes):
    # Find N + 1 = b*^0 + b* + b*^2 + b*^3 ... + b*^d
    N=1
    b=0
    while(int(N)<nodes):
        b+=0.01
        N=1
        #don't raise to the 0th power, add one to make range inclusive of root
        for exp in range(1, len(depth)+1): 
            N+=b**exp
    return b



        
#Format search results    
def print_results(ancestors, nodes):
    print(f'Nodes created during search: {nodes}')
    print(f'Solution length: {len(ancestors)}')
    print('Solution:')
    for ancestor in ancestors:
        print(ancestor)
    print(f'Branching factor b* = {find_branching_factor(len(ancestors), nodes)}')
    return 'Success\n'