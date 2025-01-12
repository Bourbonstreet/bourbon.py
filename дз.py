import time
from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def kosaraju(self):
        def dfs(v, visited, stack):
            visited[v] = True
            for neighbor in self.graph[v]:
                if not visited[neighbor]:
                    dfs(neighbor, visited, stack)
            stack.append(v)

        def dfs_transposed(v, visited, component):
            visited[v] = True
            component.append(v)
            for neighbor in transposed_graph[v]:
                if not visited[neighbor]:
                    dfs_transposed(neighbor, visited, component)

        # Step 1: Fill the stack in order of finishing times
        stack = []
        visited = [False] * self.vertices
        for i in range(self.vertices):
            if not visited[i]:
                dfs(i, visited, stack)

        # Step 2: Transpose the graph
        transposed_graph = defaultdict(list)
        for u in self.graph:
            for v in self.graph[u]:
                transposed_graph[v].append(u)

        # Step 3: Process vertices in reverse order of the stack
        visited = [False] * self.vertices
        strongly_connected_components = []

        while stack:
            v = stack.pop()
            if not visited[v]:
                component = []
                dfs_transposed(v, visited, component)
                strongly_connected_components.append(component)

        return strongly_connected_components

    def tarjan(self):
        def strongconnect(v):
            nonlocal index
            indices[v] = lowlink[v] = index
            index += 1
            stack.append(v)
            on_stack[v] = True

            for neighbor in self.graph[v]:
                if indices[neighbor] == -1:
                    strongconnect(neighbor)
                    lowlink[v] = min(lowlink[v], lowlink[neighbor])
                elif on_stack[neighbor]:
                    lowlink[v] = min(lowlink[v], indices[neighbor])

            if lowlink[v] == indices[v]:
                component = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    component.append(w)
                    if w == v:
                        break
                strongly_connected_components.append(component)

        index = 0
        indices = [-1] * self.vertices
        lowlink = [-1] * self.vertices
        on_stack = [False] * self.vertices
        stack = []
        strongly_connected_components = []

        for v in range(self.vertices):
            if indices[v] == -1:
                strongconnect(v)

        return strongly_connected_components

# Test the algorithms
def test_algorithms():
    graph = Graph(5)
    graph.add_edge(0, 2)
    graph.add_edge(2, 1)
    graph.add_edge(1, 0)
    graph.add_edge(0, 3)
    graph.add_edge(3, 4)

    print("Kosaraju's Algorithm Output:", graph.kosaraju())
    print("Tarjan's Algorithm Output:", graph.tarjan())

# Benchmarking the algorithms
def benchmark():
    import matplotlib.pyplot as plt

    def generate_large_graph(vertices, edges):
        import random
        graph = Graph(vertices)
        for _ in range(edges):
            u = random.randint(0, vertices - 1)
            v = random.randint(0, vertices - 1)
            graph.add_edge(u, v)
        return graph

    vertices = [10, 100, 1000, 5000, 10000]
    edges = [20, 200, 2000, 10000, 50000]
    kosaraju_times = []
    tarjan_times = []

    for v, e in zip(vertices, edges):
        graph = generate_large_graph(v, e)

        start = time.time()
        graph.kosaraju()
        kosaraju_times.append(time.time() - start)

        start = time.time()
        graph.tarjan()
        tarjan_times.append(time.time() - start)

    plt.plot(vertices, kosaraju_times, label="Kosaraju")
    plt.plot(vertices, tarjan_times, label="Tarjan")
    plt.xlabel("Number of Vertices")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Algorithm Performance Comparison")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    test_algorithms()
    benchmark()
