# cosine_similarity

import numpy
import sklearn.feature_extraction.text
import sklearn.metrics.pairwise

from . import args_common


def add_subparsers(parser):
    subparsers = parser.add_subparsers(
        dest="cosine_similarity", help="Calculate cosine similarity between strings."
    )

    parser = subparsers.add_parser(
        "cosine-similarity",
        help="cosine-similarity help",
        aliases=["cosine"],
    )

    parser.add_argument("--data-path", required=True, help="path to data.txt")
    args_common.add_common_args(parser)

    return parser


def read_items(file_path):
    with open(file_path, "r") as file:
        string_list = file.read().splitlines()
    return string_list


def main(args):
    string_list = read_items(args.data_path)

    # Convert the list of strings into a matrix of token counts
    vectorizer = sklearn.feature_extraction.text.CountVectorizer().fit_transform(
        string_list
    )

    # Calculate the cosine similarity between each pair of strings
    cosine_similarities = sklearn.metrics.pairwise.cosine_similarity(vectorizer)

    # Flatten the upper triangular part of the matrix (excluding the diagonal)
    flat_cosine_similarities = cosine_similarities[
        numpy.triu_indices(len(cosine_similarities), k=1)
    ]

    # Get the indices of the top 5 and bottom 5 values
    top_indices = numpy.argsort(flat_cosine_similarities)[-5:][::-1]
    bottom_indices = numpy.argsort(flat_cosine_similarities)[:5]

    # Output the top 5 items and scores
    print("Top 5 items and scores:")
    for index in top_indices:
        item1, item2 = numpy.unravel_index(index, cosine_similarities.shape)
        score = flat_cosine_similarities[index]
        print(
            f"Items: '{string_list[item1]}' and '{string_list[item2]}', Score = {score}"
        )

    # Output the bottom 5 items and scores
    print("\nBottom 5 items and scores:")
    for index in bottom_indices:
        item1, item2 = numpy.unravel_index(index, cosine_similarities.shape)
        score = flat_cosine_similarities[index]
        print(
            f"Items: '{string_list[item1]}' and '{string_list[item2]}', Score = {score}"
        )
