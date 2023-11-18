import igraph as ig
import matplotlib.pyplot as plt

def reverse_complement(read: str) -> str:
    complement = {"a": "t", "t": "a", "c": "g", "g": "c", "A": "T", "T": "A", "C": "G", "G": "C"}
    return "".join(complement[base] for base in read[::-1])

def split_reads(reads: list[str], k: int) -> list[str]:
    new_reads = []
    for read in reads:
        for i in range(len(read) - k + 1):
            new_reads.append(read[i:i+k])
    return new_reads

def preprocess_reads(reads: list[str], splits_per_read: int, use_reverse_complement: bool) -> list[str]:
    if(use_reverse_complement):
        reads += list(map(reverse_complement, reads))
    reads = split_reads(reads, splits_per_read)
    return reads

class DeBruijnGraph():
    def __init__(self, input_reads: list[str], splits_per_read: int, use_reverse_complement: bool):
        self.graph = ig.Graph(directed=True)

        reads = preprocess_reads(input_reads, splits_per_read, use_reverse_complement)
        reads = split_reads(input_reads, min(len(read) for read in input_reads) - splits_per_read)

        suffix_vertices = set(read[1:] for read in reads)
        prefix_vertices = set(read[:-1] for read in reads)
        edges = ((read[:len(read) - 1], read[1:]) for read in reads)
        self.graph.add_vertices(list(prefix_vertices | suffix_vertices))
        self.graph.add_edges(edges)
    
    def get_maximum_non_branching_paths(self) -> list[str]:
        def dfs(vertex: ig.Vertex, path: list[ig.Vertex]) -> list[ig.Vertex]:
            while vertex.outdegree() == 1:
                path.append(vertex)
                vertex = vertex.successors()[0]
                marked.add(vertex.index)

            path.append(vertex)
            return path

        def assemble_path(path: list[ig.Vertex]) -> str:
            return path[0]["name"] + "".join([vertex["name"][-1] for vertex in path[1:]])
        
        def vertex_is_branching(vertex: ig.Vertex) -> bool:
            return vertex.indegree() != 1 or vertex.outdegree() != 1

        paths: list[list[ig.Vertex]] = []
        marked = set()

        for vertex in self.graph.vs:
            if vertex.index not in marked and vertex_is_branching(vertex):
                path = dfs(vertex, [])
                paths.append(path)

        return [assemble_path(path) for path in paths]
    
    def plot(self):
        self.graph.vs["label"] = self.graph.vs["name"]
        ax = plt.subplot()
        ig.plot(self.graph, target=ax, backend="matplotlib")
        plt.show()
