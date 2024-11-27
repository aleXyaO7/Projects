def import_graph(graph_file):
    with open(graph_file) as f:
        graph_inputs = f.read().split('\n')
    return graph_inputs

def generate_graph(graph_inputs):
    n = int(graph_inputs[0])
    edges = [[] for _ in range(n)]
    values = [int(i) for i in graph_inputs[1].split(' ')]
    
    for edge_value in graph_inputs[2:]:
        temp_edges = edge_value.split(' ')
        a = int(temp_edges[0])

        for b in temp_edges[1:]:
            edges[a].append(int(b))

    return (edges, values)
