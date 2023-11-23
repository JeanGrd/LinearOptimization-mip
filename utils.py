from itertools import combinations_with_replacement


def generate_valid_combinations(item_lengths, min_len, max_len):
    """
    Generates all valid combinations of items within a specified length range.

    Args:
    item_lengths (dict): A dictionary where keys are item labels and values are their lengths.
    min_len (int): The minimum total length of a combination.
    max_len (int): The maximum total length of a combination.

    Returns:
    list: A list of tuples
    """
    min_length = min(item_lengths.values())
    max_elements = max_len // min_length

    return [comb for r in range(1, max_elements + 1)
            for comb in combinations_with_replacement(item_lengths.keys(), r)
            if min_len < sum(item_lengths[item] for item in comb) <= max_len]


def count_items_in_combinations(combinations, item):
    """
    Counts the occurrences of a specific item in each combination.

    Args:
    combinations (list): A list of combinations (tuples).
    item (str): The item to count within the combinations.

    Returns:
    dict: A dictionary where keys are indices of combinations and values are the count of the item.
    """
    return {index: comb.count(item) for index, comb in enumerate(combinations) if item in comb}

