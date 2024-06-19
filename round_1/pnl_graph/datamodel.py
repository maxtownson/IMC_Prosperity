import json
from typing import Dict, List
from json import JSONEncoder
import jsonpickle
import pandas as pd
import csv
import numpy as np

Time = int
Symbol = str
Product = str
Position = int
UserId = str
ObservationValue = int
AMETHYST = "AMETHYSTS"
STARFRUIT = "STARFRUIT"
SEASHELLS = "SEASHELLS"

class Listing:

    def __init__(self, symbol: Symbol, product: Product, denomination: Product):
        self.symbol = symbol
        self.product = product
        self.denomination = denomination
           
                 
class ConversionObservation:

    def __init__(self, bidPrice: float, askPrice: float, transportFees: float, exportTariff: float, importTariff: float, sunlight: float, humidity: float):
        self.bidPrice = bidPrice
        self.askPrice = askPrice
        self.transportFees = transportFees
        self.exportTariff = exportTariff
        self.importTariff = importTariff
        self.sunlight = sunlight
        self.humidity = humidity


class Observation:

    def __init__(self, plainValueObservations: Dict[Product, ObservationValue], conversionObservations: Dict[Product, ConversionObservation]) -> None:
        self.plainValueObservations = plainValueObservations
        self.conversionObservations = conversionObservations
        
    def __str__(self) -> str:
        return "(plainValueObservations: " + jsonpickle.encode(self.plainValueObservations) + ", conversionObservations: " + jsonpickle.encode(self.conversionObservations) + ")"


class Order:

    def __init__(self, symbol: Symbol, price: int, quantity: int) -> None:
        self.symbol = symbol
        self.price = price
        self.quantity = quantity

    def __str__(self) -> str:
        return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"

    def __repr__(self) -> str:
        return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"


class OrderDepth:

    def __init__(self, buy_orders: Dict[int, int] = None, sell_orders: Dict[int, int] = None):
        if buy_orders is None:
            self.buy_orders = {}
        else:
            self.buy_orders = buy_orders

        if sell_orders is None:
            self.sell_orders = {}
        else:
            self.sell_orders = sell_orders


class Trade:

    def __init__(self, symbol: Symbol, price: int, quantity: int, buyer: UserId=None, seller: UserId=None, timestamp: int=0) -> None:
        self.symbol = symbol
        self.price: int = price
        self.quantity: int = quantity
        self.buyer = buyer
        self.seller = seller
        self.timestamp = timestamp

    def __str__(self) -> str:
        return "(" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ", " + str(self.timestamp) + ")"

    def __repr__(self) -> str:
        return "(" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ", " + str(self.timestamp) + ")"


class TradingState(object):

    def __init__(self,
                 traderData: str,
                 timestamp: Time,
                 listings: Dict[Symbol, Listing],
                 order_depths: Dict[Symbol, OrderDepth],
                 own_trades: Dict[Symbol, List[Trade]],
                 market_trades: Dict[Symbol, List[Trade]],
                 position: Dict[Product, Position],
                 observations: Observation):
        self.traderData = traderData
        self.timestamp = timestamp
        self.listings = listings
        self.order_depths = order_depths
        self.own_trades = own_trades
        self.market_trades = market_trades
        self.position = position
        self.observations = observations
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    
class ProsperityEncoder(JSONEncoder):

        def default(self, o):
            return o.__dict__


