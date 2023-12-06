# Needleman-Wunsch Algorithm

import argparse

import numpy


def read_strings_from_file(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file]


def needleman_wunsch(str1, str2, match_score=2, mismatch_score=-1, gap_penalty=-1):
    len_str1 = len(str1) + 1
    len_str2 = len(str2) + 1

    # Initialize the scoring matrix
    score_matrix = numpy.zeros((len_str1, len_str2), dtype=int)

    for i in range(1, len_str1):
        for j in range(1, len_str2):
            match = score_matrix[i - 1, j - 1] + (
                match_score if str1[i - 1] == str2[j - 1] else mismatch_score
            )
            delete = score_matrix[i - 1, j] + gap_penalty
            insert = score_matrix[i, j - 1] + gap_penalty
            score_matrix[i, j] = max(match, delete, insert)

    return score_matrix[len_str1 - 1, len_str2 - 1]


def calculate_similarity(str1, str2):
    len_max = max(len(str1), len(str2))
    if len_max == 0:
        return 0.0
    return needleman_wunsch(str1.lower(), str2.lower()) / len_max


def main():
    parser = argparse.ArgumentParser(
        description="String similarity using Needleman-Wunsch algorithm."
    )
    parser.add_argument(
        "--file-path",
        default="data.txt",
        help="Path to the file containing newline-delimited strings.",
    )
    parser.add_argument(
        "--similarity-threshold",
        type=float,
        default=1.5,
        help="Threshold for similarity score.",
    )
    parser.add_argument(
        "--top-n", type=int, default=None, help="Filter and display the top N scores."
    )

    args = parser.parse_args()

    strings = read_strings_from_file(args.file_path)

    total_strings = len(strings)
    results = []

    for i in range(total_strings):
        for j in range(i + 1, total_strings):
            str1 = strings[i]
            str2 = strings[j]
            similarity = calculate_similarity(str1, str2)

            if similarity > args.similarity_threshold:
                results.append((similarity, str1, str2))

    # Sort results by increasing similarity
    results.sort(key=lambda x: x[0])

    # Filter and display the top N scores if specified
    if args.top_n is not None:
        results = results[: args.top_n]

    if results:
        # Print the sorted results
        for result in results:
            print(f"\nscore: {result[0]:0.3f}")
            print(result[1])
            print(result[2])

        # Print additional information
        print()
        print(f"Min similarity score: {results[0][0]:0.3f}")
        print(f"Max similarity score: {results[-1][0]:0.3f}")
        print(f"Total strings: {total_strings:,}")
        print(
            f"Strings with similarity greater than"
            f" {args.similarity_threshold}: {len(results):,}"
        )


if __name__ == "__main__":
    main()
