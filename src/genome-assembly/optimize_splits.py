import main
import argparse
from main import parser, main, write_output

def calculate_nk(contig_lengths: list[int], k: int) -> int:
    total_length = sum(contig_lengths)
    k_length = total_length * k / 100

    contig_lengths.sort(reverse=True)

    current_sum = 0
    for length in contig_lengths:
        current_sum += length
        if current_sum >= k_length:
            return length

    return 0

def optimize_splits(args: argparse.Namespace, search_space: list[int]) -> tuple[int, str]:
    splits = -1
    best_nk = 0
    contigs = []

    for k in search_space:
        args.splits = k
        assembled_contigs = main(args, False)
        contig_lengths = [len(contig) for contig in assembled_contigs]
        current_nk = calculate_nk(contig_lengths, 50)

        if current_nk > best_nk:
            best_nk = current_nk
            splits = k
            contigs = assembled_contigs

    return splits, contigs

if __name__ == "__main__":
    parser.add_argument(
        "-k",
        type=int,
        default=75,
        help="k for Nk metric, default is 75",
    )
    parser.add_argument(
        "--search-space",
        type=int,
        nargs="+",
        default=[0, 1, 2, 3],
        help="Search space for splits, default is [0, 1, 2, 3]",
    )
    args = parser.parse_args()

    best_splits, best_contigs = optimize_splits(args, args.search_space)

    print(f"Best splits value: {best_splits}")
    write_output(best_contigs, args)
