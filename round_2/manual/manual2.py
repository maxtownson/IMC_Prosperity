from itertools import permutations
from itertools import product

# Find maximum SHL
max_shl = 0
max_shl_path = None

# Define exchange rates
exchange_rates = {
    ('PIZ', 'WSB'): 0.48, ('PIZ', 'SNW'): 1.52, ('PIZ', 'SHL'): 0.71, ('PIZ', 'PIZ'): 1,
    ('WSB', 'PIZ'): 2.05, ('WSB', 'SNW'): 3.26, ('WSB', 'SHL'): 1.56, ('WSB', 'WSB'): 1,
    ('SNW', 'PIZ'): 0.64, ('SNW', 'WSB'): 0.3, ('SNW', 'SHL'): 0.46, ('SNW', 'SNW'): 1,
    ('SHL', 'PIZ'): 1.41, ('SHL', 'WSB'): 0.61, ('SHL', 'SNW'): 2.08, ('SHL', 'SHL'): 1
}

# Currencies
currencies = ['PIZ', 'WSB', 'SNW', 'SHL']

# Find maximum SHL
max_shl = 0
max_shl_path = None
counter = 0

for length in range(1, 5):
    permutations = product(currencies, repeat=length)
    # Generate all permutations of trades starting and ending with SHL
    for perm in permutations:
        path = ['SHL'] + list(perm) + ['SHL']
        shl_amount = 1
        counter += 1
        print(counter)
        for i in range(len(path) - 1):
            shl_amount *= exchange_rates[(path[i], path[i+1])]
        if shl_amount > max_shl:
            max_shl = shl_amount
            max_shl_path = path

print("Maximum return obtained:", max_shl)
print("Sequence of trades:", max_shl_path)