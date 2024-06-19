import pandas as pd
import matplotlib.pyplot as plt

# Step 2: Load the data
data = pd.read_csv("test_orchid.csv", delimiter=';')

# Step 3: Prepare data for plotting
# Assuming you want to plot bid price 1 and ask price 1 against time for the product "ORCHIDS"
orchid_data = data[data['product'] == 'ORCHIDS']
timestamps = orchid_data['timestamp']
bid_price_1 = orchid_data['bid_price_1']
ask_price_1 = orchid_data['ask_price_1']

# Step 4: Plot the data
plt.figure(figsize=(10, 6))
plt.plot(timestamps, bid_price_1, label='Bid Price 1', marker='o')
plt.plot(timestamps, ask_price_1, label='Ask Price 1', marker='o')

plt.title('Bid Price 1 and Ask Price 1 Over Time for ORCHIDS')
plt.xlabel('Timestamp')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

plt.tight_layout()
plt.show()
