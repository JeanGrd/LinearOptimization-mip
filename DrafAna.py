from mip import Model, MAXIMIZE, xsum, OptimizationStatus
from itertools import combinations_with_replacement


def valid_combinations(lengths, min_length, max_length):
    min_item_length = min(lengths.values())
    max_elements = max_length // min_item_length

    valid_combs = []
    for r in range(1, max_elements + 1):
        for comb in combinations_with_replacement(lengths.keys(), r):
            total_length = sum(lengths[item] for item in comb)
            if min_length < total_length <= max_length:
                valid_combs.append(comb)

    return valid_combs


def combinaison_contains(combinaisons: list, value: str) -> dict:
    result = {}
    for index, comb in enumerate(combinaisons):
        if value in comb:
            result[index] = comb.count(value)
    return result


lengths = {'A': 110, 'B': 92, 'C': 80, 'D': 74, 'E': 70, 'F': 65}
prix_vente = {'A': 100, 'B': 80, 'C': 70, 'D': 65, 'E': 60, 'F': 57}
cout_par_metre = 120

# Combinaisons possibles
combinaisons = valid_combinations(lengths, 180, 245)

values_combinaisons = [sum(prix_vente[i] for i in comb) - cout_par_metre for comb in combinaisons]
inconnus_combinaisons = ["x" + ''.join(comb) for comb in combinaisons]

m = Model("Rouleau", sense=MAXIMIZE)

vars = [m.add_var(name=v) for v in inconnus_combinaisons]
m.objective = xsum(values_combinaisons[i] * vars[i] for i in range(35))

# Ajout des contraintes
m += xsum(value * vars[key] for key, value in combinaison_contains(inconnus_combinaisons, 'A').items()) <= 400
m += xsum(value * vars[key] for key, value in combinaison_contains(inconnus_combinaisons, 'B').items()) <= 400
m += xsum(value * vars[key] for key, value in combinaison_contains(inconnus_combinaisons, 'C').items()) <= 400
m += xsum(value * vars[key] for key, value in combinaison_contains(inconnus_combinaisons, 'D').items()) <= 400
m += xsum(value * vars[key] for key, value in combinaison_contains(inconnus_combinaisons, 'E').items()) <= 400
m += xsum(value * vars[key] for key, value in combinaison_contains(inconnus_combinaisons, 'F').items()) <= 400

m += xsum(value * vars[key] for key, value in combinaison_contains(inconnus_combinaisons, 'A').items()) <= 0.5 * xsum(
    vars[indice] for indice, x in enumerate(inconnus_combinaisons))
m += xsum(value * vars[key] for key, value in combinaison_contains(inconnus_combinaisons, 'B').items()) <= 0.5 * xsum(
    vars[indice] for indice, x in enumerate(inconnus_combinaisons))
m += xsum(value * vars[key] for key, value in combinaison_contains(inconnus_combinaisons, 'C').items()) <= 0.5 * xsum(
    vars[indice] for indice, x in enumerate(inconnus_combinaisons))
m += xsum(value * vars[key] for key, value in combinaison_contains(inconnus_combinaisons, 'D').items()) <= 0.5 * xsum(
    vars[indice] for indice, x in enumerate(inconnus_combinaisons))
m += xsum(value * vars[key] for key, value in combinaison_contains(inconnus_combinaisons, 'E').items()) <= 0.5 * xsum(
    vars[indice] for indice, x in enumerate(inconnus_combinaisons))
m += xsum(value * vars[key] for key, value in combinaison_contains(inconnus_combinaisons, 'F').items()) <= 0.5 * xsum(
    vars[indice] for indice, x in enumerate(inconnus_combinaisons))

m += xsum(value * vars[key] for key, value in combinaison_contains(inconnus_combinaisons, 'C').items()) <= 100 + xsum(
    value * vars[key] for key, value in combinaison_contains(inconnus_combinaisons, 'A').items())

m.optimize()

# Affichage du résultat
if m.status == OptimizationStatus.OPTIMAL:
    for i, var in enumerate(vars):
        print(f"{inconnus_combinaisons[i]} = {var.x}")
    print(f"Coût total : {m.objective_value}")
else:
    print("Pas de solution possible")
