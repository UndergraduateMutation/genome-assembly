import argparse

import DeBruijnGraph
import file_io

parser = argparse.ArgumentParser(
    description="Assemble genome reads into contigs",
    prog="genome_assembly"
)
parser.add_argument(
    "-r",
    "--reads",
    required=True,
    help="Input file",
)
parser.add_argument(
    "-t",
    "--target",
    help="Output file",
)
parser.add_argument(
    "-p",
    "--plot",
    action="store_true",
    help="Plot DeBruijn graph",
)

if __name__ == "__main__":
    args = parser.parse_args()

    reads = file_io.read_file_content(args.reads).strip().splitlines()
    max_read_length = max(len(read) for read in reads)

    graph = DeBruijnGraph.DeBruijnGraph(reads)
    contigs = [path for path in graph.get_maximum_non_branching_paths() if len(path) > max_read_length]

    output = "".join(f">Contig {i}\n{contig}\n" for (i, contig) in enumerate(contigs))
    if(args.target is None):
        print(output)
    else:
        print(f"Contig number: {len(contigs)}")
        print(f"Total contig length: {sum(len(contig) for contig in contigs)}")
        file_io.write_to_file(args.target, output)
        print(f"Output written to {args.target}")

    if(args.plot):
        graph.plot()
