# cosine_similarity

import argparse

import sklearn.feature_extraction.text
import sklearn.metrics.pairwise


def read_strings_from_file(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file]


def main(similarity_threshold, file_path):
    # Example list of strings
    string_list = read_strings_from_file(file_path)

    # Convert the list of strings to a matrix of token counts
    vectorizer = sklearn.feature_extraction.text.CountVectorizer().fit_transform(
        string_list
    )

    # Calculate the cosine similarity between pairs of strings
    cosine_similarities = sklearn.metrics.pairwise.cosine_similarity(
        vectorizer, vectorizer
    )

    # Get indices of pairs that meet the similarity threshold
    selected_indices = [
        (i, j)
        for i in range(len(string_list) - 1)
        for j in range(i + 1, len(string_list))
        if cosine_similarities[i, j] > similarity_threshold
    ]

    # Sort the pairs by ascending similarity score
    selected_indices.sort(key=lambda pair: cosine_similarities[pair[0], pair[1]])

    # Print the pairs with similarity scores above the threshold
    print(
        f"Pairs with similarity scores above {similarity_threshold}"
        "(ordered by ascending score):"
    )
    for i, j in selected_indices:
        similarity = cosine_similarities[i, j]
        print(f"Score: {similarity:.3f}")
        print(f"{string_list[i]}")
        print(f"{string_list[j]}")
        print()

    # Report the total count of pairs and the count of selected pairs
    total_count = len(
        list(
            (i, j)
            for i in range(len(string_list) - 1)
            for j in range(i + 1, len(string_list))
        )
    )
    count_of_selected_pairs = len(selected_indices)
    print(f"\nTotal number of pairs: {total_count:,}")
    print(
        "Number of pairs with similarity scores above "
        f"{similarity_threshold}: {count_of_selected_pairs:,}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate cosine similarity between pairs of strings."
    )
    parser.add_argument(
        "--similarity-threshold",
        type=float,
        default=0.4,
        help="Threshold for cosine similarity (default: 0.4)",
    )
    parser.add_argument(
        "--file-path",
        type=str,
        default="data.txt",
        help="Path to the newline-delimited file"
        " containing strings (default: data.txt)",
    )

    args = parser.parse_args()
    main(args.similarity_threshold, args.file_path)
