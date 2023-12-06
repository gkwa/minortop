# Smith-Waterman algorithm

import argparse
import itertools
import typing

import Bio.Align


def read_data(filename: str) -> typing.List[str]:
    """Read data from the file."""
    with open(filename, "r") as file:
        return file.read().splitlines()


def calculate_similarity(seq1: str, seq2: str) -> int:
    """Calculate similarity using the Smith-Waterman algorithm."""
    aligner = Bio.Align.PairwiseAligner()
    alignments = aligner.align(seq1, seq2)
    return alignments[0].score


def filter_by_similarity(data: typing.List[str], threshold: int) -> typing.List[tuple]:
    """Filter pairs with similarity greater than
    the threshold and order by similarity."""
    pairs = list(itertools.combinations(data, 2))
    result = [
        (pair[0], pair[1], calculate_similarity(pair[0], pair[1])) for pair in pairs
    ]
    result = [(seq1, seq2, score) for seq1, seq2, score in result if score > threshold]
    return pairs, sorted(
        result, key=lambda x: x[2], reverse=True
    )  # Sort by similarity in descending order


def main():
    # Set up argparse
    parser = argparse.ArgumentParser(
        description="Calculate and filter string pairs based on similarity."
    )
    parser.add_argument(
        "--input_filename",
        default="data.txt",
        help="Input file containing newline-delimited strings",
    )
    parser.add_argument(
        "--similarity-threshold",
        type=int,
        default=10,
        help="Threshold for similarity score",
    )
    args = parser.parse_args()

    # Read data from file
    data = read_data(args.input_filename)

    # Filter pairs by similarity and order by similarity
    comparisons, result = filter_by_similarity(data, args.similarity_threshold)

    # Print results
    for seq1, seq2, score in result:
        print(f"score: {score}")
        print(seq1)
        print(seq2)
        print()

    # Report statistics
    print(f"Total number of strings: {len(data):,}")
    print(f"Total number of comparisons: {len(comparisons):,}")

    if result:
        min_score = min(result, key=lambda x: x[2])[2]
        max_score = max(result, key=lambda x: x[2])[2]
        print(f"Minimum score: {min_score:,}")
        print(f"Maximum score: {max_score:,}")

    count_above_threshold = len(result)
    print(
        f"Number of pairs above similarity threshold"
        f" {args.similarity_threshold}: {count_above_threshold:,}"
    )


if __name__ == "__main__":
    main()
