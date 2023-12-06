# cosine_similarity

import argparse

import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def read_items(file_path):
    with open(file_path, "r") as file:
        string_list = file.read().splitlines()
    return string_list


parser = argparse.ArgumentParser(
    description="Calculate cosine similarity between strings."
)
parser.add_argument("--file-path", required=True, help="Path to the input file")

args = parser.parse_args()

string_list = read_items(args.file_path)

# Convert the list of strings into a matrix of token counts
vectorizer = CountVectorizer().fit_transform(string_list)

# Calculate the cosine similarity between each pair of strings
cosine_similarities = cosine_similarity(vectorizer)

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
    print(f"Items: '{string_list[item1]}' and '{string_list[item2]}', Score = {score}")

# Output the bottom 5 items and scores
print("\nBottom 5 items and scores:")
for index in bottom_indices:
    item1, item2 = numpy.unravel_index(index, cosine_similarities.shape)
    score = flat_cosine_similarities[index]
    print(f"Items: '{string_list[item1]}' and '{string_list[item2]}', Score = {score}")
