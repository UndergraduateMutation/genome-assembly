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
parser.add_argument(
    "--splits",
    "-s",
    type=int,
    default = 0,
    help="Minimum number of splits per read",
)
parser.add_argument(
    "--reverse-complement",
    "-c",
    default = False,
    action="store_true",
    help="Whether to use the reverse complement of the reads",
)

def write_output(contigs: list[str], args: argparse.Namespace):
    def contig_to_string(contig: str, i: int, fasta: bool) -> str:
        return f">Contig_{i}\n{contig}\n" if fasta else f"{contig}\n"

    output_is_fasta = args.target is None or args.target.split(".")[-1] == "fasta"

    output = "".join(contig_to_string(contig, i, output_is_fasta) for i, contig in enumerate(contigs))
    print(f"Contig number: {len(contigs)}")
    print(f"Total contig length: {sum(len(contig) for contig in contigs)}")
    if(args.target is None):
        print(output)
    else:
        file_io.write_to_file(args.target, output)
        print(f"Output written to {args.target}")

def reorder_contig(contig: str) -> str:
    reverse_complement = DeBruijnGraph.reverse_complement(contig)
    return reverse_complement if reverse_complement < contig else contig

def filter_paths(max_nb_paths: list[str], reads: list[str]) -> list[str]:
    max_read_length = max(len(read) for read in reads)
    return list({reorder_contig(path) for path in max_nb_paths if len(path) > max_read_length})

def main(args: argparse.Namespace):
    reads = file_io.read_file_content(args.reads).strip().splitlines()

    graph = DeBruijnGraph.DeBruijnGraph(reads, args.splits, args.reverse_complement)

    max_nbpaths = graph.get_maximum_non_branching_paths()

    contigs = filter_paths(max_nbpaths, reads)

    write_output(contigs, args)

    if args.plot:
        graph.plot()

if __name__ == "__main__":
    arguments = parser.parse_args()
    main(arguments)
    