def is_valid_graph(values):
    for v in values:
        if v < 0:
            return False
    return True

def simulate_move(graph, move):
    edges, values = graph
    new_values = values[:]

    for node in edges[move]:
        new_values[node] += 1
    new_values[move] -= len(edges[move])

    return new_values

def solve_graph(graph):
    moves = [0 for _ in range(len(graph[1]))]
    edges, values = graph
    if(is_valid_graph(values)):
        return moves
    
    graph_queue = [(values, moves)]

    while graph_queue:
        node_values, node_moves = graph_queue.pop(0)

        for v in range(len(node_values)):
            if node_values[v] > 0:
                new_values = simulate_move((edges, node_values), v)
                new_moves = node_moves[:]
                new_moves[v] += 1

                if is_valid_graph(new_values):
                    return new_moves

                graph_queue.append((new_values, new_moves))
    
    return []
