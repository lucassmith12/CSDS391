import random

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
    #sets state of the grid. Expects nine entries, otherwise throws error
    def set_state(self, str_args):
        self.grid = list()

        #input args are strings, make them ints
        args = [int(arg) for arg in str_args]
        
        #validate
        validity = validate_args(args)
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


#Helper: validates that a new grid fits our specifications
def validate_args(args) -> str:
    
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