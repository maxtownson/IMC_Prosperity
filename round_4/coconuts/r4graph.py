import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

df = pd.read_csv("r4_data.csv", delimiter=',')

# Separate data for COCONUT and COCONUT_COUPON
coconut_data = df[df['product'] == 'COCONUT']
coconut_coupon_data = df[df['product'] == 'COCONUT_COUPON']

# Merge the two DataFrames on the 'timestamp' column
merged_df = pd.merge(coconut_data[['timestamp', 'mid_price']], coconut_coupon_data[['timestamp', 'mid_price']], on='timestamp', suffixes=('_coconut', '_coconut_coupon'))

correlation_coefficient = merged_df['mid_price_coconut'].corr(merged_df['mid_price_coconut_coupon'])

stdev = np.std(merged_df['mid_price_coconut'])

# Calculate the difference between the mid prices
merged_df['coconut_price_change'] = merged_df['mid_price_coconut'] - 10000.0
merged_df['coupon_price_change'] = merged_df['mid_price_coconut_coupon'] - 637.5

# Filter out rows where coupon_price_change is zero
valid_rows = merged_df['coupon_price_change'] != 0

print(merged_df['mid_price_coconut'].mean())
print(merged_df['mid_price_coconut_coupon'].mean())

# Calculate the average ratio
average_ratio = (merged_df.loc[valid_rows, 'coconut_price_change'] / merged_df.loc[valid_rows, 'coupon_price_change']).mean()

#print("Average Ratio:", average_ratio)
merged_df['coconut_price_change_50'] = merged_df['mid_price_coconut'] - merged_df['mid_price_coconut'].shift(50)
merged_df['coupon_price_change_50'] = merged_df['mid_price_coconut_coupon'] - merged_df['mid_price_coconut_coupon'].shift(50)
merged_df['delta'] = merged_df['coupon_price_change_50'] - merged_df['coconut_price_change_50']
merged_df['gamma'] = (merged_df['delta'] - merged_df['delta'].shift(50)) / (merged_df['coconut_price_change_50'])

# Plotting Coconut midprice against time
plt.figure(figsize=(10, 6))
plt.plot(coconut_data['timestamp'], merged_df['coconut_price_change_50'], label='COCONUT', marker='o')
plt.xlabel('Timestamp')
plt.ylabel('price change sensitivity')
plt.title('Coconut Price Change Sensitivity (50 timestamps ago)')
plt.legend()
plt.grid(True)
plt.show()

sensitivity_50 = merged_df['coupon_price_change_50'] / merged_df['coconut_price_change_50']

# Plotting Coconut midprice sensitivity against time
plt.figure(figsize=(10, 6))
plt.plot(coconut_data['timestamp'], merged_df['coupon_price_change_50'], label='COCONUT', marker='o')
plt.xlabel('Timestamp')
plt.ylabel('price change')
plt.title('coupon Price Change Sensitivity (50 timestamps ago)')
plt.legend()
plt.grid(True)
plt.show()

valid_rows_50 = merged_df['coupon_price_change_50'] != 0
delta = merged_df.loc[valid_rows_50, 'coconut_price_change_50'] / merged_df.loc[valid_rows_50, 'coupon_price_change_50']
print(delta.mean())

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Creating a single figure with two subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

# Plotting sensitivity_50 in the first subplot
ax1.plot(coconut_data['timestamp'], merged_df['gamma'], label='Delta (COCONUT / COCONUT_COUPON)')
ax1.set_xlabel('Timestamp')
ax1.set_ylabel('Delta (COCONUT / COCONUT_COUPON)')
ax1.set_title('Delta (50 timestamps ago)')
ax1.legend(loc='upper left')
ax1.grid(True)

df1 = pd.read_csv("DATASELL.csv", delimiter=',')
df2 = pd.read_csv('DATABUY.csv', delimiter=',')

# Plotting mid price of coupons and mid price of COCONUT in the second subplot
ax2.plot(coconut_data['timestamp'], merged_df['mid_price_coconut_coupon'], color='red', label='Mid Price of Coupons')
ax3.plot(df1['timestamp'], df1['price'], label='Sell', color='red', marker='o')
ax3.plot(df2['timestamp'], df2['price'], label='Buy', color='green', marker='o')
ax2.set_xlabel('Timestamp')
ax2.set_ylabel('Mid Price')
ax2.legend(loc='upper right')
ax2.grid(True)

ax3.plot(coconut_data['timestamp'], merged_df['mid_price_coconut'], color='blue', label='Mid Price of Coconuts')
ax3.set_xlabel('Timestamp')
ax3.set_ylabel('Mid Price')
ax3.legend(loc='upper right')
ax3.grid(True)

plt.tight_layout()
plt.show()







# Function to extract z_values
def extract_z_values(log_file, limit=None):
    pattern = r"\[(-?\d+\.\d+)\]x"
    z_values = []
    with open(log_file, "r") as file:
        for line in file:
            matches = re.findall(pattern, line)
            if matches:
                z_values.extend(matches)
            if limit and len(z_values) >= limit:
                break
    return [float(value) for value in z_values]

# Step 1: Calculate daily returns
merged_df['coconut_return'] = merged_df['mid_price_coconut'].pct_change()
merged_df['coupon_return'] = merged_df['mid_price_coconut_coupon'].pct_change()

# Step 2: Compute daily volatility
coconut_volatility = np.std(merged_df['coconut_return']) * np.sqrt(250)  # Annualize volatility
coconut_coupon_volatility = np.std(merged_df['coupon_return']) * np.sqrt(250)  # Annualize volatility

# Step 3: Black-Scholes calculation
def black_scholes(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return call_price, put_price

# Parameters
strike_price = 10000
time_to_maturity = 250 / 365  # Convert days to years
risk_free_rate = 0.10  # 4.5% annualized

# Call option price estimation
coconut_call_price, _ = black_scholes(merged_df['mid_price_coconut'], strike_price, time_to_maturity, risk_free_rate, coconut_volatility)

# Put option price estimation (optional)
# coconut_put_price, _ = black_scholes(merged_df['mid_price_coconut'], strike_price, time_to_maturity, risk_free_rate, coconut_volatility)

# Visualize results
plt.figure(figsize=(10, 6))
plt.plot(merged_df['timestamp'], coconut_call_price, label='Estimated Call Option Price')
plt.plot(merged_df['timestamp'], merged_df['mid_price_coconut_coupon'], label='Actual Coconut Option Mid Price')
plt.xlabel('Timestamp')
plt.ylabel('Option Price')
plt.title('Black-Scholes Estimated vs. Actual Coconut Option Mid Price')
plt.legend()
plt.show()