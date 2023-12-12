"""
Team 4 project
git: 
"""

import csv
import random
import string
import pandas as pd

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
            if len(row) != 4:
                continue
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

def generate_random_color():
    return random.choice(['red', 'green', 'blue'])

def generate_random_vertex():
    return ''.join(random.choices(string.ascii_uppercase, k=1))

def generate_random_edge(vertices):
    vertex1 = random.choice(vertices)
    vertex2 = random.choice([v for v in vertices if v != vertex1])
    return vertex1, vertex2

def generate_graph_csv(num_vertices, num_edges, output_file):
    vertices = [generate_random_vertex() for _ in range(num_vertices)]
    edges = [generate_random_edge(vertices) for _ in range(num_edges)]

    data = []
    for edge in edges:
        color1, color2 = generate_random_color(), generate_random_color()
        data.append((edge[0], edge[1], color1, color2))

    df = pd.DataFrame(data, columns=['Vertex1', 'Vertex2', 'Color1', 'Color2'])
    df.to_csv(output_file, index=False)
    
if __name__ == 'main':
    print(generate_graph_csv(1000, 20000, 'large_graph.csv'))