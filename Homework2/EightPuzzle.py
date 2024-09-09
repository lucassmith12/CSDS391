'''
Lucas Smith
CSDS391: Intro to AI
Case ID: ljs174
Homework 1 Submission
'''
import random
import sys

class EightPuzzle: 
    #define our grid as a 3D matrix, with entries representing numbers in the grid
    #0 represents blank space
    
    def __init__(self):
        self.grid = list()
        
    #Helper: finds indices of blank (0) as a list
    def blank(self):   
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 0:
                    return [i,j]   
        print('Error: blank not found')
        return IndexError


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
            if str(num) not in args:
                return f'Missing number: {num}'
            
        return 'Valid'
        
            



    #sets state of the grid. Expects nine entries, otherwise throws error
    def set_state(self, args):
        self.grid = list()

        validity = self.validate_args(args)
        if validity != 'Valid':
            return 'Error' + validity

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
        

    #Moves tile into blank space depending on direction
    #Equivalent to moving blank space in opposite direction
    def move(self, direction):
        #check if grid exists
        
        if len(self.grid) !=3:
            print('Grid is not populated')
            return IndexError
        

        err = TypeError
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
                return err
            self.grid[row][col] = self.grid[row][col-1]
            self.grid[row][col-1] = 0
            
        
        elif move == 'left': 
            #but blank is on the right
            if col == 2:
                print('Illegal move left')
                return err
            self.grid[row][col] = self.grid[row][col+1]
            self.grid[row][col+1] = 0
            
        
        else: 
            print((move))
            print('Error: Direction not recognized')
            return ValueError

        return self.grid
    
    #make n random moves to create a solvable puzzle
    def scramble_state(self, n):
        #reset state
        self.set_state(1,2,3,4,5,6,7,8,0)
        
        #0 = up, 1 = down, 2 = left, 3 = right
        moves = [0,1,2,3]
        
        #start unable to move up or left since 0 is bottom right
        moves.remove(0)
        moves.remove(2)

        #after each move, must determine new possible moves
        for i in range(n):
            
            possible_moves = []
            blank = self.blank()
            if blank is None:
                return None
            row, col = blank
            # Identify possible moves based on the blank's position
            if row > 0:
                possible_moves.append('down')
            if row < 2:
                possible_moves.append('up')
            if col > 0:
                possible_moves.append('right')
            if col < 2:
                possible_moves.append('left')

            # Perform a random move
            move = random.choice(possible_moves)
            self.move(move)
    
        return 'Scrambled successfully'




    #parses text into running commands. Here is where I implement comment checking    
    def cmd(self, txt):
        if '#' in txt or '//' in txt:
            return 0
        
        words = txt.lower()
        words = words.replace('\n', '')
        words = words.split(' ')
         
       
        if 'setstate' == words[0].lower():
            status = self.set_state(words[1:])
            return status == 'Success'
                
            
            
       
        elif 'printstate' == words[0].lower():
            self.print_state()
            

        elif 'move' == words[0].lower():
            try:
                self.move(words[1])
                
            except TypeError:
                print('Error: Invalid Move')
            except IndexError:
                print('Error: Trying to make move before grid has been initialized')

        elif 'scramblestate' == words[0]:
            
            self.scramble_state(int(words[1]))
            
        else:
            print('Invalid Command: ')
            print(words)
            return TypeError
        
        
    
        
#parses commands and runs each one
def cmdfile(file, puzzle):
    with open(file) as text:
        cmds = text.readlines()
        num_line = 0
        for command in cmds:
            num_line += 1
            try:
                puzzle.cmd(command)
            except ValueError:
                print('ValueError on line: ' + str(num_line))
            except TypeError:
                print('TypeError on line: ' + str(num_line))
            
        
   
#runs commands from text input file
def main(args, puzzle):
    cmdfile(args, puzzle)

if __name__ == '__main__':
    #kudos to you if you know this number
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
    



        
        
    