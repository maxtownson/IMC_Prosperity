from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import numpy as np
import math

AMETHYST = "AMETHYSTS"
STARFRUIT = "STARFRUIT"
ORCHIDS = "ORCHIDS"
GIFT_BASKET = "GIFT_BASKET"
CHOCOLATE = "CHOCOLATE"
STRAWBERRIES = "STRAWBERRIES"
ROSES = "ROSES"


class Trader:
    """A class representing a trading agent."""


    def __init__(self):
        """Initialize the Trader object with default parameters."""
        self.alpha = 0.33
        self.starfruit_ema = None
        self.position_limit = 20
        self.amethyst_fair_price = 10000
        self.am_market_deviation = 4
        self.orchid_position_limit = 100

        self.chocolate_pos_limit = 250
        self.strawberry_pos_limit = 350
        self.roses_pos_limit = 60
        self.gift_basket_pos_limit = 58
        self.ratio_matrix = np.array([[6 + 4 * 1.9656933442176188 + 3.6026796488094828],
                                [6 * 0.5088062931960909 + 4 + 1.8328332608080198],
                                [6 * 0.277611864773156 + 4 * 0.5456307844901649 + 1]])
        self.rosechoc = 1.8328332608080198
        self.giftchoc = 8.933633868419538
        self.strawchoc = 0.5088062931960909
        self.translation = 355


    def calculate_star_ema(self, mid_price):
        """Calculate Exponential Moving Average (EMA) of mid_price.

        Args:
            mid_price (float): The mid price to calculate EMA for.
        """
        if self.starfruit_ema is None:
            self.starfruit_ema = mid_price
        self.starfruit_ema = mid_price * self.alpha + (1 - self.alpha) * self.starfruit_ema


    def starfruit_trades(self, state: TradingState):
        """Generate trading orders for STARFRUIT symbol.

        Args:
            state (TradingState): The current trading state.

        Returns:
            List[Order]: A list of Order objects representing the trading orders for STARFRUIT.
        """
        orders: List[Order] = []
        if STARFRUIT not in state.position.keys():
            starfruit_pos = 0
        else:
            starfruit_pos = state.position[STARFRUIT]

        star_bid_volume = self.position_limit - starfruit_pos
        star_ask_volume = - self.position_limit - starfruit_pos

        starfruit_order_depth: OrderDepth = state.order_depths[STARFRUIT]

        best_star_bid, _ = list(starfruit_order_depth.buy_orders.items())[0]
        best_star_ask, _ = list(starfruit_order_depth.sell_orders.items())[0]
        
        bid_ask_spread = (best_star_ask + best_star_bid) / 2

        self.calculate_star_ema(bid_ask_spread)

        return orders


    def amethyst_trades(self, state: TradingState):
        """Generate trading orders for AMETHYSTS symbol.

        Args:
            state (TradingState): The current trading state.

        Returns:
            List[Order]: A list of Order objects representing the trading orders for AMETHYSTS.
        """
        orders: List[Order] = []
        amesthyst_order_depth: OrderDepth = state.order_depths[AMETHYST]

        if AMETHYST not in state.position.keys():
            amethyst_temp_position = 0
        else:
            amethyst_temp_position = state.position[AMETHYST]

        running_pos_tally = max(0, amethyst_temp_position)
        running_neg_tally = min(0, amethyst_temp_position)

        # Market taking takes precedence for maximal profit
        for price, amount in amesthyst_order_depth.buy_orders.items():
            if price > self.amethyst_fair_price:
                if -self.position_limit <= amethyst_temp_position - amount:
                    orders.append(Order(AMETHYST, price, -amount))
                    amethyst_temp_position -= amount
                    running_neg_tally -= amount

                else:
                    if amethyst_temp_position != -self.position_limit:
                        max_amount = self.position_limit + amethyst_temp_position
                        orders.append(Order(AMETHYST, price, -max_amount))
                        amethyst_temp_position -= max_amount
                        running_neg_tally -= max_amount

        for price, amount in amesthyst_order_depth.sell_orders.items():
            if price < self.amethyst_fair_price:
                if amethyst_temp_position - amount <= self.position_limit:
                    orders.append(Order(AMETHYST, price, -amount))
                    amethyst_temp_position -= amount
                    running_pos_tally -= amount

                else:
                    if amethyst_temp_position != self.position_limit:
                        max_amount = -self.position_limit + amethyst_temp_position
                        orders.append(Order(AMETHYST, price, -max_amount))
                        amethyst_temp_position -= max_amount
                        running_pos_tally -= max_amount
        
        return orders

    def run(self, state: TradingState):
        result = {}
        conversions = 0
        trader_data = ""

        s_orders = self.starfruit_trades(state)
        a_orders = self.amethyst_trades(state)
        #o_orders, conversions = self.orchid_trades(state)
        
        result[AMETHYST] = a_orders
        result[STARFRUIT] = s_orders

        return result, conversions, trader_data