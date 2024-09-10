Note for the dfs and bfs, the addition of the maxnodes parameter 
must come as is described in the assignment, e.g.
max_nodes=1000

The following will cause an error:
max_nodes= 1000
max_nodes =1000
max_nodes 1000
1000

Not including the solve in front of bfs/dfs will also cause
an error.

Raw DFS with no state checking does not solve the problem, so it will
run infinitely. Running it for 1000 nodes exceeds recursion depth.
Set it for 100 instead, it will do the same thing but not crash.

As with the last assignment, both terminal commands and file 
inputs will work

Thanks!