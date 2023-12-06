# levenshtein, jaccard and cosine

import argparse
import logging
import math
import os

import Levenshtein


class SimilarityCalculator:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def calculate_similarity(self, string1, string2):
        return self.algorithm.calculate_similarity(string1, string2)


class LevenshteinAlgorithm:
    @staticmethod
    def calculate_similarity(string1, string2):
        return Levenshtein.distance(string1.lower(), string2.lower())


class JaccardAlgorithm:
    @staticmethod
    def calculate_similarity(string1, string2):
        set1 = set(string1.lower())
        set2 = set(string2.lower())
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return 1.0 - intersection / union if union != 0 else 0.0


class CosineSimilarityAlgorithm:
    @staticmethod
    def calculate_similarity(string1, string2):
        vector1 = {char: string1.lower().count(char) for char in set(string1.lower())}
        vector2 = {char: string2.lower().count(char) for char in set(string2.lower())}

        dot_product = sum(
            vector1[char] * vector2[char] for char in vector1 if char in vector2
        )
        magnitude1 = math.sqrt(sum(value**2 for value in vector1.values()))
        magnitude2 = math.sqrt(sum(value**2 for value in vector2.values()))

        return (
            dot_product / (magnitude1 * magnitude2)
            if magnitude1 * magnitude2 != 0
            else 0.0
        )


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read().splitlines()


def find_pairs_below_score(strings, score_threshold, similarity_calculator):
    pairs = []
    for i in range(len(strings)):
        for j in range(i + 1, len(strings)):
            similarity = similarity_calculator.calculate_similarity(
                strings[i], strings[j]
            )
            if similarity <= score_threshold:
                pairs.append(((i, j), similarity))
    pairs.sort(key=lambda x: x[1])
    return pairs


def quote_if_whitespace(word):
    if word[0].isspace() or word[-1].isspace():
        return f'"{word}"'
    return word


def main():
    parser = argparse.ArgumentParser(
        description="String similarity scoring using different algorithms."
    )
    parser.add_argument(
        "--file-path",
        default="data.txt",
        help="Path to the file containing newline-delimited strings.",
    )
    parser.add_argument(
        "--score", type=float, default=1, help="Score threshold to filter pairs."
    )
    parser.add_argument(
        "--algorithm",
        choices=["levenshtein", "jaccard", "cosine"],
        default="levenshtein",
        help="Similarity calculation algorithm.",
    )
    args = parser.parse_args()

    # Set up similarity calculator based on the chosen algorithm
    if args.algorithm == "levenshtein":
        similarity_calculator = SimilarityCalculator(LevenshteinAlgorithm())
    elif args.algorithm == "jaccard":
        similarity_calculator = SimilarityCalculator(JaccardAlgorithm())
    elif args.algorithm == "cosine":
        similarity_calculator = SimilarityCalculator(CosineSimilarityAlgorithm())
    else:
        raise ValueError("Invalid algorithm choice.")

    # Read strings from the file
    strings = read_file(args.file_path)

    # Count of the total number of items in data.txt
    total_items = len(strings)

    # Find and print the pairs below the score threshold
    pairs_below_score = find_pairs_below_score(
        strings, args.score, similarity_calculator
    )
    count_below_score = len(pairs_below_score)

    for (i, j), similarity in pairs_below_score:
        quoted_str1 = quote_if_whitespace(strings[i])
        quoted_str2 = quote_if_whitespace(strings[j])
        print(f"score: {similarity:,.2f}\n{quoted_str1}\n{quoted_str2}\n")

    print(
        "Number of items found within score "
        f"threshold {args.score:,.2f}: {count_below_score:,d}\n"
        f"Total number of items in {args.file_path}: {total_items:,d}\n"
    )


if __name__ == "__main__":
    # Set up logging if logging is enabled
    log_filename = "similarity_log.txt"
    logging_enabled = True  # Change to False if logging is not desired

    if logging_enabled:
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s: %(message)s",
        )

    try:
        main()
    except Exception as e:
        if logging_enabled:
            logging.exception(f"An error occurred: {str(e)}")
        else:
            print(f"An error occurred: {str(e)}")

    log_size_limit = 10 * 1024 * 1024  # 10MB
    if logging_enabled and os.path.getsize(log_filename) > log_size_limit:
        os.remove(log_filename)
        logging.warning(
            "Log file exceeded size limit and was truncated."
            f" Original log file: {log_filename}"
        )
