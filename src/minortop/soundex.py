# soundex

import argparse

import jellyfish


def read_strings_from_file(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file]


def calculate_similarity(string1, string2):
    return jellyfish.soundex(string1.lower()) == jellyfish.soundex(string2.lower())


def main():
    parser = argparse.ArgumentParser(
        description="String similarity using Soundex algorithm"
    )
    parser.add_argument(
        "--file_path",
        default="data.txt",
        help="Path to the file containing newline-delimited strings",
    )
    parser.add_argument(
        "--similarity_threshold",
        type=float,
        default=10,
        help="Threshold for similarity comparison (default: 10)",
    )

    args = parser.parse_args()

    strings = read_strings_from_file(args.file_path)
    total_strings = len(strings)

    results = []

    for i in range(total_strings - 1):
        for j in range(i + 1, total_strings):
            similarity_score = calculate_similarity(strings[i], strings[j])
            if similarity_score >= args.similarity_threshold:
                results.append((similarity_score, strings[i], strings[j]))

    results.sort()

    if results:
        min_score = results[0][0]
        max_score = results[-1][0]

        for score, string1, string2 in results:
            print(string1)
            print(string2)
            print()

        print(f"Total strings: {total_strings:,}")
        print(f"Total comparisons made: {total_strings * (total_strings - 1) // 2:,}")
        print(
            "Strings with similarity score greater than"
            f"{args.similarity_threshold}: {len(results):,}"
        )
        print(f"Min similarity score: {min_score}")
        print(f"Max similarity score: {max_score}")


if __name__ == "__main__":
    main()
