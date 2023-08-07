import networkx as nx
import numpy as np

def prim(graph):
    n = len(graph)
    selected_nodes = {0}
    num_selected = 1
    mst = nx.Graph()
    
    while num_selected < n:
        min_distance = float('inf')
        new_node = None
        selected_node = None

        for node in selected_nodes:
            for i in range(n):
                if i not in selected_nodes and graph[node][i] > 0 and graph[node][i] < min_distance:
                    min_distance = graph[node][i]
                    new_node = i
                    selected_node = node

        selected_nodes.add(new_node)
        num_selected += 1
        mst.add_edge(selected_node, new_node, weight=min_distance)
    
    return mst

def kruskal(graph):
    n = len(graph)
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            if graph[i][j] > 0:
                edges.append((i, j, graph[i][j]))
    
    edges.sort(key=lambda x: x[2])
    mst = nx.Graph()
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x == root_y:
            return False
        if rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
        elif rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            parent[root_y] = root_x
            rank[root_x] += 1
        return True

    for edge in edges:
        u, v, weight = edge
        if union(u, v):
            mst.add_edge(u, v, weight=weight)

    return mst