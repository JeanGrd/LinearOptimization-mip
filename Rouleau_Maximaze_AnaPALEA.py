# Import necessary modules from MIP library and utility functions
from mip import Model, MAXIMIZE, xsum, OptimizationStatus
from utils import count_items_in_combinations, generate_valid_combinations

# Define lengths and selling prices for items, and the cost per meter
lengths = {'A': 110, 'B': 92, 'C': 80, 'D': 74, 'E': 70, 'F': 65}
prix_vente = {'A': 100, 'B': 80, 'C': 70, 'D': 65, 'E': 60, 'F': 57}
cout_par_metre = 120

# Generate valid combinations of items within specified length constraints
combinaisons = generate_valid_combinations(lengths, 180, 245)

# Calculate values for each combination (revenue minus cost)
values_combinaisons = [sum(prix_vente[i] for i in comb) - cout_par_metre for comb in combinaisons]

# Create variable names for each combination
inconnus_combinaisons = ["x" + ''.join(comb) for comb in combinaisons]

# Print the variable names (for debugging or verification)
print(inconnus_combinaisons)

# Create an optimization model to maximize profit
m = Model("Rouleau", sense=MAXIMIZE)

# Add variables to the model for each combination
vars = [m.add_var(name=v) for v in inconnus_combinaisons]

# Define the objective function (maximize total value of combinations)
m.objective = xsum(values_combinaisons[i] * vars[i] for i in range(35))

# Add constraints for the number of each item used in the combinations
item_constraints = ['A', 'B', 'C', 'D', 'E', 'F']
for item in item_constraints:
    m += xsum(value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, item).items()) <= 400

# Add constraints to limit the number of certain items relative to the total number of items used
for item in item_constraints:
    m += xsum(value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, item).items()) <= 0.5 * xsum(
        (len(inconnus_combinaisons[indice])-1) * vars[indice] for indice, x in enumerate(inconnus_combinaisons))

# Additional constraint specific to items 'C' and 'A'
m += xsum(value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, 'C').items()) <= xsum(
    value * vars[key] for key, value in count_items_in_combinations(inconnus_combinaisons, 'A').items()) - 100

# Optimize the model
m.optimize()

# Check if an optimal solution was found and print results
if m.status == OptimizationStatus.OPTIMAL:
    for i, var in enumerate(vars):
        print(f"{inconnus_combinaisons[i]} = {var.x}")
    print(f"Total Cost: {m.objective_value}")
else:
    print("Impossible solution")
