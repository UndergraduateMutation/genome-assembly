def find_overlap(read1, read2, min_length):
    """Find the length of the longest suffix of 'read1' matching a prefix of 'read2'."""
    start = 0

    while True:
        start = read1.find(read2[:min_length], start)
        if start == -1:
            return 0

        if read1[start:] == read2[:len(read1) - start]:
            return len(read1) - start
        start += 1

def overlap_map(reads, min_length):
    """Build a map of overlaps."""
    overlap_graph = {}
    for read_a in reads:
        for read_b in reads:
            if read_a != read_b:
                overlap_length = find_overlap(read_a, read_b, min_length)
                if overlap_length > 0:
                    overlap_graph[(read_a, read_b)] = overlap_length
    return overlap_graph

def construct_layout(overlap_graph):
    """Construct a simple layout from the overlap graph."""
    read_order = []
    while overlap_graph:
        max_overlap = 0
        for pair, overlap in overlap_graph.items():
            if overlap > max_overlap:
                max_overlap = overlap
                chosen_pair = pair
        read_order.append(chosen_pair[0])
        del overlap_graph[chosen_pair]
    read_order.append(chosen_pair[1])  # Add the last read
    return read_order

def generate_consensus(read_order, overlap_graph):
    """Generate a consensus sequence from the ordered reads."""
    consensus = read_order[0]
    for i in range(1, len(read_order)):
        overlap = overlap_graph.get((read_order[i-1], read_order[i]), 0)
        consensus += read_order[i][overlap:]
    return consensus

def load_reads(file_path):
    """Load reads from a file."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def main():
    reads = load_reads("path_to_your_reads_file.txt")
    min_overlap_length = 3
    overlaps = overlap_map(reads, min_overlap_length)

    read_order = construct_layout(overlaps)

    consensus_sequence = generate_consensus(read_order, overlaps)

    print("Read Order:", read_order)
    print("Consensus Sequence:", consensus_sequence)

if __name__ == "__main__":
    main()
