'''
Lucas Smith
CSDS391: Intro to AI
Case ID: ljs174
Homework 2 Submission
'''
import random
import sys
import copy
from collections import deque 

class EightPuzzle: 
    #define our grid as a 3D matrix, with entries representing numbers in the grid
    #0 represents blank space
    
    def __init__(self):
        self.grid = list()
        self.ancestors = list()
    
    def copy(self, other):
        self.grid = other.grid
        self.ancestors = other.ancestors
        return self.grid
        
    #Helper: finds indices of blank (0) as a list
    def blank(self):   
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 0:
                    return [i,j]   
        return 'Error: blank not found'


    #Helper: validates that a new grid fits our specifications
    def validate_args(self, args):
        
        #Check type
        if type(args) != type(list()):
            return f'Arguments given are a {type(args)} and not a list'
        
        #Check size
        if len(args) != 9:
            return 'New grid is not the correct length'
        
        #Check for 0-9
        for num in range(0,9):
            if num not in args:
                return f'Missing number: {num}'
            
        return 'Valid'
        
    #returns legal moves from current state    
    def find_moves(self):
        possible_moves = []
        blank = self.blank()
        if blank is None:
            return None
        row, col = blank
        #identify possible moves based on the blank's position
        #priority is left--> right --> up --> down
        if col < 2:
            possible_moves.append('left')
        if col > 0:
            possible_moves.append('right')
        if row < 2:
            possible_moves.append('up')
        if row > 0:
            possible_moves.append('down')
        
        return possible_moves


    #sets state of the grid. Expects nine entries, otherwise throws error
    def set_state(self, str_args):
        self.grid = list()

        #input args are strings, make them ints
        args = [int(arg) for arg in str_args]
       
        #validate
        validity = self.validate_args(args)
        if validity != 'Valid':
            print('Error: ' + validity)
            return 'Error'

        top_row = list(args[:3])
        middle_row = list(args[3:6])
        bottom_row = list(args[6:])

        self.grid.append(top_row)
        self.grid.append(middle_row)
        self.grid.append(bottom_row)
        
            
        return 'Success'

    #print the state of the grid
    def print_state(self):
        string = ''
        for row in self.grid:
            for item in row:
                string += str(item)
                string += ' '
            string += '\n'
        print(string)
        return 'Success'


    #Moves tile into blank space depending on direction
    #Equivalent to moving blank space in opposite direction
    def move(self, direction):
        #check if grid exists
        err = 'MoveErr'

        if len(self.grid) !=3:
            print('Grid is not populated')
            return 'GridErr'
        

        
        move = direction.lower()
        
        #get coords of blank tile
        
        row,col = self.blank()
        if move == 'up':
            #but blank is on the bottom
            
            if row == 2:
                print('Illegal move up')
                return err
            self.grid[row][col] = self.grid[row+1][col]
            self.grid[row+1][col] = 0
            
        elif move == 'down':
            #but blank is on the top
            if row==0:
                print('Illegal move down')
                return err
            self.grid[row][col] = self.grid[row-1][col]
            self.grid[row-1][col] = 0
        
        elif move == 'right':
            #but blank is on the left
            
            if col == 0:
                print('Illegal move right')
                return 'MoveErr'
            self.grid[row][col] = self.grid[row][col-1]
            self.grid[row][col-1] = 0
            
        
        elif move == 'left': 
            #but blank is on the right
            if col == 2:
                print('Illegal move left')
                return 'MoveErr'
            self.grid[row][col] = self.grid[row][col+1]
            self.grid[row][col+1] = 0
            
        
        else: 
            print((move))
            print('Error: Direction not recognized')
            return 'DirErr'

        return self.grid
    
    #make n random moves to create a solvable puzzle
    def scramble_state(self, n):
        #reset state
        self.set_state([0,1,2,3,4,5,6,7,8])
        

        #after each move, must determine new possible moves
        for _ in range(n):
            
            # list of valid moves
            possible_moves = self.find_moves()

            #perform a random move
            move = random.choice(possible_moves)
            self.move(move)
    
        return 'Success'
    


    #parses text into running commands.     
    def cmd(self, txt):
        
        
        words = txt.lower()
        words = words.replace('\n', '')
        words = words.split(' ')
        for word in words:
            if word == '' or word == '\n' or word == '\t':
                words.remove(word)
        
        command = words[0].lower()
       
        if 'setstate' == command:
            status = self.set_state(words[1:])
            
       
        elif 'printstate' == command:
            status = self.print_state()
                        
        elif 'move' == command:
            status = self.move(words[1])
                
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
                status = self.scramble_state(int(words[1]))
            
        elif 'solve' == command:
            algo = words[1]
            max = 1000
            if len(words) > 2:
                max = int(words[2].split('=')[1])
           
            if algo == 'dfs':
                status =  dfs(self, max_nodes=max) 
            elif algo == 'bfs':
                status =  bfs(self, max_nodes=max)
            else:
                print('Error: unknown search command')
                return 'Error'
        else:
            print(f'Invalid Command: {command}')
            return 'Error'
        
        print(command, ': ', status)
        return status
        
#Homework 2 submissions

goal = [[0,1,2],[3,4,5],[6,7,8]]
def bfs(original_puzzle, max_nodes=1000):
    nodes = 1
    if original_puzzle.grid == goal:
        return print_results(original_puzzle.ancestors, nodes)
   
    puzzle = copy.deepcopy(original_puzzle)
    queue = deque()

    queue.append(puzzle)
    while len(queue) != 0:
        node = queue.popleft()
        for move in node.find_moves():
            nodes +=1
            
            child = copy.deepcopy(node)
            child.ancestors.append(' '.join(['move', move]))
            child.move(move)
            if child.grid == goal:
                return print_results(child.ancestors, nodes)
            elif nodes >= max_nodes:
                return 'Error'
            else:
                queue.append(copy.deepcopy(child))
            
            
#Runs recursive dfs on a puzzle
def dfs(original_puzzle, max_nodes=1000):
    puzzle = copy.deepcopy(original_puzzle) 
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
        
#parses commands and runs each one
def cmdfile(file, puzzle):
    with open(file) as text:
        cmds = text.readlines()
        num_line = 0
        for command in cmds:
            if '#' in command or '//' in command:
                print(command)
            else:    
                print('Running ', command)
                num_line += 1
                status = puzzle.cmd(command)
                if status == 'Error':
                    print('Error on line: ', num_line)
                # else continue
                
                
            
#runs commands from text input file
def main(args, puzzle):
    cmdfile(args, puzzle)

if __name__ == '__main__':
    #best number choice, iykyk
    random.seed(8675309)
    puzzle = EightPuzzle()
    if(len(sys.argv)<=1):
        running = True
        while(running):
            choice = input('Enter a command, q to quit:\n')
            if str(choice) == 'q':
                running = False
                break
            puzzle.cmd(choice)
            
    else: 
        main(sys.argv[1], puzzle)
    



        
        
    