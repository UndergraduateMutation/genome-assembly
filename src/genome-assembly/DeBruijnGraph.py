import igraph as ig
import matplotlib.pyplot as plt

class DeBruijnGraph():
    def __init__(self, reads: list[str]):
        self.graph = ig.Graph(directed=True)
        suffix_vertices = set(read[1:] for read in reads)
        prefix_vertices = set(read[:len(read) - 1] for read in reads)
        edges = ((read[:len(read) - 1], read[1:]) for read in reads)
        self.graph.add_vertices(list(prefix_vertices | suffix_vertices))
        self.graph.add_edges(edges)
    
    def get_maximum_non_branching_paths(self) -> list[str]:
        def vertex_is_branching(vertex: ig.Vertex) -> bool:
            return vertex.indegree() != 1 or vertex.outdegree() != 1
        
        def assemble_path(path: list[ig.Vertex]) -> str:
            return path[0]["name"] + "".join([vertex["name"][-1] for vertex in path[1:]])

        paths: list[list[ig.Vertex]] = []
        for vertex in self.graph.vs:
            if (vertex_is_branching(vertex)):
                for edge in self.graph.es.select(_source=vertex.index):
                    path: list[ig.Vertex] = [vertex]
                    while True:
                        path.append(self.graph.vs[edge.target_vertex.index])
                        if self.graph.vs[edge.target_vertex.index].outdegree() == 1:
                            edge = self.graph.es.select(_source=edge.target_vertex.index)[0]
                        else:
                            break
                    paths.append(path)

        return [assemble_path(path) for path in paths]
    
    def plot(self):
        self.graph.vs["label"] = self.graph.vs["name"]
        ax = plt.subplot()
        ig.plot(self.graph, target=ax, backend="matplotlib")
        plt.show()
