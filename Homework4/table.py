# Table printing for exercise 5
from copy import deepcopy
import pandas as pd
from commands import a_star, heuristic1, heuristic2, bfs, dfs, find_branching_factor
from puzzle import EightPuzzle

table_df = pd.DataFrame({
    'Search Cost: Nodes Generated': [],
    'Effective Branching Factor b*:':[],
    'Solution Length': []
})

nodes_df = pd.DataFrame(columns=["DFS","BFS", "A*(h1)", "A*(h2)"])
b_df = pd.DataFrame(columns=["DFS","BFS", "A*(h1)", "A*(h2)"])
sol_df = pd.DataFrame(columns=["DFS","BFS", "A*(h1)", "A*(h2)"])

puzzles = list()
p = EightPuzzle()
p.set_state([0,1,2,3,4,5,6,7,8])
moves = [('up', 'up'), ('left', 'down'), ('left', 'up'), ('right', 'right'), ('down', 'down'), ('left', 'up'), ('left', 'down'), ('right', 'right') ]
for m in moves:
    p.move(m[0])
    p.move(m[1])
    puzzles.append(p)
    p = deepcopy(p)

print('Running algorithms, this may take a while')
dfs_data = [dfs(p, 20000) for p in puzzles]
dfs_df = pd.DataFrame({
    'Nodes': [data[1] for data in dfs_data],
    'b*': [find_branching_factor(data[0], data[1]) for data in dfs_data],
    's': [len(data[0]) for data in dfs_data]

})
print('DFS complete')

bfs_data = [bfs(p, 20000) for p in puzzles]
print(data for data in dfs_data)
bfs_df = pd.DataFrame({
    'Nodes': [point[1] for point in bfs_data],
    'b*': [find_branching_factor(data[0], data[1]) for data in bfs_data],
    's': [len(point[0]) for point in bfs_data]
})
print('BFS complete')


ah1_data = [a_star(p, 'h1', 20000) for p in puzzles]
ah1_df = pd.DataFrame({
    'Nodes': [data[1] for data in ah1_data],
    'b*': [find_branching_factor(data[0], data[1]) for data in ah1_data],
    's': [len(data[0]) for data in ah1_data]
})
print("First A* complete")

ah2_data = [a_star(p, 'h2', 20000) for p in puzzles]
ah2_df = pd.DataFrame({
    'Nodes': [data[1] for data in ah2_data],
    'b*':  [find_branching_factor(data[0], data[1]) for data in ah2_data],
    's': [len(data[0]) for data in ah2_data]
})
print("Second A* complete", '\n')



nodes_df = pd.concat([dfs_df['Nodes'], bfs_df['Nodes'], ah1_df['Nodes'], ah2_df['Nodes']], axis=1)
nodes_df.columns = pd.MultiIndex.from_product([['Search Cost: Nodes Generated'], ['DFS', 'BFS', 'A*(h1)', 'A*(h2)']])

b_df = pd.concat([dfs_df['b*'], bfs_df['b*'], ah1_df['b*'], ah2_df['b*']], axis=1)
b_df.columns = pd.MultiIndex.from_product([['Effective Branching Factor b*'], ['DFS', 'BFS', 'A*(h1)*', 'A*(h2)']])

sol_df = pd.concat([dfs_df['s'], bfs_df['s'], ah1_df['s'], ah2_df['s']], axis=1)
sol_df.columns = pd.MultiIndex.from_product([['Solution Length'], ['DFS', 'BFS', 'A*(h1)', 'A*(h2)']])

table_df = pd.concat([nodes_df, b_df, sol_df], axis=1)
table_df['d']=[2, 4, 6, 8, 10, 12, 14, 16]
pd.set_option('display.max_columns', None)
print(table_df)

table_df.to_csv('table.csv')






