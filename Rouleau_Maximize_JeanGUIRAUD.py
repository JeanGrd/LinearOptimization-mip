from mip import Model, MAXIMIZE, xsum, OptimizationStatus
from utils import generate_valid_combinations, count_items_in_combinations

# Variable definitions
widths = {'A': 110, 'B': 92, 'C': 80, 'D': 74, 'E': 70, 'F': 65}
selling_prices = {'A': 100, 'B': 80, 'C': 70, 'D': 65, 'E': 60, 'F': 57}
cost_per_meter = 120

# Generate valid combinations of widths within specified length range
combinations = generate_valid_combinations(widths, 190, 255)

# Calculate the net value of each combination
net_values = [sum(selling_prices[i] for i in comb) - cost_per_meter for comb in combinations]
variable_names = ["x" + ''.join(comb) for comb in combinations]

# Model initialization
model = Model("Rouleau", sense=MAXIMIZE)
variables = [model.add_var(name=name) for name in variable_names]

# Setting the objective function
model.objective = xsum(net_values[i] * variables[i] for i in range(len(net_values)))

# Constraints
requirements = {'A': 200, 'B': 150, 'C': 215, 'D': 180, 'E': 150, 'F': 100}
for item, requirement in requirements.items():
    model += xsum(count * variables[index] for index, count in
                  count_items_in_combinations(variable_names, item).items()) >= requirement

model += xsum(variables) <= 1000

constraint_C = count_items_in_combinations(variable_names, 'C')
constraint_A = count_items_in_combinations(variable_names, 'A')

model += xsum(count * variables[index] for index, count in constraint_C.items()) <= 100 + xsum(
    count * variables[index] for index, count in constraint_A.items())

model.optimize()

if model.status == OptimizationStatus.OPTIMAL:
    for name, var in zip(variable_names, variables):
        print(f"{name} = {var.x}")
    print(f"Total cost: {model.objective_value}")
else:
    print("Impossible solution")
