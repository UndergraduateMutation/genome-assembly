import argparse
import DeBruijnGraph
import file_io
import time

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
parser.add_argument(
    "--splits",
    type=int,
    default = 0,
    help="Minimum number of splits per read",
)
parser.add_argument(
    "--reverse-complement",
    default = False,
    action="store_true",
    help="Whether to use the reverse complement of the reads",
)

def write_output(contigs: list[str], args: argparse.Namespace):
    def contig_to_string(contig: str, i: int, fasta: bool) -> str:
        return f">Contig {i}\n{contig}\n" if fasta else f"{contig}\n"

    output_is_fasta = args.target is None or args.target.split(".")[-1] == "fasta"

    output = "".join(contig_to_string(contig, i, output_is_fasta) for i, contig in enumerate(contigs))
    print(f"Contig number: {len(contigs)}")
    print(f"Total contig length: {sum(len(contig) for contig in contigs)}")
    if(args.target is None):
        print(output)
    else:
        file_io.write_to_file(args.target, output)
        print(f"Output written to {args.target}")

if __name__ == "__main__":
    args = parser.parse_args()

    reads = file_io.read_file_content(args.reads).strip().splitlines()
    max_read_length = max(len(read) for read in reads)

    start_time = time.time()

    graph = DeBruijnGraph.DeBruijnGraph(reads, args.splits, args.reverse_complement)
    contigs = [path for path in graph.get_maximum_non_branching_paths() if len(path) > max_read_length]

    end_time = time.time()
    elapsed_time = end_time - start_time

    write_output(contigs, args)

    print(f"Job took {elapsed_time} seconds.")

    if(args.plot):
        graph.plot()
