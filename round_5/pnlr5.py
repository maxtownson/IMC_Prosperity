import csv
import tkinter as tk
from tkinter import ttk

trader_trades = {
    'Valentina': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Vinnie': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Vladimir': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Vivian': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Celeste': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Colin': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Carlos': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Camilla': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Pablo': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Penelope': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Percy': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Petunia': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Ruby': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Remy': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Rhianna': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Raj': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Amelia': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Adam': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Alina': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}},
    'Amir': {'STARFRUIT': {}, 'AMETHYSTS': {}, 'GIFT_BASKET': {}, 'ROSES': {}, 'CHOCOLATE': {}, 'STRAWBERRIES': {}, 'COCONUT_COUPON': {}, 'COCONUT': {}}
}

symbol_closings = {
    'STARFRUIT': {'bid': 5048, 'ask': 5054},
    'AMETHYSTS': {'bid': 9996, 'ask': 10004},
    'ROSES': {'bid': 14411, 'ask': 14412},
    'STRAWBERRIES': {'bid': 3984, 'ask': 3985},
    'GIFT_BASKET': {'bid': 69551, 'ask': 69561},
    'CHOCOLATE': {'bid': 7749, 'ask': 7751},
    'COCONUT_COUPON': {'bid': 575, 'ask': 576},
    'COCONUT': {'bid': 9882, 'ask': 9883}
}

def read_trades(file_name):
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            trader = row['buyer']
            seller = row['seller']
            symbol = row['symbol']
            price = float(row['price'])
            quantity = int(row['quantity'])

            if trader in trader_trades:
                if symbol in trader_trades[trader]:
                    if price in trader_trades[trader][symbol]:
                        trader_trades[trader][symbol][price] += quantity
                    else:
                        trader_trades[trader][symbol][price] = quantity
                else:
                    trader_trades[trader][symbol] = {price: quantity}
            else:
                trader_trades[trader] = {symbol: {price: quantity}}

            if seller in trader_trades:
                if symbol in trader_trades[seller]:
                    if price in trader_trades[seller][symbol]:
                        trader_trades[seller][symbol][price] -= quantity
                    else:
                        trader_trades[seller][symbol][price] = -quantity
                else:
                    trader_trades[seller][symbol] = {price: -quantity}
            else:
                trader_trades[seller] = {symbol: {price: -quantity}}

def calculate_pnl(symbol, trader_trades):
    pnl_data = {}
    for trader, trades in trader_trades.items():
        pnl = 0
        for trade_symbol, transactions in trades.items():
            for price, quantity in transactions.items():
                if trade_symbol == symbol:
                    pnl += price * -quantity

        if (sum(trades[symbol].values())) > 0:
            pnl += (symbol_closings[symbol]['ask'] * (sum(trades[symbol].values())))
        elif (sum(trades[symbol].values())) < 0:
            pnl += (symbol_closings[symbol]['bid'] * (sum(trades[symbol].values())))

        pnl_data[trader] = pnl
    return pnl_data

def print_pnl_table(all_pnl, window):
    pnl_window = tk.Toplevel(window)
    pnl_window.title("PnL Table")

    tree = ttk.Treeview(pnl_window)

    tree["columns"] = tuple(all_pnl['STARFRUIT'].keys())

    tree.heading("#0", text="Trader")
    for col in tree["columns"]:
        tree.heading(col, text=col)

    for trader, pnl_data in all_pnl.items():
        tree.insert("", "end", text=trader, values=tuple(pnl_data.values()))

    tree.pack(expand=True, fill="both")

def main():
    read_trades('r5_trades_r1.csv')
    all_pnl = {}
    print(trader_trades)
    all_pnl['STARFRUIT'] = calculate_pnl('STARFRUIT', trader_trades)
    all_pnl['AMETHYSTS'] = calculate_pnl('AMETHYSTS', trader_trades)

    read_trades('r5_trades_r3.csv')
    all_pnl['ROSES'] = calculate_pnl('ROSES', trader_trades)
    all_pnl['STRAWBERRIES'] = calculate_pnl('STRAWBERRIES', trader_trades)
    all_pnl['GIFT_BBASKET'] = calculate_pnl('GIFT_BASKET', trader_trades)
    all_pnl['CHOCOLATE'] = calculate_pnl('CHOCOLATE', trader_trades)

    read_trades('r5_trades_r4.csv')
    all_pnl['COCONUT_COUPON'] = calculate_pnl('COCONUT_COUPON', trader_trades)
    all_pnl['COCONUT'] = calculate_pnl('COCONUT', trader_trades)

    print_pnl_table(all_pnl, tk.Tk())

    tk.mainloop()

if __name__ == "__main__":
    main()
