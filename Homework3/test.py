# Testing to show heuristic functionality and state checking
# the actual testfile is found in the testcmds.txt

from commands import a_star, heuristic1, heuristic2
#goal state, should be 0 for h1,h2
state1 = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
print('state1:')
print('h1:' , heuristic1( state1)) # 0
print('h2:' , heuristic2( state1)) # 0

#after 5 moves, check heuristics
state2 = [[4, 3, 2], [0, 1, 5], [6, 7, 8]]
print('state2:')
print('h1:' , heuristic1( state2)) #3
print('h2:' , heuristic2( state2)) #5