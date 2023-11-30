from mip import Model, MAXIMIZE, xsum, OptimizationStatus
from utils import count_items_in_combinations, generate_valid_combinations

lengths = {'A': 110, 'B': 92, 'C': 80, 'D': 74, 'E': 70, 'F': 65}
prix_vente = {'A': 100, 'B': 80, 'C': 70, 'D': 65, 'E': 60, 'F': 57}
cout_par_metre = 120

# Combinaisons possibles
combinaisons = generate_valid_combinations(lengths, 180, 245)

values_combinaisons = [sum(prix_vente[i] for i in comb) - cout_par_metre for comb in combinaisons]
inconnus_combinaisons = ["x" + ''.join(comb) for comb in combinaisons]

print(inconnus_combinaisons)

m = Model("Rouleau", sense=MAXIMIZE)

vars = [m.add_var(name=v) for v in inconnus_combinaisons]
m.objective = xsum(values_combinaisons[i] * vars[i] for i in range(35))

# Ajout des contraintes
m += xsum(value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, 'A').items()) <= 400
m += xsum(value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, 'B').items()) <= 400
m += xsum(value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, 'C').items()) <= 400
m += xsum(value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, 'D').items()) <= 400
m += xsum(value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, 'E').items()) <= 400
m += xsum(value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, 'F').items()) <= 400

m += xsum(value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, 'A').items()) <= 0.5 * xsum(
    (len(inconnus_combinaisons[indice])-1) * vars[indice] for indice, x in enumerate(inconnus_combinaisons))
m += xsum(value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, 'B').items()) <= 0.5 * xsum(
    (len(inconnus_combinaisons[indice])-1) * vars[indice] for indice, x in enumerate(inconnus_combinaisons))
m += xsum(value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, 'C').items()) <= 0.5 * xsum(
    (len(inconnus_combinaisons[indice])-1) * vars[indice] for indice, x in enumerate(inconnus_combinaisons))
m += xsum(value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, 'D').items()) <= 0.5 * xsum(
    (len(inconnus_combinaisons[indice])-1) * vars[indice] for indice, x in enumerate(inconnus_combinaisons))
m += xsum(value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, 'E').items()) <= 0.5 * xsum(
    (len(inconnus_combinaisons[indice])-1) * vars[indice] for indice, x in enumerate(inconnus_combinaisons))
m += xsum(value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, 'F').items()) <= 0.5 * xsum(
    (len(inconnus_combinaisons[indice])-1) * vars[indice] for indice, x in enumerate(inconnus_combinaisons))

m += xsum(value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, 'C').items()) <= xsum(
    value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, 'A').items()) - 100

m.optimize()

# Affichage du résultat
if m.status == OptimizationStatus.OPTIMAL:
    for i, var in enumerate(vars):
        print(f"{inconnus_combinaisons[i]} = {var.x}")
    print(f"Coût total : {m.objective_value}")
else:
    print("Pas de solution possible")
