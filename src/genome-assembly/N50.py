import DeBruijnGraph
import file_io
import argparse

parser = argparse.ArgumentParser(
    description="Evaluate the best k-mer size for a given set of reads",
    prog="N50.py"
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

def optimize_kmer_size(input_reads: list[str], k_search_space: list[int]) -> int:
    best_k = -1
    best_n50 = 0

    for k in k_search_space:
        assembler = DeBruijnGraph.DeBruijnGraph(input_reads, splits_per_read=k, use_reverse_complement=True)
        assembled_contigs = assembler.get_maximum_non_branching_paths()
        contig_lengths = [len(contig) for contig in assembled_contigs]
        current_n50 = calculate_n50(contig_lengths)

        if current_n50 > best_n50:
            best_n50 = current_n50
            best_k = k

    return best_k


def main():
    search_space = [0, 1, 2, 3]
    args = parser.parse_args()

    reads = file_io.read_file_content(args.reads).strip().splitlines()

    best_k = optimize_kmer_size(reads, search_space)

    print(f"Best k-mer size: {best_k}")

if __name__ == "__main__":
    main()
