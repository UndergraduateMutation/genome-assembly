import matplotlib.pyplot as plt
import argparse
from Bio import SeqIO

def read_contigs(file_path: str):
    return list(SeqIO.parse(file_path, "fasta"))

parser = argparse.ArgumentParser(
    description="Visualize genome assembly contigs",
    prog="visualize_contigs"
)
parser.add_argument(
    "--file",
    required=True,
    help="Contigs file",
)

def plot_contig_lengths(contigs: list[SeqIO.SeqRecord]):
    lengths = [len(contig) for contig in contigs]
    plt.hist(lengths)
    plt.title('Contig Length Distribution')
    plt.xlabel('Contig Length')
    plt.ylabel('Frequency')
    plt.show()

if __name__ == "__main__":
    args = parser.parse_args()
    contigs = read_contigs(args.file)
    plot_contig_lengths(contigs)
