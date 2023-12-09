"""
Team 4 project
git: 
"""
import csv

def read_graph_from_file(file_path):
    """
    Read a graph from a file and return a dictionary representation of the graph.
    >>> read_graph_from_file('graph.csv')
    {'A': {'color': 'red', 'neighbors': ['F']},\
 'F': {'color': 'green', 'neighbors': ['A']},\
 'D': {'color': 'purple', 'neighbors': ['G']},\
 'G': {'color': 'blue', 'neighbors': ['D']},\
 'V': {'color': 'red', 'neighbors': ['H']},\
 'H': {'color': 'purple', 'neighbors': ['V']},\
 'Y': {'color': 'yellow', 'neighbors': ['U']},\
 'U': {'color': 'white', 'neighbors': ['Y']}}
    """
    graph = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            vertex1, vertex2, color1, color2 = row
            if vertex1 not in graph:
                graph[vertex1] = {'color': color1, 'neighbors': []}
            if vertex2 not in graph:
                graph[vertex2] = {'color': color2, 'neighbors': []}
            graph[vertex1]['neighbors'].append(vertex2)
            graph[vertex2]['neighbors'].append(vertex1)
    return graph

def successful_coloring(graph):
    """
    Get a successful coloring of the graph.
    >>> successful_coloring(read_graph_from_file('graph.csv'))
    [('A', 'red'), ('F', 'green'), ('D', 'purple'), ('G', 'blue'), ('V', 'red'), ('H', 'purple'), ('Y', 'yellow'), ('U', 'white')]
    """
    coloring = [(vertex, data['color']) for vertex, data in graph.items()]
    for _, data in graph.items():
        color = data['color']
        for neighbor in data['neighbors']:
            if graph[neighbor]['color'] == color:
                return "Coloring doesn't exist"
    return coloring

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())