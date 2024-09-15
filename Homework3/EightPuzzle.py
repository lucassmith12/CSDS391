'''
Lucas Smith
CSDS391: Intro to AI
Case ID: ljs174
Homework 2 Submission
'''
import random
import sys, os

from puzzle import EightPuzzle
from commands import cmd
        
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
                status = cmd(puzzle, command)
                if status == 'Error':
                    print('Error on line: ', num_line)
                # else continue
                
                
#runs commands from text input file
def main(args, puzzle):
    print(os.listdir('.'))
    cmdfile(args, puzzle)

if __name__ == '__main__':
    #best number choice, iykyk
    random.seed(8675309)
   
    
    if(len(sys.argv)<=1):
        running = True
        while(running):
            choice = input('Enter a command, q to quit:\n')
            if str(choice) == 'q':
                running = False
                break
            cmd(EightPuzzle(), choice)
            
    else: 
        main(sys.argv[1], EightPuzzle())
    



        
        
    