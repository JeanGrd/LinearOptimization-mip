from mip import Model, MAXIMIZE, xsum, OptimizationStatus
from utils import generate_valid_combinations, count_items_in_combinations

# Variable definitions
widths = {'A': 110, 'B': 92, 'C': 80, 'D': 74, 'E': 70, 'F': 65}
selling_prices = {'A': 100, 'B': 80, 'C': 70, 'D': 65, 'E': 60, 'F': 57}
cost_per_meter = 120

# Generate valid combinations of widths within specified length range
combinations = generate_valid_combinations(widths, 180, 245)

# Calculate the net value of each combination
net_values = [sum(selling_prices[i] for i in comb) - cost_per_meter for comb in combinations]
variable_names = ["x" + ''.join(comb) for comb in combinations]

# Model initialization
model = Model("Rouleau", sense=MAXIMIZE)
variables = [model.add_var(name=name) for name in variable_names]

# Setting the objective function
model.objective = xsum(net_values[i] * variables[i] for i in range(len(net_values)))

#Contraints
items_constraints = {item: 400 for item in widths.keys()}
half_constraints = {item: 0.5 for item in widths.keys()}
special_constraint_items = ['C', 'A']

for item in widths.keys():
    item_counts = count_items_in_combinations(combinations, item)
    model += xsum(count * variables[idx] for idx, count in item_counts.items()) <= items_constraints[item]
    model += xsum(count * variables[idx] for idx, count in item_counts.items()) <= half_constraints[item] * xsum(variables)

c_counts = count_items_in_combinations(combinations, 'C')
a_counts = count_items_in_combinations(combinations, 'A')
model += xsum(count * variables[idx] for idx, count in c_counts.items()) <= 100 + xsum(count * variables[idx] for idx, count in a_counts.items())

model.optimize()

if model.status == OptimizationStatus.OPTIMAL:
    for name, var in zip(variable_names, variables):
        print(f"{name} = {var.x}")
    print(f"Total cost: {model.objective_value}")
else:
    print("Impossible solution")
