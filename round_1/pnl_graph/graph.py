import csv
import pyqtgraph as pg
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QApplication
import pandas as pd
from file import createStarandAmyCSV
import numpy as np


def extract_data(csv_file):
    timestamps = []
    avg_price = []
    pnl = []

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            timestamp = int(row['timestamp'])
            avg = ((float(row['bid_price_1']) * float(row['bid_volume_1']) + float(row['ask_price_1']) * float(row['ask_volume_1'])) /
                   (float(row['bid_volume_1']) + float(row['ask_volume_1'])))
            
            timestamps.append(timestamp)
            avg_price.append(avg)
            pnl.append(float(row['profit_and_loss']))

    return timestamps, avg_price

def calculate_ema(mid_prices):
    """
    Calculates Exponential Moving Averages (EMAs) from a list of prices with a window size equal to the length of the list.

    Args:
    - prices (list): List of prices.

    Returns:
    - emas (list): List of EMAs corresponding to the input prices.
    """

    mid_price_vals = list(mid_prices.values())

    if len(mid_prices) < 2:
        raise ValueError("List must contain at least two values to calculate EMA.")

    emas = [mid_price_vals[0]]  # EMA for the first value is the value itself
    
    alpha = 0.1

    for i in range(1, len(mid_price_vals)):
        mid_price = mid_price_vals[i]
        ema = mid_price * alpha + (1 - alpha) * emas[-1]
        emas.append(ema)

    return emas

def get_mid_prices(csv_file):
    
    mid_prices = {}

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            time = int(row['timestamp'])

            bid_price = float(row['bid_price_1'])
            ask_price = float(row['ask_price_1'])
            bid_volume = float(row['bid_volume_1'])
            ask_volume = float(row['ask_volume_1'])

            vwap = ((bid_price * bid_volume) + (ask_price * ask_volume))  / (bid_volume + ask_volume)

            mid_prices[time] = vwap

    return mid_prices

def moving_averages(csv_file, j):
    rolling_averages = {}

    df = pd.read_csv(csv_file, sep=';')
    for i in range(5, len(df)):  # Start from 5th row to avoid index out of range
        selected_rows = df.loc[i-j:i]

        bid_prices = selected_rows['bid_price_1']
        ask_prices = selected_rows['ask_price_1']
        bid_volumes = selected_rows['bid_volume_1']
        ask_volumes = selected_rows['ask_volume_1']

        # Calculating volume-weighted average bid and ask prices
        vwap = ((bid_prices * bid_volumes).sum() + (ask_prices * ask_volumes).sum())  / (bid_volumes.sum() + ask_volumes.sum())

        timestamp = selected_rows['timestamp'].iloc[-1]  # Taking the timestamp of the last row
        rolling_averages[timestamp] = vwap

    return rolling_averages

def moving_averages_bid_ask(csv_file, j):
    rolling_averages_bid = {}
    rolling_averages_ask = {}

    df = pd.read_csv(csv_file, sep=';')
    for i in range(5, len(df)):  # Start from 5th row to avoid index out of range
        selected_rows = df.loc[i-j:i]

        bid_prices = selected_rows['bid_price_1']
        ask_prices = selected_rows['ask_price_1']
        bid_volumes = selected_rows['bid_volume_1']
        ask_volumes = selected_rows['ask_volume_1']

        # Calculating volume-weighted average bid and ask prices
        vwap_bid = (bid_prices * bid_volumes).sum() / bid_volumes.sum()
        vwap_ask = (ask_prices * ask_volumes).sum() / ask_volumes.sum()

        timestamp = selected_rows['timestamp'].iloc[-1]  # Taking the timestamp of the last row
        rolling_averages_bid[timestamp] = vwap_bid
        rolling_averages_ask[timestamp] = vwap_ask

    return rolling_averages_bid, rolling_averages_ask

def extract_trades(csv_file, mid_prices):
    trades_under = {}
    trades_over = {}
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            time = float(row['timestamp'])
            if 'traded_price' in row and row['traded_price']:  # Check if 'traded_price' exists and is not empty
                traded_price = float(row['traded_price'])
                if mid_prices[time] >= traded_price:
                    trades_over[time] = traded_price
                    trades_under[time] = np.nan
                else:
                    trades_under[time] = traded_price
                    trades_over[time] = np.nan
            else:
                trades_under[time] = np.nan
                trades_over[time] = np.nan # If 'traded_price' is missing or empty, use np.nan as a placeholder

    return trades_under, trades_over

def extract_results(csv_file):
    starfruit_pnl = []
    starfruit_positions = []
    amethyst_pnl = []
    amethyst_positions = []

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            starfruit_pnl.append(float(row['starfruit_pnl']))
            starfruit_positions.append(float(row['starfruit_positions']))
            amethyst_pnl.append(float(row['amethyst_pnl']))
            amethyst_positions.append(float(row['amethyst_positions']))

    return starfruit_pnl, starfruit_positions, amethyst_pnl, amethyst_positions

