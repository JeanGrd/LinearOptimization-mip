"""
Nom: PALEA
Prénom: Ana
Numéro étudiant: 22012765

Optimisation linéaire pour maximiser le bénéfice de la découpe de papier
"""

from mip import Model, MAXIMIZE, xsum, OptimizationStatus
from utils import generate_valid_combinations, count_items_in_combinations

# Définition des longueurs et des prix de vente pour chaque type de bande
longueurs_bandes = {'A': 110, 'B': 92, 'C': 80, 'D': 74, 'E': 70, 'F': 65}
prix_vente_bandes = {'A': 100, 'B': 80, 'C': 70, 'D': 65, 'E': 60, 'F': 57}
cout_par_metre = 120

# Génération des combinaisons valides de découpe
combinaisons = generate_valid_combinations(longueurs_bandes, 180, 245)

# Calcul du bénéfice pour chaque combinaison
benefices_combinaisons = [sum(prix_vente_bandes[i] for i in comb) - cout_par_metre for comb in combinaisons]
variables_combinaisons = ["x" + ''.join(comb) for comb in combinaisons]

# Création du modèle d'optimisation
modele = Model("Rouleau", sense=MAXIMIZE)

# Ajout des variables correspondant aux combinaisons
variables = [modele.add_var(name=v) for v in variables_combinaisons]

# Définition de la fonction objectif
modele.objective = xsum(benefices_combinaisons[i] * variables[i] for i in range(len(benefices_combinaisons)))

# Contrainte : ne pas produire plus de 400m de chaque bande
modele += xsum(value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'A').items()) <= 400
modele += xsum(value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'B').items()) <= 400
modele += xsum(value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'C').items()) <= 400
modele += xsum(value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'D').items()) <= 400
modele += xsum(value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'E').items()) <= 400
modele += xsum(value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'F').items()) <= 400

# Contrainte : Aucune bande ne peut représenter plus de 50% de la longueur de bande totale
modele += xsum(value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'A').items()) - 0.5 * xsum(
    (len(variables_combinaisons[indice])-1) * variables[indice] for indice, x in enumerate(variables_combinaisons)) <= 0
modele += xsum(value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'B').items()) - 0.5 * xsum(
    (len(variables_combinaisons[indice])-1) * variables[indice] for indice, x in enumerate(variables_combinaisons)) <= 0
modele += xsum(value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'C').items()) - 0.5 * xsum(
    (len(variables_combinaisons[indice])-1) * variables[indice] for indice, x in enumerate(variables_combinaisons)) <= 0
modele += xsum(value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'D').items()) - 0.5 * xsum(
    (len(variables_combinaisons[indice])-1) * variables[indice] for indice, x in enumerate(variables_combinaisons)) <= 0
modele += xsum(value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'E').items()) - 0.5 * xsum(
    (len(variables_combinaisons[indice])-1) * variables[indice] for indice, x in enumerate(variables_combinaisons)) <= 0
modele += xsum(value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'F').items()) - 0.5 * xsum(
    (len(variables_combinaisons[indice])-1) * variables[indice] for indice, x in enumerate(variables_combinaisons)) <= 0

# Contrainte : Il faut au moins produire plus de bande A que de bande C
modele += xsum(value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'C').items()) - xsum(
    value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'A').items()) <= -100

# Optimisation du modèle
modele.optimize()

# Affichage des résultats
if modele.status == OptimizationStatus.OPTIMAL:
    for i, var in enumerate(variables):
        print(f"{variables_combinaisons[i]} = {var.x}")
    print(f"Bénéfice total : {modele.objective_value}")
else:
    print("Pas de solution possible")
