treasure_vals = {180000: 2, 525000: 4, 307500: 3, 157500: 2, 450000: 4,
                 352500: 3, 615000: 5, 652500: 5, 600000: 5, 262500: 3,
                 547500: 4, 667500: 5, 750000: 8, 675000: 7, 127500: 2,
                 577500: 5, 622500: 5, 637500: 5, 592500: 5, 412500: 4,
                 90000: 2, 202500: 3, 390000: 4, 112500: 2, 225000: 3}

even_distribution = {}
expected_val = []
diffs = []
proportion = {}

even_percent = 4

for i, (money, hunters) in enumerate(treasure_vals.items()):
    even_distribution[i] = money / (hunters + even_percent)

print(sorted(list(even_distribution.values())))