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


    #sets state of the grid. Expects nine entries, otherwise throws error
    def set_state(self, *args):
        #check validity of args
        try:
            self.validate_grid(args)
        except:
            return TypeError
            



        #slice the args into three rows
        
        top_row = list(args[:3])
        middle_row = list(args[3:6])
        bottom_row = list(args[6:])
        

        #add each row to construct the matrix
        self.grid.append(top_row)
        self.grid.append(middle_row)
        self.grid.append(bottom_row)

        return self.grid

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
        #check if grid is populated
        if len(self.grid) !=9:
            return IndexError
        
        err = TypeError
        move = direction.lower()
        
        #get coords of blank tile
        blank = self.blank()
        
        if move == 'up':
            #but blank is on the bottom
            
            if blank[0] == 2:
                return err
            self.grid[blank[0]][blank[1]] = self.grid[blank[0]+1][blank[1]]
            self.grid[blank[0]+1][blank[1]] = 0
            
        elif move == 'down':
            #but blank is on the top
            if blank[0]==0:
                return err
            self.grid[blank[0]][blank[1]] = self.grid[blank[0]-1][blank[1]]
            self.grid[blank[0]-1][blank[1]] = 0
        
        elif move == 'right':
            #but blank is on the left
            
            if blank[1] == 0:
                return err
            self.grid[blank[0]][blank[1]] = self.grid[blank[0]][blank[1]-1]
            self.grid[blank[0]][blank[1]-1] = 0
        
        elif move == 'left': 
            #but blank is on the right
            if blank[1] == 2:
                return err
            self.grid[blank[0]][blank[1]] = self.grid[blank[0]][blank[1]+1]
            self.grid[blank[0]][blank[1]+1] = 0
            
        
        else: 
            print('Error: Direction not recognized')
            return ValueError

        self.print_state()
    
    #make n random moves to create a solvable puzzle
    def scramble_state(self, n):
        #reset state
        self.set_state(1,2,3,4,5,6,7,8,0)
        
        #flags to keep track of legal moves
        row = 2
        col = 2

        #0 = up, 1 = down, 2 = left, 3 = right
        moves = [0,1,2,3]
        #start unable to move up or left since 0 is bottom right
        moves.remove(0)
        moves.remove(2)

        #after each move, must add new possible moves and remove new impossible ones
        for i in range(n):
            
            randnum = random.randint(0,len(moves)-1)

            if moves[randnum]==0:
                
                self.move('up')
                col -=1
                if 1 not in moves:
                    moves.insert(1,1)
                if col == 0:
                    moves.remove(0)

            elif moves[randnum]==1:
                
                self.move('down')
                col+=1
                if 0 not in moves:
                    moves.insert(0,0)
                if col == 2:
                    moves.remove(1)

            elif moves[randnum]==2:
                
                self.move('left')
                row-=1
                if 3 not in moves:
                    moves.insert(3,3)
                if row == 0:
                    moves.remove(2)

            elif moves[randnum]==3:
                
                self.move('right')
                row+=1
                if 2 not in moves:
                    moves.insert(2,2)
                if row == 2:
                    moves.remove(3)
        self.print_state()
        return 'Scrambled successfully'




    #parses text into running commands. Here is where i implement comment checking    
    def cmd(self, txt):
        txtlwr = txt.lower()
        words = txtlwr.split(' ')
        if '#' in words or '//' in words:
            return 0 
       
        elif 'setstate' in words:
            try:
                self.set_state(*words[1:])
            except ValueError:
                print('Error: invalid state')
       
        elif 'printstate' in words:
            self.print_state()

        elif 'move' in words:
            try:
                self.move(words[1])
                
            except TypeError:
                print('Error: Invalid Move')
            except IndexError:
                print('Error: Trying to make move before grid has been initialized')

        elif 'scramblestate' in words:
            self.scramble_state(int(words[1]))
        else:
            return ValueError
        
        
    #Helper: finds indices of blank (0) as a list
    def blank(self):   
        for i in range(0,2):
            for j in range(0,2):
                if self.grid[i][j] == 0:
                    return [i,j]   


    #Helper: validates that a new grid fits our specifications
    def validate_grid(self, new_grid):
        if type(new_grid) is not type(list):
            return TypeError
        if len(new_grid) != 3:
            return TypeError
        for row in new_grid:
            if len(row) != 3:
                return TypeError
        missing_arg = True
        for ints in range(0,9):
            if ints not in new_grid:
                missing_arg = True
        if(len(new_grid) !=9 and not missing_arg):
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
                print('Error on line: ' + str(num_line))
            except TypeError:
                print('Error on line: ' + str(num_line))
   
#runs commands from text input file
def main(args):
    return cmdfile(args, EightPuzzle())

if __name__ == '__main__':
    main(sys.argv[1])
    



        
        
    