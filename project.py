"""
Recoloring given colored graph using 2-SAT
"""
from typing import Dict, List, Tuple
import networkx as nx
import matplotlib.pyplot as plt

def csv_to_graph(path: str) -> Tuple[Dict[int, List[int]], Dict[int, int]]:
    """
    Parses a CSV file to generate a graph and a corresponding color mapping.
    Parameters:
        path (str): The file path for the CSV file.
    Returns:
        Tuple[Dict[int, List[int]], Dict[int, int]]: A graph represented as an adjacency list,
        along with a dictionary mapping nodes to their colors.
    """
    graph = {}
    node_colors = {}
    with open(path, "r", encoding="utf-8") as file:
        for record in file:
            node1, node2, color_node1, color_node2 = map(int, record.strip().split(",")[:4])
            transformed_node1 = (node1 + 1) * 3
            transformed_node2 = (node2 + 1) * 3

            if transformed_node1 not in graph:
                graph[transformed_node1] = []
            graph[transformed_node1].append(transformed_node2)
            node_colors[transformed_node1] = color_node1

            if transformed_node2 not in graph:
                graph[transformed_node2] = []
            graph[transformed_node2].append(transformed_node1)
            node_colors[transformed_node2] = color_node2

    return graph, node_colors


def transform_to_cnf(graph: Dict[int, List[int]], colors: Dict[int, int]) -> List[List[int]]:
    """
    Returns conjunctive normal form of future colors of graph vertices.
    Args:
        graph (Dict[int, List[int]]): The old graph.
        colors (Dict[int, int]): The old colors.
    Returns:
        List[List[int]]: The conjunctive form of new coloring.
    """
    cnf = []
    for vert in graph:
        new_colors = [0, 1, 2]
        new_colors.remove(colors[vert])
        cnf.append([vert + new for new in new_colors])
        cnf.append([-(vert + new) for new in new_colors])
        for adj_vert in graph[vert]:
            for new_color in new_colors:
                if colors[adj_vert] != new_color and [-(adj_vert \
                                                        + new_color), -(vert + new_color)] not in cnf:
                    cnf.append([-(vert + new_color), -(adj_vert + new_color)])
    return cnf


def implication_graph(cnf: List[List[int]]) -> Dict[int, List[int]]:
    """
    Transforms disjunctions into implications and returns an oriented graph.
    Args:
        cnf (List[List[int]]): The CNF.
    Returns:
        Dict[int, List[int]]: The implication graph.
    """
    imp_graph = {}
    for (a, b) in cnf:
        if -a not in imp_graph:
            imp_graph[-a] = [b]
        else:
            if b not in imp_graph[-a]:
                imp_graph[-a].append(b)
        if -b not in imp_graph:
            imp_graph[-b] = [a]
        else:
            if a not in imp_graph[-b]:
                imp_graph[-b].append(a)
    return imp_graph


def reverse_graph(imp_graph: Dict[int, List[int]]) -> Dict[int, List[int]]:
    """
    Returns the transpose of the given directed graph.
    Args:
        imp_graph (Dict[int, List[int]]): The implication graph.
    Returns:
        Dict[int, List[int]]: The transposed graph.
    """
    reversed_graph = {}
    for vert in imp_graph:
        for adj_vert in imp_graph[vert]:
            if adj_vert not in reversed_graph:
                reversed_graph[adj_vert] = [vert]
            else:
                reversed_graph[adj_vert].append(vert)
    return reversed_graph


def dfs(imp_graph: Dict[int, List[int]], start: int, visited: List[int]) -> List[int]:
    """
    Performs depth-first search on the graph and returns the list of vertices.
    Args:
        imp_graph (Dict[int, List[int]]): The implicated graph.
        start (int): The vertex from which to start the DFS.
        visited (List[int]): The visited vertices.
    Returns:
        List[int]: The DFS result.
    """
    path = []
    stack = [start]
    dfs_graph = {}
    for vertice in imp_graph:
        dfs_graph[vertice] = sorted(imp_graph[vertice])
    while len(stack) != 0:
        clear_stack = True
        vert = stack[-1]
        if vert not in path:
            visited.append(vert)
            path.append(vert)
        if vert in dfs_graph:
            dfs_graph[vert] = [adj for adj in dfs_graph[vert] if adj not in visited]
            if len(dfs_graph[vert]) != 0:
                stack.append(dfs_graph[vert][0])
                clear_stack = False
        if clear_stack:
            stack.pop()
    return path


def find_scc(graph: Dict[int, List[int]]) -> List[List[int]]:
    """
    Performs DFS from each vertex in the graph and returns the list of strongly connected components.
    Args:
        graph (Dict[int, List[int]]): The direct implication graph.
    Returns:
        List[List[int]]: The list of strongly connected components.
    """
    result = []
    visited = []
    order = []
    for vert1 in graph.keys():
        if vert1 not in visited:
            order.extend(dfs(graph, vert1, visited))
    new_visited = []
    for vert2 in list(reversed(order)):
        if vert2 not in new_visited:
            result.append(dfs(reverse_graph(graph), vert2, new_visited))
    return result


def recolor_graph(graph: Dict[int, List[int]], colors: Dict[int, int]) -> List[Tuple[int, int]]:
    """
    Recolors the graph using 2-SAT algorithm.
    Args:
        graph (Dict[int, List[int]]): The graph from the CSV file.
        colors (Dict[int, int]): The coloring of the graph from the CSV file.
    Returns:
        List[Tuple[int, int]]: The new coloring.
    """
    cnf = transform_to_cnf(graph, colors)
    imp_graph = implication_graph(cnf)
    scc_list = list(find_scc(imp_graph))
    new_graph = {}
    for scc in list(reversed(scc_list)):
        if len(list(map(abs, scc))) != len(set(list(map(abs, scc)))):
            return "No solution"
        for vert_color in list(reversed(scc)):
            if len(new_graph) == len(graph):
                break
            if abs(vert_color) // 3 - 1 not in new_graph:
                if vert_color > 0:
                    new_graph[vert_color // 3 - 1] = vert_color % 3
                else:
                    new_color = [color for color in [0, 1, 2] if color not in [abs(vert_color) % 3, colors[abs(vert_color) - abs(vert_color) % 3]]]
                    new_graph[abs(vert_color) // 3 - 1] = new_color[0]
    return sorted(list(new_graph.items()))



if __name__ == "__main__":
    graph, colors = csv_to_graph('graph.csv')
    print(recolor_graph(graph, colors))