def main():

    from oldtrader import Trader
    
    timestamp = 0

    listings = {
	AMETHYST: Listing(
		symbol=AMETHYST, 
		product=AMETHYST, 
		denomination= SEASHELLS
	    ),
	STARFRUIT: Listing(
		symbol=STARFRUIT, 
		product=STARFRUIT, 
		denomination= SEASHELLS
	    ),
    }

    market_trades = {}

    simplified_trades = {
            AMETHYST: {},
            STARFRUIT: {}
    }

    positions = {
	AMETHYST: 0,
	STARFRUIT: 0
    }

    order_depths = {}

    observations = {}

    state = TradingState("SAMPLE", timestamp, listings, order_depths, simplified_trades, market_trades, positions, observations)

    trader1 = Trader()

    amethyst_pnls = []
    starfruit_pnls = []

    # Load the historical data CSV file
    historical_data = pd.read_csv('historical_data.csv', sep=";")

    # Group data by timestamp
    grouped_data = historical_data.groupby(['timestamp'])

    with open('additional.csv', 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'starfruit_positions', 'amethyst_positions', 'starfruit_pnl', 'amethyst_pnl']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write headers to the file
        writer.writeheader()

        # Iterate through each timestamp group
        for timestampy, group_data in grouped_data:
            state.timestamp = timestampy[0]
            
            # Filter data for Amethysts and Starfruit
            am_data = group_data[group_data['product'] == 'AMETHYSTS'].reset_index(drop=True)
            st_data = group_data[group_data['product'] == 'STARFRUIT'].reset_index(drop=True)
            
            # Extract values for Amethysts and starfruit
            am_ap1 = am_data.at[0, 'ask_price_1']
            am_av1 = am_data.at[0, 'ask_volume_1']
            am_ap2 = am_data.at[0, 'ask_price_2']
            am_av2 = am_data.at[0, 'ask_volume_2']
            am_ap3 = am_data.at[0, 'ask_price_3']
            am_av3 = am_data.at[0, 'ask_volume_3']

            am_bp1 = am_data.at[0, 'bid_price_1']
            am_bv1 = am_data.at[0, 'bid_volume_1']
            am_bp2 = am_data.at[0, 'bid_price_2']
            am_bv2 = am_data.at[0, 'bid_volume_2']
            am_bp3 = am_data.at[0, 'bid_price_3']
            am_bv3 = am_data.at[0, 'bid_volume_3']
            
            st_ap1 = st_data.at[0, 'ask_price_1']
            st_av1 = st_data.at[0, 'ask_volume_1']
            st_ap2 = st_data.at[0, 'ask_price_2']
            st_av2 = st_data.at[0, 'ask_volume_2']
            st_ap3 = st_data.at[0, 'ask_price_3']
            st_av3 = st_data.at[0, 'ask_volume_3']

            st_bp1 = st_data.at[0, 'bid_price_1']
            st_bv1 = st_data.at[0, 'bid_volume_1']
            st_bp2 = st_data.at[0, 'bid_price_2']
            st_bv2 = st_data.at[0, 'bid_volume_2']
            st_bp3 = st_data.at[0, 'bid_price_3']
            st_bv3 = st_data.at[0, 'bid_volume_3']

            # Create dictionaries for buy and sell orders
            am_buy_orders = {am_bp1: am_bv1, am_bp2: am_bv2, am_bp3: am_bv3}
            am_sell_orders = {am_ap1: -am_av1, am_ap2: -am_av2, am_ap3: -am_av3}

            st_buy_orders = {st_bp1: st_bv1, st_bp2: st_bv2, st_bp3: st_bv3}
            st_sell_orders = {st_ap1: -st_av1, st_ap2: -st_av2, st_ap3: -st_av3}

            am_buy_orders = {price: quantity for price, quantity in am_buy_orders.items() if pd.notna(price) and pd.notna(quantity)}
            am_sell_orders = {price: quantity for price, quantity in am_sell_orders.items() if pd.notna(price) and pd.notna(quantity)}
            
            st_buy_orders = {price: quantity for price, quantity in st_buy_orders.items() if pd.notna(price) and pd.notna(quantity)}
            st_sell_orders = {price: quantity for price, quantity in st_sell_orders.items() if pd.notna(price) and pd.notna(quantity)}

            # Create instances of OrderDepth
            order_depth = {}

            order_depth[AMETHYST] = OrderDepth()
            order_depth[AMETHYST].buy_orders = am_buy_orders
            order_depth[AMETHYST].sell_orders = am_sell_orders

            order_depth[STARFRUIT] = OrderDepth()
            order_depth[STARFRUIT].buy_orders = st_buy_orders
            order_depth[STARFRUIT].sell_orders = st_sell_orders

            state.order_depths = order_depth

            result, gaf1, gaf2 = trader1.run(state)

            am_ap2 = np.nan_to_num(am_ap2)
            am_av2 = np.nan_to_num(am_av2)
            am_bp2 = np.nan_to_num(am_bp2)
            am_bv2 = np.nan_to_num(am_bv2)
            am_ap3 = np.nan_to_num(am_ap3)
            am_av3 = np.nan_to_num(am_av3)
            am_bp3 = np.nan_to_num(am_bp3)
            am_bv3 = np.nan_to_num(am_bv3)

            st_ap2 = np.nan_to_num(st_ap2)
            st_av2 = np.nan_to_num(st_av2)
            st_bp2 = np.nan_to_num(st_bp2)
            st_bv2 = np.nan_to_num(st_bv2)
            st_ap3 = np.nan_to_num(st_ap3)
            st_av3 = np.nan_to_num(st_av3)
            st_bp3 = np.nan_to_num(st_bp3)
            st_bv3 = np.nan_to_num(st_bv3)

            amethyst_pnl = 0
            starfruit_pnl = 0
            am_amount_tally = 0
            st_amount_tally = 0

            amethyst_pnl += sum(trade * -amount for trade, amount in simplified_trades[AMETHYST].items())
            am_amount_tally = sum(amount for amount in simplified_trades[AMETHYST].values())

            if am_amount_tally > 0:
                best_bid = am_bp1
                amethyst_pnl += am_amount_tally * best_bid
            else:
                best_ask = am_ap1
                amethyst_pnl += am_amount_tally * best_ask

            starfruit_pnl += sum(trade * -amount for trade, amount in simplified_trades[STARFRUIT].items())
            st_amount_tally = sum(amount for amount in simplified_trades[STARFRUIT].values())

            if st_amount_tally > 0:
                best_bid = st_bp1
                starfruit_pnl += st_amount_tally * best_bid
            else:
                best_ask = st_ap1
                starfruit_pnl += st_amount_tally * best_ask
            
            starfruit_pnls.append(starfruit_pnl)
            amethyst_pnls.append(amethyst_pnl)

            if result[AMETHYST]:
                for orders in result[AMETHYST]:
                    quantity = int(orders.quantity)
                    price = int(orders.price)

                    state.position[AMETHYST] += quantity
                    if price in simplified_trades[AMETHYST].keys():
                        simplified_trades[AMETHYST][price] += quantity
                    else:
                        simplified_trades[AMETHYST][price] = quantity
                                
            if result[STARFRUIT]:
                for orders in result[STARFRUIT]:
                    quantity = int(orders.quantity)
                    price = int(orders.price)

                    state.position[STARFRUIT] += quantity
                    if price in simplified_trades[STARFRUIT].keys():
                        simplified_trades[STARFRUIT][price] += quantity
                    else:
                        simplified_trades[STARFRUIT][price] = quantity

            writer.writerow({
                'timestamp': timestampy[0],
                'starfruit_positions': state.position[STARFRUIT],
                'amethyst_positions': state.position[AMETHYST],
                'starfruit_pnl': starfruit_pnl,
                'amethyst_pnl': amethyst_pnl,
            })
        print(f"PNL for starfruit {starfruit_pnl}")
        print(f"Simplified trades {simplified_trades}")
    
    
if __name__ == "__main__":
    main()