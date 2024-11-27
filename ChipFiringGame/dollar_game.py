import sys
from graph_generator import import_graph, generate_graph
from game_solver import solve_graph

graph_file = sys.argv[1]

graph = generate_graph(import_graph(graph_file))
print(graph)

solution = solve_graph(graph)
if solution: print(solution)
else: print('No Solution')