import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


z = 0.5
percent = (norm.cdf(z) - 0.5) 
print(percent)

hello = 6 + 4 * 1.9656933442176188 + 3.6026796488094828

df = pd.read_csv("r3_data.csv", delimiter=',')

# Calculate midprice for each asset
df['midprice'] = (df['bid_price_1'] + df['ask_price_1']) / 2

# Filter data for each asset
strawberries = df[df['product'] == 'STRAWBERRIES'][['timestamp', 'bid_price_1', 'ask_price_1']]
chocolate = df[df['product'] == 'CHOCOLATE'][['timestamp', 'bid_price_1', 'ask_price_1']]
roses = df[df['product'] == 'ROSES'][['timestamp', 'bid_price_1', 'ask_price_1']]
gift_basket = df[df['product'] == 'GIFT_BASKET'][['timestamp', 'bid_price_1', 'ask_price_1']]

# Merge data frames based on timestamp with left join
merged_df = strawberries.merge(chocolate, on='timestamp', suffixes=('_straweberries', '_chocolate'), how='left')
merged_df = merged_df.merge(roses, on='timestamp', suffixes=('_straweberries', '_roses'), how='left')
merged_df = merged_df.merge(gift_basket, on='timestamp', suffixes=('_roses', '_gift_basket'), how='left')

weighted_sum = (4 * merged_df['bid_price_1_chocolate'] +
                6 * merged_df['bid_price_1_straweberries'] +
                1 * merged_df['bid_price_1_roses'] +
                355)

weighted_df = pd.DataFrame({'timestamp': merged_df['timestamp'], 'weighted_sum': weighted_sum})

# Add bid price 1 of gift basket to the weighted_df
weighted_df['ask_price_1_gift_basket'] = merged_df['ask_price_1_gift_basket']

# Filter out values less than 0
"""filtered_values = weighted_df['bid_price_1_gift_basket'] - weighted_df['weighted_sum']
filtered_timestamps = weighted_df['timestamp'][filtered_values >= 0]
filtered_values = filtered_values[filtered_values >= 0]"""

# Calculate the standard deviation
std_dev = np.std(weighted_df['weighted_sum']- weighted_df['ask_price_1_gift_basket'])
print(std_dev)

# Calculate modified ask price for gift basket
modified_ask_price = merged_df['bid_price_1_straweberries'] - (merged_df['ask_price_1_gift_basket'] - 355) / hello

print(np.std(modified_ask_price))

df2 = pd.read_csv("DATASELL.csv", delimiter=',')
print(df2)

df3 = pd.read_csv("DATABUY.csv", delimiter=',')

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(weighted_df['timestamp'], weighted_df['weighted_sum']- weighted_df['ask_price_1_gift_basket'], label='Strawberries Bid Price 1 - Modified Gift Basket Ask Price', color='blue')
plt.xlabel('Timestamp')
plt.ylabel('Price Difference')
plt.title('Difference between Strawberries Bid Price 1 and Modified Gift Basket Ask Price')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plotting ask price 1 for strawberries
plt.figure(figsize=(10, 6))
plt.plot(weighted_df['timestamp'], (merged_df['bid_price_1_chocolate'] + merged_df['ask_price_1_chocolate']) / 2, label='choco Ask vs bid Price 1', color='red')
plt.plot(df2['timestamp'], df2['price'], color='green', marker='o', label="buys")
plt.plot(df3['timestamp'], df3['price'], color='purple', marker='o', label="sells")
plt.xlabel('Timestamp')
plt.ylabel('Ask Price 1')
plt.title('Ask Price 1 of Strawberries Over Time')

plt.legend()
plt.grid(True)
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()