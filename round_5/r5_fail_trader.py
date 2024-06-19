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
COCONUT = "COCONUT"
COCONUT_COUPON = "COCONUT_COUPON"

class Trader:

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
        self.gift_basket_pos_limit = 60
        self.ratio_matrix = np.array([[6 + 4 * 1.9656933442176188 + 3.6026796488094828],
                                [6 * 0.5088062931960909 + 4 + 1.8328332608080198],
                                [6 * 0.277611864773156 + 4 * 0.5456307844901649 + 1]])
        self.rosechoc = 1.8328332608080198
        self.giftchoc = 8.933633868419538
        self.strawchoc = 0.5088062931960909
        self.translation = 355

        self.coconut_alpha = 0.33
        self.coconut_ema = None

        self.coconut_position_limit = 300
        self.coupon_position_limit = 600
        self.coupon_mid_prices = {}
        self.coconut_mid_prices = {}
        self.vinnie_pos = 0
        self.valentina_pos = 0

    def amethyst_trades(self, state: TradingState):

        orders: List[Order] = []
        amesthyst_order_depth: OrderDepth = state.order_depths[AMETHYST]

        if AMETHYST not in state.position.keys():
            amethyst_pos = 0
        else:
            amethyst_pos = state.position[AMETHYST]

        if AMETHYST in state.market_trades.keys():
            amethyst_trades = state.market_trades[AMETHYST]
            for trade in amethyst_trades:
                if trade.timestamp == state.timestamp - 100:
                    if trade.seller == 'Vinnie':
                        max_sell = int(max(-trade.quantity, -self.position_limit - amethyst_pos))
                        orders.append(Order(AMETHYST, int(trade.price), max_sell))
                        amethyst_pos += max_sell
                    if trade.buyer == 'Vinnie':
                        max_buy = int(min(trade.quantity, self.position_limit - amethyst_pos))
                        orders.append(Order(AMETHYST, int(trade.price), max_buy))
                        amethyst_pos += max_buy
        
        return orders

    def starfruit_trades(self, state: TradingState):
        orders: List[Order] = []

        if STARFRUIT not in state.position.keys():
            starfruit_pos = 0
        else:
            starfruit_pos = state.position[STARFRUIT]

        starfruit_order_depth: OrderDepth = state.order_depths[STARFRUIT]

        if STARFRUIT in state.market_trades.keys():
            starfruit_trades = state.market_trades[STARFRUIT]
            for trade in starfruit_trades:
                if trade.timestamp == state.timestamp - 100:
                    if trade.seller == 'Valentina':
                        max_sell = int(max(-trade.quantity, -self.position_limit - starfruit_pos))
                        orders.append(Order(STARFRUIT, int(trade.price), max_sell))
                        self.valentina_pos -= trade.quantity
                        starfruit_pos += max_sell
                    if trade.buyer == 'Valentina':
                        max_buy = int(min(trade.quantity, self.position_limit - starfruit_pos))
                        orders.append(Order(STARFRUIT, int(trade.price), max_buy))
                        self.valentina_pos += trade.quantity
                        starfruit_pos += max_buy

        print(self.valentina_pos)
        return orders
    
    def roses_trades(self, state: TradingState):

        orders: List[Order] = []
        if ROSES not in state.position.keys():
            roses_pos = 0
        else:
            roses_pos = state.position[ROSES]

        roses_order_depth: OrderDepth = state.order_depths[ROSES]

        roses_bid, roses_bid_vol = list(roses_order_depth.buy_orders.items())[0]
        roses_ask, roses_ask_vol = list(roses_order_depth.sell_orders.items())[0]

        roses_mid = (roses_ask + roses_bid) / 2

        sell = math.ceil(roses_mid) + 1
        buy = math.floor(roses_mid) - 1

        max_sell = int(-self.roses_pos_limit - roses_pos)
        max_buy = int(self.roses_pos_limit - roses_pos)

        if ROSES in state.market_trades.keys():
            roses_trades = state.market_trades[ROSES]
            for trade in roses_trades:
                if trade.timestamp >= state.timestamp - 1000:
                    if (trade.buyer == 'Vladimir' and trade.seller == 'Remy'):
                        max_buy = (int(min(trade.quantity, self.roses_pos_limit - roses_pos)))
                        orders.append(Order(ROSES, int(trade.price),  self.roses_pos_limit - roses_pos))
                    if (trade.seller == 'Vladimir' and trade.buyer == 'Remy'):
                        max_sell = (int(max(-trade.quantity, -self.roses_pos_limit - roses_pos)))
                        orders.append(Order(ROSES, int(trade.price), -self.roses_pos_limit - roses_pos))

        return orders

    def coconut_counpon_trades(self, state: TradingState):
        coupon_orders: List[Order] = []

        if COCONUT_COUPON not in state.position.keys():
            coupon_pos = 0
        else:
            coupon_pos = state.position[COCONUT_COUPON]

        coupon_order_depth: OrderDepth = state.order_depths[COCONUT_COUPON]

        if COCONUT_COUPON in state.market_trades.keys():
            coupon_trades = state.market_trades[COCONUT_COUPON]
            print(coupon_trades)
            for trade in coupon_trades:
                if trade.timestamp <= state.timestamp - 400:
                    if (trade.buyer == 'Ruby'):
                        max_buy = int(min(trade.quantity, self.coupon_position_limit - coupon_pos))
                        coupon_orders.append(Order(COCONUT_COUPON, int(trade.price), max_buy))
                    if (trade.seller == 'Ruby'):
                        max_sell = int(max(-trade.quantity, -self.coupon_position_limit - coupon_pos))
                        coupon_orders.append(Order(COCONUT_COUPON, int(trade.price), max_sell))

                    if trade.seller == 'Vinnie':
                        self.vinnie_pos -= trade.quantity
                    if trade.buyer == 'Vinnie':
                        self.vinnie_pos += trade.quantity
        
        print(self.vinnie_pos)
        return coupon_orders

    def coconut_trades(self, state: TradingState):
        orders: List[Order] = []

        if COCONUT not in state.position.keys():
            coconut_pos = 0
        else:
            coconut_pos = state.position[COCONUT]

        coconut_order_depth: OrderDepth = state.order_depths[COCONUT]

        coconut_bid, coconut_bid_vol = list(coconut_order_depth.buy_orders.items())[0]
        coconut_ask, coconut_ask_vol = list(coconut_order_depth.sell_orders.items())[0]

        coconut_mid = (coconut_bid + coconut_ask) / 2

        max_buy = int(self.coconut_position_limit - coconut_pos)
        max_sell = int(-self.coconut_position_limit - coconut_pos)


        orders.append(Order(COCONUT, math.floor(coconut_mid) - 1, max_buy))
        orders.append(Order(COCONUT, math.ceil(coconut_mid) + 1, max_sell))


        return orders

    def straw_trades(self, state: TradingState):
        orders: List[Order] = []

        if STRAWBERRIES not in state.position.keys():
            strawberry_pos = 0
        else:
            strawberry_pos = state.position[STRAWBERRIES]

        straw_orders: OrderDepth = state.order_depths[STRAWBERRIES]

        straw_bids, straw_bids_vol = list(straw_orders.buy_orders.items())[0]
        straw_asks, straw_asks_vol = list(straw_orders.sell_orders.items())[0]

        if STRAWBERRIES in state.market_trades.keys():
            straw_trades = state.market_trades[STRAWBERRIES]
            for trade in straw_trades:
                if trade.timestamp <= state.timestamp - 1000:
                    if (trade.buyer == 'Remy' and trade.seller == 'Vladimir'):
                        max_buy = int(min(-straw_asks_vol, self.strawberry_pos_limit - strawberry_pos))
                        orders.append(Order(STRAWBERRIES, straw_asks, max_buy))
                    if (trade.seller == 'Remy' and trade.buyer == 'Vladimir'):
                        max_sell = int(max(-straw_bids_vol, -self.strawberry_pos_limit - strawberry_pos))
                        orders.append(Order(STRAWBERRIES, straw_bids, max_sell))
        
        print(strawberry_pos)
        return orders

    def run(self, state: TradingState):
        result = {}
        conversions = 0
        trader_data = ""

        straw_orders = self.roses_trades(state)
        result[ROSES] = straw_orders

        print(state.position)

        return result, conversions, trader_data