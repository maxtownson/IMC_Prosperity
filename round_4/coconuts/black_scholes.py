import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np

STRIKE = 10000
RF = -0.052855941708912724
VOL = 0.24086532541788852
EXPIRY = 250/365

df = pd.read_csv("r4_data.csv", delimiter=',')

# Separate data for COCONUT and COCONUT_COUPON
coconut_data = df[df['product'] == 'COCONUT']
coconut_coupon_data = df[df['product'] == 'COCONUT_COUPON']

# Merge the two DataFrames on the 'timestamp' column
merged_df = pd.merge(coconut_data[['timestamp', 'mid_price']], coconut_coupon_data[['timestamp', 'mid_price']], on='timestamp', suffixes=('_coconut', '_coconut_coupon'))

log_squared_coconut = (np.log(merged_df['mid_price_coconut'] / merged_df['mid_price_coconut'].shift(1))) ** 2

log_returns_coconut_sum = log_squared_coconut.sum()
log_returns_coconut_length = 20000

volatility = np.sqrt((1 / (log_returns_coconut_length - 1)) * log_returns_coconut_sum)

annual_vol = volatility / (np.sqrt(1/(10000 * 365)))

def black_scholes_call(S):
    d1 = (np.log(S / STRIKE) + (RF + 0.5 * VOL**2) * EXPIRY) / (VOL * np.sqrt(EXPIRY))
    d2 = d1 - VOL * np.sqrt(EXPIRY)
    call_price = S * norm.cdf(d1) - STRIKE * np.exp(-RF * EXPIRY) * norm.cdf(d2)
    return call_price

# Given data
S = 10000
X = 10000
r = -0.052855941708912724
t = 250/365
sigma = annual_vol

# Calculate call option price
call_price = black_scholes_call(S)

# Calculate call option price for each mid_price_coupon
merged_df['call_option_price'] = black_scholes_call(merged_df['mid_price_coconut'])
# Create subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# Plot mid_price_coupon and call_option_price separately
axs[0].plot(merged_df['timestamp'], merged_df['mid_price_coconut_coupon'] - merged_df['call_option_price'], label='price difference - black scholes (profit opportunities)', color='blue')
axs[0].set_ylabel('Price')
axs[0].set_title('Mid Price Coupon over Time')
axs[0].legend()
axs[0].grid(True)

# Plot mid_price_coupon and call_option_price separately
axs[1].plot(merged_df['timestamp'], merged_df['mid_price_coconut_coupon'], label='Mid Price Coupon', color='red')
axs[1].plot(merged_df['timestamp'], merged_df['call_option_price'], label='Black-Scholes Call Option Price', color='blue')
axs[1].set_xlabel('Timestamp')
axs[1].set_ylabel('Price')
axs[1].set_title('Black-Scholes Call Option Price over Time')
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()
plt.show()