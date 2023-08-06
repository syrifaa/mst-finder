from tkinter import *
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = Tk()
root.title('Task 2 - MST Finder')
root.geometry('1000x600')
root.configure(background='#E5E5E5')

textEditor = Frame(root, bg="white", width=300, height=300)
textEditor.pack_propagate(0)
textEditor.place(x=50, y=100)

textScroll = Scrollbar(textEditor)
textScroll.pack(side=RIGHT, fill=Y)

myText = Text(textEditor, width=97, height=25, font=("Dongle", 12), undo=True, yscrollcommand=textScroll.set)
myText.insert(END, 
            "0 4 0 0 0 0 0\n4 0 1 3 0 0 0\n0 1 0 2 0 0 0\n0 3 2 0 1 0 0\n0 0 0 1 0 2 0\n0 0 0 0 2 0 3\n0 0 0 0 0 3 0")
            # "1 0 1 0 1\n0 0 1 1 0\n1 1 0 1 0\n1 1 0 0 0\n0 0 0 1 0")
            # "0 1 2 0 0\n1 0 0 3 0\n2 0 0 6 5\n0 3 6 0 4\n0 0 5 4 0")
myText.pack()

textScroll.config(command=myText.yview)

def retrieve_input():
    input = myText.get(1.0,"end-1c")
    # inputList = [elements.split() for elements in input.strip().split("\n")]
    rows = input.strip().split('\n')
    inputList = [list(map(int, row.split())) for row in rows]
    return inputList

def createGraph(adjM):
    edges=[]
    noofvertices=len(adjM)
    for mat in adjM:
        if len(mat)>noofvertices or len(mat)<noofvertices:
            print("False Adjacency Matrix")
            return 0
    for i in range(len(adjM)):
        mat=adjM[i]
        for j in range(len(mat)):
            if mat[j]!=0:
                temp=[i,j]
                edges.append(temp)
    G=nx.Graph()
    G.add_edges_from(edges)
    nx.draw_networkx(G)
    return G

fig, ax = plt.subplots()

def drawGraph(graph, canvas):
    ax.clear()
    pos = nx.spring_layout(graph, seed=42)
    nx.draw(graph, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=12, font_weight='bold', ax=ax)
    canvas.draw()


def create_graph_canvas(frame):
    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    return canvas

def prim_mst(graph):
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

def kruskal_mst(graph):
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

def toggle_algorithm():
    graph_data = np.array(retrieve_input())
    if graph_data is None:
        return
    if algorithmToggle.config('text')[-1] == "Prim":
        mst = prim_mst(graph_data.copy())
    else:
        mst = kruskal_mst(graph_data.copy())
    drawGraph(mst, canvas)

graph = Frame(root, bg="white", width=550, height=400)
graph.pack_propagate(0)
graph.place(x=400, y=100)

canvas = create_graph_canvas(graph)
drawGraph(createGraph(retrieve_input()), canvas)

saveButton = Button(root, text="Save", fg="#4B4D4E", bg="white", bd=5, command=lambda:[retrieve_input, drawGraph(createGraph(retrieve_input()), canvas)], font=("Dongle", 12), cursor='hand2')
saveButton.place(x=150, y=425)

solveButton = Button(root, text="Solve", fg="#4B4D4E", bg="white", bd=5, command=toggle_algorithm, font=("Dongle", 12), cursor='hand2')
solveButton.place(x=200, y=475)

def selectAlgorithm():
    if algorithmToggle.config('text')[-1] == 'Kruskal':
        algorithmToggle.config(text='Prim')
    else:
        algorithmToggle.config(text='Kruskal')

algorithmToggle = Button(text="Kruskal", fg="#4B4D4E", bg="white", bd=5, command=selectAlgorithm, font=("Dongle", 12), cursor='hand2')
algorithmToggle.place(x=100, y=475)

root.mainloop()