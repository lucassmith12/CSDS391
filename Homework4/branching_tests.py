from commands import find_branching_factor
# represent solutions as a (solution tree, nodes) pair
# since the find branching method takes a list and measures its length,
# we can pass in an arbitrary list of that length and it will work 
# in the same way. 

two_branch = find_branching_factor(range(2), 7) # N+1 = 1 + 2 + 4 = 7, d=2, b* should be 2
three_branch = find_branching_factor(range(3), 40) # N+1 = 1 + 3 + 9 + 27 = 40, d=3, b* should be 3
four_branch = find_branching_factor(range(4), 341) # N+1 = 1 + 4 + 16 + 64 + 256 = 213, d=4, b* should be 4
dfs = find_branching_factor(range(10),11) # N+1 = 1 + 1... + 1 = 11, b* should be 1
print("Expect a b* of 2: ", two_branch)
print("Expect a b* of 3: ",three_branch)
print("Expect a b* of 4: ",four_branch)
print("Expect a b* of 1: ", dfs)
