from itertools import combinations_with_replacement


def generate_valid_combinations(item_lengths, min_len, max_len):
    """
    Génère toutes les combinaisons valides d'items dans une plage de longueurs spécifiée.

    :param longueurs_items: Un dictionnaire où les clés sont les étiquettes des items et les valeurs sont leurs longueurs.
    :type longueurs_items: dict
    :param longueur_min: La longueur totale minimale d'une combinaison.
    :type longueur_min: int
    :param longueur_max: La longueur totale maximale d'une combinaison.
    :type longueur_max: int
    :return: Une liste de tuples représentant les combinaisons valides.
    :rtype: list of tuples
    """
    min_length = min(item_lengths.values())
    max_elements = max_len // min_length

    return [comb for r in range(1, max_elements + 1)
            for comb in combinations_with_replacement(item_lengths.keys(), r)
            if min_len < sum(item_lengths[item] for item in comb) <= max_len]


def count_items_in_combinations(combinations, item):
    """
    Compte les occurrences d'un item spécifique dans chaque combinaison.

    :param combinaisons: Une liste de combinaisons (tuples).
    :type combinaisons: list
    :param item: L'item à compter dans les combinaisons.
    :type item: str
    :return: Un dictionnaire où les clés sont les indices des combinaisons et les valeurs sont le nombre de fois que l'item apparaît.
    :rtype: dict
    """
    return {index: comb.count(item) for index, comb in enumerate(combinations) if item in comb}