def orchid_results(csv_file):
    timestamp = []
    orchids = []
    transport_fees = []
    export_tariff = []
    import_tariff = []
    sunlight = []
    humidity = []

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            timestamp.append(float(row['timestamp']))
            orchids.append(float(row['ORCHIDS']))
            transport_fees.append(float(row['TRANSPORT_FEES']))
            export_tariff.append(float(row['EXPORT_TARIFF']))
            import_tariff.append(float(row['IMPORT_TARIFF']))
            sunlight.append(float(row['SUNLIGHT']))
            humidity.append(float(row['HUMIDITY']))

    return timestamp, orchids,transport_fees, export_tariff, import_tariff, sunlight, humidity
            

oldDataPath = "historical_data.csv"
amethystPath = 'amethysts_data.csv'   
starfruitPath = 'starfruit_data.csv'  
newDataPath = "additional.csv"

orchid_path = "orchid_data.csv"

createStarandAmyCSV(oldDataPath, amethystPath, starfruitPath)

# Extract and create amethyst and starfruit csv from results.csv
"""extractedStarData = moving_averages(starfruitPath, 1500)
furtherStarData = moving_averages(starfruitPath, 500)"""

extractedStarData, x = moving_averages_bid_ask(starfruitPath, 4500)
y, furtherStarData = moving_averages_bid_ask(starfruitPath, 500)

extractedAmyData = moving_averages(amethystPath, 900)

timestamps_amethyst, avg_price_amethyst = extract_data(amethystPath)
timestamps_starfruit, avg_price_starfruit = extract_data(starfruitPath)

pnl_starfruit, position_starfruit, pnl_amethyst, position_amethyst = extract_results(newDataPath)

mid_prices =get_mid_prices(starfruitPath)

#trades_under, trades_over = extract_trades('Cleaned_final_starfruit_data_trades.csv', mid_prices)

emas = calculate_ema(mid_prices)

timestamp, orchids, transport_fees, export_tariff, import_tariff, sunlight, humidity = orchid_results(orchid_path)

app = QApplication([])
win = pg.GraphicsLayoutWidget()

# First plot for amethyst average prices
plot_avg_price_amethyst = win.addPlot()
plot_avg_price_amethyst.setLabel('left', 'Price', color='black', **{'font-size': '14pt'})
plot_avg_price_amethyst.setLabel('bottom', 'Timestamp', color='black', **{'font-size': '14pt'})
original_amy = plot_avg_price_amethyst.plot(timestamps_amethyst, avg_price_amethyst, pen={'color': 'b', 'width': 3}, name='Original')
plot_avg_price_amethyst.setTitle(title="<span style='font-size: 18pt;'>Amethyst Volume Weighted Average Prices</span>", color='black')
legend_amy = plot_avg_price_amethyst.addLegend()

# Second plot for amethyst PnL
plot_pnl_amethyst = win.addPlot(row=1, col=0)
plot_pnl_amethyst.setLabel('left', 'PnL', color='black', **{'font-size': '14pt'})
plot_pnl_amethyst.setLabel('bottom', 'Timestamp', color='black', **{'font-size': '14pt'})
plot_pnl_amethyst.plot(timestamps_amethyst, pnl_amethyst, pen={'color': 'g', 'width': 3})
plot_pnl_amethyst.setTitle(title="<span style='font-size: 18pt;'>Amethyst PnL</span>", color='black')

# Third plot for starfruit average prices
plot_avg_price_starfruit = win.addPlot(row=0, col=1)
plot_avg_price_starfruit.setLabel('left', 'Price', color='black', **{'font-size': '14pt'})
plot_avg_price_starfruit.setLabel('bottom', 'Timestamp', color='black', **{'font-size': '14pt'})
original_starfruit = plot_avg_price_starfruit.plot(timestamps_starfruit, avg_price_starfruit, pen={'color': 'b', 'width': 3}, name='Original')
#moving_avg_starfruit_900 = plot_avg_price_starfruit.plot(list(extractedStarData.keys()), list(extractedStarData.values()), pen={'color': 'r', 'width': 3}, name='900 Moving Average')
#moving_avg_starfruit_300 = plot_avg_price_starfruit.plot(list(furtherStarData.keys()), list(furtherStarData.values()), pen={'color': 'g', 'width': 3}, name='300 Moving Average')
#manual_trades_plot_under = plot_avg_price_starfruit.plot(list(trades_under.keys()), list(trades_under.values()), pen={'color': 'r', 'width': 3}, name='300 Moving Average')
#manual_trades_plot_under = plot_avg_price_starfruit.plot(list(trades_over.keys()), list(trades_over.values()), pen={'color': 'g', 'width': 3}, name='300 Moving Average')
#emas_plot = plot_avg_price_starfruit.plot(list(timestamps_starfruit), list(emas), pen={'color': 'g', 'width': 3}, name='300 Moving Average')

