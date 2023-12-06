# jarowinkler.jarowinkler_similarity

import argparse

import jarowinkler


def compare_strings(strings_to_compare, similarity_threshold):
    # Create a list of tuples containing the original
    # strings and their Jaro-Winkler distances
    similarities = []
    total_comparisons = 0  # Initialize the total comparisons count

    for i in range(len(strings_to_compare) - 1):
        for j in range(i + 1, len(strings_to_compare)):
            total_comparisons += 1  # Increment the total comparisons count
            string1 = strings_to_compare[i]
            string2 = strings_to_compare[j]

            # Calculate the Jaro and Jaro-Winkler Similarities (case-insensitive)
            jaro_sim = jarowinkler.jaro_similarity(string1.lower(), string2.lower())
            jarowinkler_sim = jarowinkler.jarowinkler_similarity(
                string1.lower(), string2.lower()
            )

            # Append the tuple to the list if similarity is above the threshold
            if jarowinkler_sim >= similarity_threshold:
                similarities.append((string1, string2, jaro_sim, jarowinkler_sim))

    # Sort the list of tuples based on Jaro-Winkler similarities in ascending order
    similarities.sort(key=lambda x: x[3])

    # Print the sorted list in the specified format
    for similarity in similarities:
        print(f"score1: {similarity[2]:.3f}, score2: {similarity[3]:.3f}")
        print(f"{similarity[0]}\n{similarity[1]}\n")

    # Report counts
    total_strings_count = len(strings_to_compare)
    above_threshold_count = sum(
        1 for sim in similarities if sim[3] >= similarity_threshold
    )

    print(f"Total Comparisons Made: {total_comparisons:,}")
    print(f"Total Strings Count: {total_strings_count:,}")
    print(f"Above Threshold Count: {above_threshold_count:,}")


if __name__ == "__main__":
    # Set up argparse for command line arguments
    parser = argparse.ArgumentParser(
        description="Compare strings using Jaro-Winkler similarity."
    )
    parser.add_argument(
        "--similarity-threshold", type=float, default=0.8, help="Similarity threshold"
    )
    args = parser.parse_args()

    # Read data from the file
    with open("data.txt", "r") as file:
        strings_to_compare = [line.strip() for line in file]

    # Call the comparison function
    compare_strings(strings_to_compare, args.similarity_threshold)
