"""
Nom: GUIRAUD
Prénom: Jean
Numéro étudiant: 21804397

Optimisation linéaire pour maximiser le bénéfice de la découpe de papier
"""

from mip import Model, MAXIMIZE, xsum, OptimizationStatus
from utils import generate_valid_combinations, count_items_in_combinations

# Définition des longueurs et des prix de vente pour chaque type de bande
longueurs_bandes = {'A': 110, 'B': 92, 'C': 80, 'D': 74, 'E': 70, 'F': 65}
prix_vente_bandes = {'A': 100, 'B': 80, 'C': 70, 'D': 65, 'E': 60, 'F': 57}
cout_par_metre = 120

# Génération des combinaisons valides de découpe
combinaisons = generate_valid_combinations(longueurs_bandes, 190, 255)
print(len(combinaisons))

# Calcul du bénéfice pour chaque combinaison
benefices_combinaisons = [sum(prix_vente_bandes[i] for i in comb) - cout_par_metre for comb in combinaisons]
variables_combinaisons = ["x" + ''.join(comb) for comb in combinaisons]

# Création du modèle d'optimisation
modele = Model("Rouleau", sense=MAXIMIZE)

# Ajout des variables correspondant aux combinaisons
variables = [modele.add_var(name=v) for v in variables_combinaisons]

# Définition de la fonction objectif
modele.objective = xsum(benefices_combinaisons[i] * variables[i] for i in range(40))
print(modele.objective)

# Contrainte : Longueur totale de papier maximale disponible = 1000m
modele += xsum(variables[indice] for indice, x in enumerate(variables_combinaisons)) <= 1000

# Contrainte : Il faut produire assez de chaque bande pour honorer les commandes
modele += xsum(-value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'A').items()) <= -200
modele += xsum(-value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'B').items()) <= -150
modele += xsum(-value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'C').items()) <= -215
modele += xsum(-value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'D').items()) <= -180
modele += xsum(-value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'E').items()) <= -150
modele += xsum(-value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'F').items()) <= -100

# Contrainte : Il faut au moins produire 100m de plus de la bande A que de la bande C
modele += xsum(variables) - xsum(value * variables[key] for key, value in count_items_in_combinations(variables_combinaisons, 'A').items()) <= 100

# Optimisation du modèle
modele.optimize()

# Affichage des résultats
if modele.status == OptimizationStatus.OPTIMAL:
    for i, var in enumerate(variables):
        print(f"{variables_combinaisons[i]} = {var.x}")
    print(f"Bénéfice total : {modele.objective_value}")
else:
    print("Pas de solution possible")
