import argparse
import random

import file_io

parser = argparse.ArgumentParser(
    description="Generate reads from a given sequence",
    prog="read_generator"
)
parser.add_argument(
    "-s",
    "-g",
    "--sequence",
    "--genome",
    required=True,
    help="Input file",
)
parser.add_argument(
    "-t",
    "--target",
    help="Output file",
)
parser.add_argument(
    "-r",
    "--read-size",
    type=int,
    default=100,
    help="Read size",
)
parser.add_argument(
    "-e",
    "--error-probability",
    type=float,
    default=0.0,
    help="Error probability",
)
parser.add_argument(
    "-c",
    "--reverse-complement",
    action="store_true",
    help="Introduce reverse complements",
)

def get_reverse_complement(read: str) -> str:
    complement = {"a": "t", "t": "a", "c": "g", "g": "c", "A": "T", "T": "A", "C": "G", "G": "C"}
    return "".join(complement[base] for base in read[::-1])

def generate_read(read: str, error_probability: float, reverse_complement: bool) -> str:
    read_size = len(read)
    for j in range(read_size):
        if random.random() < error_probability / read_size:
            read = read[:j] + random.choice("acgt") + read[j+1:]
    return read if not reverse_complement or random.random() < 0.5 else get_reverse_complement(read)

def generate_reads(sequence: str, read_size: int, error_probability: float, reverse_complement: bool) -> list[str]:
    sequence_length = len(sequence)
    num_reads = int(sequence_length - read_size + 1)
    reads = [generate_read(sequence[i:i+read_size], error_probability, reverse_complement) for i in range(num_reads)]
    return reads

if __name__ == "__main__":
    args = parser.parse_args()
    reference_genome = file_io.read_file_content(args.sequence).replace("\n", "").strip()

    generated_reads = generate_reads(reference_genome, args.read_size, args.error_probability, args.reverse_complement)

    file_io.write_to_file(args.target, "\n".join(generated_reads))
    print(f"Output written to {args.target}")
