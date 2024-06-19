import csv
import matplotlib.pyplot as plt
import pandas as pd

def calculate_averages(rows):
    bid_price_values = [int(row['bid_price_1']) for row in rows]
    ask_price_values = [int(row['ask_price_1']) for row in rows]
    spread_price_values = [ask - bid for bid, ask in zip(bid_price_values, ask_price_values)]
    average_price_values = [(ask + bid) / 2 for bid, ask in zip(bid_price_values, ask_price_values)]

    bid_price_length = len(bid_price_values)
    avg_bid_price = sum(bid_price_values) / bid_price_length
    print(f"Average bid price is {int(avg_bid_price)}")

    ask_price_length = len(ask_price_values)
    avg_ask_price = sum(ask_price_values) / ask_price_length
    print(f"Average ask price is {int(avg_ask_price)}")

    spread_price_length = len(spread_price_values)
    avg_spread_price = sum(spread_price_values) / spread_price_length
    print(f"Average spread difference is {int(avg_spread_price)}")

    print(f"Maximum spread is {max(spread_price_values)}")

    average_price_length = len(average_price_values)
    avg_average_price = sum(average_price_values) / average_price_length
    print(f"Average average price is {int(avg_average_price)}")

    return bid_price_values, avg_bid_price, ask_price_values, avg_ask_price

def get_mean(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        rows = list(reader)

    return calculate_averages(rows)

def distribution(values, average, type: str):
    prob_distrib = {i - average: 0 for i in range(9990, 10010)}

    for value in values:
        diff = value - average
        if diff in prob_distrib:
            prob_distrib[diff] += 1
        else:
            print("fail")
    
    with open(f'amethyst_{type}_distribution.csv', 'w', newline ='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["deviation", "frequency"])

        for deviation, frequency in prob_distrib.items():
            csv_writer.writerow([deviation, frequency])

    return

def plot_distribution(csv_file, type):
    df = pd.read_csv(csv_file)
    
    frequency = df['frequency']
    deviation = df['deviation']

    plt.bar(deviation, frequency)

    plt.xlabel('deviation')
    plt.ylabel('frequency')
    plt.title(f'frequency against distribution for {type}')

    plt.show()

def moving_averages(csv_file):
    rolling_averages = {}

    df = pd.read_csv(csv_file, sep=';')
    for i in range(5, len(df)):  # Start from 5th row to avoid index out of range
        selected_rows = df.loc[i-5:i]

        bid_prices = selected_rows['bid_price_1']
        ask_prices = selected_rows['ask_price_1']
        bid_volumes = selected_rows['bid_volume_1']
        ask_volumes = selected_rows['ask_volume_1']
        
        # Calculating volume-weighted average bid and ask prices
        vwap = ((bid_prices * bid_volumes).sum() + (ask_prices * ask_volumes).sum())  / (bid_volumes.sum() + ask_volumes.sum())

        timestamp = selected_rows['timestamp'].iloc[-1]  # Taking the timestamp of the last row
        rolling_averages[timestamp] = vwap

    return rolling_averages

def plot_ma(roll_avg):

    time = list(roll_avg.keys())
    rolling_avg = list(roll_avg.values())

    plt.plot(time, rolling_avg, color='b')
    plt.title('7-Day Average Over Time')
    plt.xlabel('Time')
    plt.ylabel('7-Day Average')
    plt.grid(True)
    plt.show()
 
if __name__ == "__main__":
    bid_values, bid_average, ask_values, ask_average = get_mean("amethysts_data.csv")
    distribution(bid_values, 10000, "bid")
    distribution(ask_values, 10000, "ask")
    plot_distribution("amethyst_bid_distribution.csv", "bid")
    plot_distribution("amethyst_ask_distribution.csv", "ask")
    data = moving_averages("starfruit_data.csv")
    plot_ma(data)
