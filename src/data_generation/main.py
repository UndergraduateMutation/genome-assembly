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

def insert_error(read: str, error_probability: float) -> str:
    read_size = len(read)
    for j in range(read_size):
        if random.random() < error_probability / read_size:
            read = read[:j] + random.choice("acgt") + read[j+1:]
    return read

def generate_reads(sequence: str, read_size: int, error_probability: float) -> list[str]:
    reads = []
    sequence_length = len(sequence)
    num_reads = int(sequence_length - read_size + 1)

    for i in range(num_reads):
        reads.append(insert_error(sequence[i:i+read_size], error_probability))

    return reads

if __name__ == "__main__":
    args = parser.parse_args()
    reference_genome = file_io.read_file_content(args.sequence).replace("\n", "").strip()

    generated_reads = generate_reads(reference_genome, args.read_size, args.error_probability)

    file_io.write_to_file(args.target, "\n".join(generated_reads))
    print(f"Output written to {args.target}")