plot_avg_price_starfruit.setTitle(title="<span style='font-size: 18pt;'>Starfruit Volume Weighted Average Prices</span>", color='black')
legend_starfruit = plot_avg_price_starfruit.addLegend()

# Fourth plot for starfruit PnL (changed to volatility for one second)
plot_pnl_starfruit = win.addPlot(row=1, col=1)
plot_pnl_starfruit.setLabel('left', 'PnL', color='black', **{'font-size': '14pt'})
plot_pnl_starfruit.setLabel('bottom', 'Timestamp', color='black', **{'font-size': '14pt'})
plot_pnl_starfruit.plot(timestamps_starfruit, pnl_starfruit, pen={'color': 'g', 'width': 3})
plot_pnl_starfruit.setTitle(title="<span style='font-size: 18pt;'>Starfruit PnL</span>", color='black')


# Fifth plot for amethyst positions
plot_positions_amethyst = win.addPlot(row=2, col=0)
plot_positions_amethyst.setLabel('left', 'Position', color='black', **{'font-size': '14pt'})
plot_positions_amethyst.setLabel('bottom', 'Timestamp', color='black', **{'font-size': '14pt'})
plot_positions_amethyst.plot(timestamps_amethyst, position_amethyst, pen={'color': 'm', 'width': 3})
plot_positions_amethyst.setTitle(title="<span style='font-size: 18pt;'>Amethyst Positions</span>", color='black')

# Sixth plot for starfruit positions
plot_positions_starfruit = win.addPlot(row=2, col=1)
plot_positions_starfruit.setLabel('left', 'Position', color='black', **{'font-size': '14pt'})
plot_positions_starfruit.setLabel('bottom', 'Timestamp', color='black', **{'font-size': '14pt'})
plot_positions_starfruit.plot(timestamps_starfruit, position_starfruit, pen={'color': 'm', 'width': 3})
plot_positions_starfruit.setTitle(title="<span style='font-size: 18pt;'>Starfruit Positions</span>", color='black')

# Set background to white
win.setBackground('w')

# Set bold font for tick labels on x and y axes for the first plot
ax_avg_price_amethyst = plot_avg_price_amethyst.getAxis('bottom')
ax_avg_price_amethyst.setTickFont(QFont('Arial', 10, QFont.Bold))
ax_avg_price_amethyst.setPen(color=QColor('black'))

ay_avg_price_amethyst = plot_avg_price_amethyst.getAxis('left')
ay_avg_price_amethyst.setTickFont(QFont('Arial', 10, QFont.Bold))
ay_avg_price_amethyst.setPen(color=QColor('black'))

# Set bold font for tick labels on x and y axes for the second plot
ax_pnl_amethyst = plot_pnl_amethyst.getAxis('bottom')
ax_pnl_amethyst.setTickFont(QFont('Arial', 10, QFont.Bold))
ax_pnl_amethyst.setPen(color=QColor('black'))

ay_pnl_amethyst = plot_pnl_amethyst.getAxis('left')
ay_pnl_amethyst.setTickFont(QFont('Arial', 10, QFont.Bold))
ay_pnl_amethyst.setPen(color=QColor('black'))

# Set bold font for tick labels on x and y axes for the third plot
ax_avg_price_starfruit = plot_avg_price_starfruit.getAxis('bottom')
ax_avg_price_starfruit.setTickFont(QFont('Arial', 10, QFont.Bold))
ax_avg_price_starfruit.setPen(color=QColor('black'))

ay_avg_price_starfruit = plot_avg_price_starfruit.getAxis('left')
ay_avg_price_starfruit.setTickFont(QFont('Arial', 10, QFont.Bold))
ay_avg_price_starfruit.setPen(color=QColor('black'))

# Set bold font for tick labels on x and y axes for the fourth plot
ax_pnl_starfruit = plot_pnl_starfruit.getAxis('bottom')
ax_pnl_starfruit.setTickFont(QFont('Arial', 10, QFont.Bold))
ax_pnl_starfruit.setPen(color=QColor('black'))

ay_pnl_starfruit = plot_pnl_starfruit.getAxis('left')
ay_pnl_starfruit.setTickFont(QFont('Arial', 10, QFont.Bold))
ay_pnl_starfruit.setPen(color=QColor('black'))

win.setGeometry(100, 100, 1800, 900)

win.show()

if __name__ == '__main__':
    QApplication.instance().exec_()
