import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithm import *

class GuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Task 2 - MST Finder')
        self.root.geometry('1000x600')
        self.root.configure(background='#E5E5E5')

        self.title = tk.Label(root, text="Minimum Spanning Tree Finder", fg="#4B4D4E", font=("Dongle", 20))
        self.title.place(x=300, y=25)

        self.textEditor = tk.Frame(root, bg="white", width=300, height=300)
        self.textEditor.pack_propagate(0)
        self.textEditor.place(x=50, y=100)

        self.textScroll = tk.Scrollbar(self.textEditor)
        self.textScroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.myText = tk.Text(self.textEditor, width=97, height=25, font=("Dongle", 12), undo=True, yscrollcommand=self.textScroll.set)
        self.myText.insert(tk.END, 
                    "0 4 0 0 0 0 0\n4 0 1 3 0 0 0\n0 1 0 2 0 0 0\n0 3 2 0 1 0 0\n0 0 0 1 0 2 0\n0 0 0 0 2 0 3\n0 0 0 0 0 3 0")
                    # "1 0 1 0 1\n0 0 1 1 0\n1 1 0 1 0\n1 1 0 0 0\n0 0 0 1 0")
                    # "0 1 2 0 0\n1 0 0 3 0\n2 0 0 6 5\n0 3 6 0 4\n0 0 5 4 0")
        self.myText.pack()

        self.textScroll.config(command=self.myText.yview)

        fig, ax = plt.subplots()

        self.graph_frame = tk.Frame(self.root, bg="white", width=550, height=400)
        self.graph_frame.pack_propagate(0)
        self.graph_frame.place(x=400, y=100)

        self.canvas = self.create_graph_canvas(self.graph_frame)
        graph_data = self.createGraph(self.retrieve_input())
        self.drawGraph(graph_data, self.canvas)

        self.saveButton = tk.Button(root, text="Save", fg="#4B4D4E", bg="white", bd=5, command=lambda:[self.retrieve_input(), self.drawGraph(self.createGraph(self.retrieve_input()), self.canvas)], font=("Dongle", 12), cursor='hand2')
        self.saveButton.place(x=150, y=425)

        self.solveButton = tk.Button(root, text="Solve", fg="#4B4D4E", bg="white", bd=5, command=self.toggle_algorithm, font=("Dongle", 12), cursor='hand2')
        self.solveButton.place(x=200, y=475)

        self.algorithmToggle = tk.Button(text="Kruskal", fg="#4B4D4E", bg="white", bd=5, command=self.selectAlgorithm, font=("Dongle", 12), cursor='hand2')
        self.algorithmToggle.place(x=100, y=475)

    def retrieve_input(self):
        input_text = self.myText.get(1.0, "end-1c")
        rows = input_text.strip().split('\n')
        inputList = [list(map(int, row.split())) for row in rows]
        return inputList

    def createGraph(self, adjM):
        edges = []
        noofvertices = len(adjM)
        for mat in adjM:
            if len(mat) > noofvertices or len(mat) < noofvertices:
                print("False Adjacency Matrix")
                return 0
        for i in range(len(adjM)):
            mat = adjM[i]
            for j in range(len(mat)):
                if mat[j] != 0:
                    temp = [i, j]
                    edges.append(temp)
        G = nx.Graph()
        G.add_edges_from(edges)
        return G

    def create_graph_canvas(self, frame):
        canvas = FigureCanvasTkAgg(plt.figure(), frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        return canvas

    def drawGraph(self, graph, canvas):
        plt.clf()  # Clear the previous graph from the plot
        pos = nx.spring_layout(graph, seed=42)
        nx.draw(graph, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=12, font_weight='bold',
                ax=plt.gca())
        canvas.draw()  # Redraw the updated graph

    def toggle_algorithm(self):
        graph_data = np.array(self.retrieve_input())
        if graph_data is None:
            return
        if self.algorithmToggle.config('text')[-1] == "Prim":
            mst = prim(graph_data.copy())
        else:
            mst = kruskal(graph_data.copy())
        self.drawGraph(mst, self.canvas)
    
    def selectAlgorithm(self):
        if self.algorithmToggle.config('text')[-1] == 'Kruskal':
            self.algorithmToggle.config(text='Prim')
        else:
            self.algorithmToggle.config(text='Kruskal')


def run_gui():
    root = tk.Tk()
    app = GuiApp(root)
    root.mainloop()