import DeBruijnGraph
import file_io
import argparse
from typing import Tuple

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

def calculate_n50(contig_lengths: list[int]) -> int:
    total_length = sum(contig_lengths)
    half_length = total_length / 2

    contig_lengths.sort(reverse=True)

    current_sum = 0
    for length in contig_lengths:
        current_sum += length
        if current_sum >= half_length:
            return length

    return 0

def optimize_kmer_size(input_reads: list[str]) -> Tuple[int, list[str]]:
    best_k = 0
    # best_assembly = []
    best_n50 = 0

    for k in range(29, 31):  # You can adjust the range based on your dataset and requirements
        assembler = DeBruijnGraph.DeBruijnGraph(input_reads, splits_per_read=int(len(input_reads[0])/k), use_reverse_complement=False)
        assembled_contigs = assembler.get_maximum_non_branching_paths()
        contig_lengths = [len(contig) for contig in assembled_contigs]
        current_n50 = calculate_n50(contig_lengths)

        if current_n50 > best_n50:
            best_n50 = current_n50
            best_k = k
            # best_assembly = assembled_contigs

    # return best_k, best_assembly
    return best_k


def main():

    args = parser.parse_args()

    reads = file_io.read_file_content(args.reads).strip().splitlines()

    # Optimize k-mer size
    best_k, best_assembly = optimize_kmer_size(reads)

    # Display results
    print(f"Best k-mer size: {best_k}")

    # Initialize assembler with the best k-mer size
    # assembler = DeBruijnGraph.DeBruijnGraph(reads, splits_per_read=best_k, use_reverse_complement=False)


if __name__ == "__main__":
    main()