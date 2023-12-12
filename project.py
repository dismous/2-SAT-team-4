"""
Team 4 project
git: 
"""
import time
import csv
import random
import string
import pandas as pd

def timer(func):
    """
    timer decorator to time the execution of a function.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time} seconds to run.")
        return result
    return wrapper

def read_graph_from_file(file_path):
    """
    Reads a graph from a file and returns a dictionary.
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

def dfs(graph, start_node):
    """
    Perform a depth-first search (DFS) on a graph from a given node.

    Args:
        graph (dict): The graph to search.
        start_node (str): The node to start the search from.

    >>> graph = {'A': ['B', 'C'], 'B': ['A', 'D', 'E'], 'C': ['A', 'F'], 'D': ['B'], 'E': ['B', 'F'], 'F': ['C', 'E']}
    >>> dfs(graph, 'A')
    ['A', 'C', 'F', 'E', 'B', 'D']
    """
    visited = set()
    stack = [start_node]
    result = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            result.append(node)
            stack.extend(graph[node])

    return result

def kosaraju(graph, inv_graph):
    """
    Use of kosaaju's algorithm to find the strongly connected components of a graph.

    >>> graph = {1: [2], 2: [3], 3: [1, 4], 4: [5], 5: [6], 6: [4]}
    >>> inv_graph = {1: [3], 2: [1], 3: [2], 4: [3, 6], 5: [4], 6: [5]}
    >>> kosaraju(graph, inv_graph)
    [[4, 5, 6], [1, 2, 3]]
    """
    order = []
    visited = set()
    for node in graph:
        if node not in visited:
            order.extend(dfs(graph, node)[::-1])
    sccs = []
    visited = set()
    for node in reversed(order):
        if node not in visited:
            scc = dfs(inv_graph, node)
            visited.update(scc)
            sccs.append(scc)
    return sccs

def successful_coloring(graph):
    """
    Determine if a successful coloring of the graph is possible.

    Args:
        graph (dict): The graph to color.

    Returns:
        bool: True if a successful coloring is possible, False otherwise.
    """
    for vertex, data in graph.items():
        color = data['color']
        for neighbor in data['neighbors']:
            if graph[neighbor]['color'] == color:
                return False
    return True

def generate_random_color():
    """
    Generate a random color from the [red, green, blue].

    >>> random.seed(1)
    >>> generate_random_color()
    'blue'
    """
    return random.choice(['red', 'green', 'blue'])

def generate_random_vertex():
    """
    Generate a random vertex name consisting of 5 alphanumeric characters.

    >>> random.seed(1)
    >>> generate_random_vertex()
    'K1L5T'
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def generate_random_edge(vertices):
    """
    Generate a random edge between two distinct vertices.

    Args:
        vertices (list): The list of vertices to choose from.

    >>> random.seed(1)
    >>> generate_random_edge(['A', 'B', 'C', 'D', 'E'])
    ('E', 'B')
    """
    vertex1 = random.choice(vertices)
    vertex2 = random.choice([v for v in vertices if v != vertex1])
    return vertex1, vertex2

@timer
def generate_graph_csv(num_vertices, num_edges, output_file):
    """
    Generate a random graph and write it to a CSV file.

    Args:
        num_vertices (int): The number of vertices in the graph.
        num_edges (int): The number of edges in the graph.
        output_file (str): The path to the output file.

    >>> random.seed(1)
    >>> generate_graph_csv(3, 3, 'test.csv')
    """
    vertices = [generate_random_vertex() for _ in range(num_vertices)]
    edges = [generate_random_edge(vertices) for _ in range(num_edges)]

    data = []
    for edge in edges:
        color1, color2 = generate_random_color(), generate_random_color()
        data.append((edge[0], edge[1], color1, color2))

    df = pd.DataFrame(data, columns=['Vertex1', 'Vertex2', 'Color1', 'Color2'])
    df.to_csv(output_file, index=False)
    
if __name__ == '__main__':
    generate_graph_csv(1000, 20000, 'large_graph_res.csv')
    graph = read_graph_from_file('large_graph.csv')
    print(successful_coloring(graph))