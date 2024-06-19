import tkinter as tk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming you have the data stored in a CSV file named 'trades.csv'
df = pd.read_csv('pnl_output_per.csv')

def create_gui(root):
    # Group the data by 'Symbol'
    grouped_data = df.groupby('Symbol')
    
    # Create a separate heatmap for each tradable good
    for symbol, group in grouped_data:
        # Pivot the data to create a matrix of trader against counterparty for the current tradable good
        matrix_df = group.pivot_table(index='Trader', columns='Counterparty', values='PnL', aggfunc='sum', fill_value=0)
        
        # Create a larger figure
        plt.figure(figsize=(10, 8))
        
        # Create the heatmap plot
        sns.heatmap(matrix_df, annot=True, fmt=".1f", cmap="coolwarm", linewidths=.5)
        plt.title(f"{symbol} Trader vs Counterparty PnL Matrix")
        plt.xlabel("Counterparty")
        plt.ylabel("Trader")
        
        # Display the plot
        plt.show()

# Create the main application window
root = tk.Tk()
root.title("Trading Data GUI")


# Set the window size
root.geometry("300x100")

# Create and display the GUI
create_gui(root)

# Run the main event loop
root.mainloop()
