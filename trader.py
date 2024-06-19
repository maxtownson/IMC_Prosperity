from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List, Tuple
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
STRIKE = 10000
RF = -0.052855941708912724
VOL = 0.24086532541788852
EXPIRY = 250/365


class Trader:
    """
    A class representing a trading agent that performs automated trading strategies
    across various financial instruments.

    Methods:
        __init__():
            Initializes a Trader object with default parameter values.

        norm_cdf(x: float) -> float:
            Computes the cumulative distribution function (CDF) of the standard normal distribution.

        black_scholes_call(spot_price: float) -> float:
            Calculates the Black-Scholes call option price for a given spot price.

        calculate_starfruit_ema(mid_price: float):
            Updates the Exponential Moving Average (EMA) of mid_price for STARFRUIT.

        generate_starfruit_orders(state: TradingState) -> List[Order]:
            Generates trading orders for STARFRUIT symbols.

        generate_amethyst_orders(state: TradingState) -> List[Order]:
            Generates trading orders for AMETHYSTS symbols.

        generate_orchid_orders(state: TradingState) -> Tuple[List[Order], int]:
            Generates trading orders for ORCHID symbols.

        generate_coconut_coupon_orders(state: TradingState) -> List[Order]:
            Generates trading orders for C COCONUT_COUPON symbols.

        round_3_trades(state: TradingState) -> Tuple[List[Order], List[Order]]:
            Generates trading orders for STRAWBERRIES and GIFT_BASKET symbols.

        run(state: TradingState) -> Tuple[Dict[str, List[Order]], int, str]:
            Executes the complete trading strategy for all symbols and returns trading orders, conversions, and trader data.
    """

    def __init__(self):
        """
        Initialize the Trader object with default parameters.
        """
        self.alpha = 0.33
        self.starfruit_ema = None
        self.star_and_am_position_limit = 20
        self.amethyst_fair_price = 10000
        self.am_market_deviation = 4
        self.orchid_position_limit = 100

        self.chocolate_pos_limit = 250
        self.strawberry_pos_limit = 350
        self.roses_pos_limit = 60
        self.gift_basket_pos_limit = 60
        self.r3_ratio_matrix = np.array([[6 + 4 * 1.9656933442176188 + 3.6026796488094828],
                                [6 * 0.5088062931960909 + 4 + 1.8328332608080198],
                                [6 * 0.277611864773156 + 4 * 0.5456307844901649 + 1]])
        self.translation = 355

        self.coconut_position_limit = 300
        self.coupon_position_limit = 600
        self.coupon_mid_prices = {}
        self.coconut_mid_prices = {}

    
    def norm_cdf(self, x: float) -> float:
        """Calculate the cumulative distribution function (CDF) of the standard normal distribution.

        Args:
            x (float): The value for which the CDF is calculated.

        Returns:
            float: The CDF value for the standard normal distribution at x.
        """
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))


    def black_scholes_call(self, spot_price: float) -> float:
        """Calculate the Black-Scholes price for a call option.

        Args:
            spot_price (float): The current price of the underlying asset.

        Returns:
            float: The Black-Scholes call option price.
        """
        d1 = (np.log(spot_price / STRIKE) + (RF + 0.5 * VOL**2) * EXPIRY) / (VOL * np.sqrt(EXPIRY))
        d2 = d1 - VOL * np.sqrt(EXPIRY)
        call_price = spot_price * self.norm_cdf(d1) - STRIKE * np.exp(-RF * EXPIRY) * self.norm_cdf(d2)
        return call_price


    def calculate_starfruit_ema(self, mid_price: float) -> None:
        """Calculate and update the Exponential Moving Average (EMA) for STARFRUIT.

        This method updates the EMA for the STARFRUIT symbol based on the provided
        mid price. If the EMA has not been initialized, it sets the EMA to the
        current mid price.

        Args:
            mid_price (float): The mid price used to calculate the EMA.
        """
        if self.starfruit_ema is None:
            # Initialize EMA with the current mid price if not already initialized
            self.starfruit_ema = mid_price
        else:
            # Update the EMA using the formula: EMA = alpha * mid_price + (1 - alpha) * EMA
            self.starfruit_ema = self.alpha * mid_price + (1 - self.alpha) * self.starfruit_ema


    def generate_starfruit_orders(self, state: TradingState) -> List[Order]:
        """Generate trading orders for the STARFRUIT symbol.

        This method calculates an EMA with the starfruit midprice, and market
        makes around this value.

        Args:
            state (TradingState): The current trading state containing market data and positions.

        Returns:
            List[Order]: A list of Order objects representing the trading orders for STARFRUIT.
        """
        orders: List[Order] = []

        # Retrieve current position in STARFRUIT, defaulting to 0 if not present
        current_position = state.position.get(STARFRUIT, 0)

        # Calculate the volume we can trade within the position limits
        max_buy_volume = self.star_and_am_position_limit - current_position
        max_sell_volume = -self.star_and_am_position_limit - current_position

        # Retrieve the order depth for STARFRUIT
        starfruit_order_depth: OrderDepth = state.order_depths[STARFRUIT]

        # Get the best bid and ask prices
        best_bid_price, _ = list(starfruit_order_depth.buy_orders.items())[0]
        best_ask_price, _ = list(starfruit_order_depth.sell_orders.items())[0]

        # Calculate the mid-price as a simple average of the best bid and ask prices
        mid_price = (best_ask_price + best_bid_price) / 2

        # Update the EMA with the latest mid-price
        self.calculate_starfruit_ema(mid_price)

        # Create bid and ask orders around the EMA
        profitable_bid_price = math.floor(self.starfruit_ema - 1)
        profitable_ask_price = math.ceil(self.starfruit_ema + 1)

        # Market make around the profitable bid and ask prices
        orders.append(Order(STARFRUIT, profitable_bid_price, max_buy_volume))
        orders.append(Order(STARFRUIT, profitable_ask_price, max_sell_volume))

        return orders


    def generate_amethyst_orders(self, state: TradingState) -> List[Order]:
        """Generate trading orders for the AMETHYST symbol.

        This method calculates the optimal bid and ask prices for AMETHYST
        based on the current market state and the trader's position, and creates
        corresponding orders.

        Args:
            state (TradingState): The current trading state containing market data and positions.

        Returns:
            List[Order]: A list of Order objects representing the trading orders for AMETHYST.
        """
        orders: List[Order] = []
        amethyst_order_depth: OrderDepth = state.order_depths[AMETHYST]

        # Retrieve current position in AMETHYST, defaulting to 0 if not present
        current_position = state.position.get(AMETHYST, 0)

        # Initialize running tallies for positive and negative positions
        positive_tally = max(0, current_position)
        negative_tally = min(0, current_position)

        # Market taking takes precedence for maximal profit
        for price, volume in amethyst_order_depth.buy_orders.items():
            if price > self.amethyst_fair_price:
                if current_position - volume >= -self.star_and_am_position_limit:
                    orders.append(Order(AMETHYST, price, -volume))
                    current_position -= volume
                    negative_tally -= volume
                else:
                    if current_position > -self.star_and_am_position_limit:
                        max_volume = self.star_and_am_position_limit + current_position
                        orders.append(Order(AMETHYST, price, -max_volume))
                        current_position -= max_volume
                        negative_tally -= max_volume

        for price, volume in amethyst_order_depth.sell_orders.items():
            if price < self.amethyst_fair_price:
                if current_position + volume <= self.star_and_am_position_limit:
                    orders.append(Order(AMETHYST, price, volume))
                    current_position += volume
                    positive_tally += volume
                else:
                    if current_position < self.star_and_am_position_limit:
                        max_volume = self.star_and_am_position_limit - current_position
                        orders.append(Order(AMETHYST, price, max_volume))
                        current_position += max_volume
                        positive_tally += max_volume

        # Followed by market making
        max_bid_volume = min(self.star_and_am_position_limit - current_position, self.star_and_am_position_limit - positive_tally)
        max_ask_volume = max(-self.star_and_am_position_limit - current_position, -self.star_and_am_position_limit - negative_tally)

        bid_volume = min(self.star_and_am_position_limit, max_bid_volume)
        ask_volume = max(-self.star_and_am_position_limit, max_ask_volume)

        orders.append(Order(AMETHYST, self.amethyst_fair_price - self.am_market_deviation, bid_volume))
        orders.append(Order(AMETHYST, self.amethyst_fair_price + self.am_market_deviation, ask_volume))

        return orders


    def generate_orchid_orders(self, state: TradingState) -> Tuple[List[Order], int]:
        """Generate trading orders for the ORCHID symbol.

        This method focuses on creating arbitrage opportunities between the
        exchange and the southern islands, by considering the export tariffs,
        import tariffs, bid and ask prices.

        Args:
            state (TradingState): The current trading state containing market data, positions, and observations.

        Returns:
            Tuple[List[Order], int]: A tuple containing a list of Order objects representing the trading orders for ORCHID
            and the negative of the current ORCHID position.
        """
        orders: List[Order] = []

        # Retrieve current position in ORCHID, defaulting to 0 if not present
        current_position = state.position.get(ORCHIDS, 0)
        
        temporary_position = 0

        # Retrieve the order depth and observations for ORCHIDS
        orchid_order_depth: OrderDepth = state.order_depths[ORCHIDS]
        orchid_obs = state.observations.conversionObservations[ORCHIDS]

        # Generate orders by comparing bids with observation-based price thresholds (market taking)
        for bid_price, bid_volume in orchid_order_depth.buy_orders.items():
            target_price = orchid_obs.askPrice + orchid_obs.importTariff + orchid_obs.transportFees
            if bid_price > target_price:
                orders.append(Order(ORCHIDS, bid_price, -bid_volume))
                temporary_position -= bid_volume
                break

        # Calculate the volume and price for the ask order (market making)
        max_ask_volume = max(-100, -self.orchid_position_limit - temporary_position)
        profitable_ask_price = math.ceil(orchid_obs.askPrice + orchid_obs.importTariff + orchid_obs.transportFees + 1.2)

        orders.append(Order(ORCHIDS, profitable_ask_price, max_ask_volume))

        # -current_position as the conversion to immediate convert (arbitrage)
        return orders, -current_position


    def round_3_trades(self, state: TradingState) -> Tuple[List[Order], List[Order]]:
        """Generate trading orders for round 3 trades involving multiple symbols.

        This method generates trading orders for STRAWBERRIES and GIFT_BASKET symbols
        based on the current trading state. It includes logic for determining profitable bids and asks,
        and it manages position limits for each symbol.

        Args:
            state (TradingState): The current trading state containing market data, positions, and order depths.

        Returns:
            Tuple[List[Order], List[Order], List[Order], List[Order]]: A tuple containing lists of Order objects
            for CHOCOLATE, STRAWBERRIES, ROSES, and GIFT_BASKET respectively.
        """

        strawberry_orders: List[Order] = []
        gift_basket_orders: List[Order] = []

        strawberry_position = state.position.get(STRAWBERRIES, 0)
        gift_basket_position = state.position.get(GIFT_BASKET, 0)

        strawberry_order_depth: OrderDepth = state.order_depths[STRAWBERRIES]
        chocolate_order_depth: OrderDepth = state.order_depths[CHOCOLATE]
        roses_order_depth: OrderDepth = state.order_depths[ROSES]
        gift_order_depth: OrderDepth = state.order_depths[GIFT_BASKET]

        straw_bid = list(strawberry_order_depth.buy_orders.items())[0][0]
        straw_ask = list(strawberry_order_depth.sell_orders.items())[0][0]
        choc_bid = list(chocolate_order_depth.buy_orders.items())[0][0]
        choc_ask = list(chocolate_order_depth.sell_orders.items())[0][0]
        roses_bid = list(roses_order_depth.buy_orders.items())[0][0]
        roses_ask = list(roses_order_depth.sell_orders.items())[0][0]
        gift_bid = list(gift_order_depth.buy_orders.items())[0][0]
        gift_ask = list(gift_order_depth.sell_orders.items())[0][0]

        temp_straw_pos = strawberry_position
        temp_gift_pos = gift_basket_position

        gift_selling_pos = 0
        gift_buying_pos = 0
        straw_selling_pos = 0
        straw_buying_pos = 0

        # Determine a profitable strawberry ask value w.r.t the the components (market making)
        profitable_straw_ask = math.ceil((gift_ask - self.translation) / self.r3_ratio_matrix[0][0]) + 20
        straw_max_ask_vol = max((-self.strawberry_pos_limit - temp_straw_pos - straw_selling_pos), -self.strawberry_pos_limit)
        if straw_max_ask_vol != 0:
            strawberry_orders.append(Order(STRAWBERRIES, profitable_straw_ask, straw_max_ask_vol))

        # Determine a profitable strawberry bid value w.r.t the the components (market making)
        profitable_straw_bid = math.floor((gift_bid - self.translation) / self.r3_ratio_matrix[0][0]) - 20
        straw_max_bid_vol = min((self.strawberry_pos_limit - temp_straw_pos - straw_buying_pos), self.strawberry_pos_limit)
        if straw_max_bid_vol != 0:
            strawberry_orders.append(Order(STRAWBERRIES, profitable_straw_bid, straw_max_bid_vol))
        
        # Find profitable gift basket ask value w.r.t the the components (market taking)
        for bid, vol in list(gift_order_depth.buy_orders.items()):
            if bid - 25 > (6 * straw_ask + 4 * choc_ask + roses_ask + self.translation) and temp_gift_pos > -60:
                gift_max_ask_vol = abs(-self.gift_basket_pos_limit - temp_gift_pos)
                min_gift_pos = min(abs(vol), gift_max_ask_vol)
                if min_gift_pos != 0:
                    gift_basket_orders.append(Order(GIFT_BASKET, bid, -min_gift_pos))
                    gift_selling_pos -= min_gift_pos
                    temp_gift_pos -= min_gift_pos

        # Find profitable gift basket bid value w.r.t the the components (market taking)
        for ask, vol in list(gift_order_depth.sell_orders.items()):
            if ask + 55 < 6 * straw_bid + 4 * choc_bid + roses_bid + self.translation and temp_gift_pos < 58:
                gift_max_bid_vol = abs(self.gift_basket_pos_limit - temp_gift_pos)
                min_gift_pos = min(abs(vol), gift_max_bid_vol)
                if min_gift_pos != 0:
                    gift_basket_orders.append(Order(GIFT_BASKET, ask, min_gift_pos))
                    gift_buying_pos += min_gift_pos
                    temp_gift_pos += min_gift_pos

        return strawberry_orders, gift_basket_orders


    def generate_coconut_coupon_orders(self, state: TradingState) -> List[Order]:
        """
        Generate trading orders for the COCONUT and COCONUT_COUPON symbols.

        This method finds the black_scholes option price estimation of the coupon
        with respect to the COCONUT price. If these orders are not sufficient, then
        trade against the instantaneous delta rate.

        Args:
            state (TradingState): The current trading state containing market data, positions, and observations.

        Returns:
            Tuple[List[Order], List[Order]]: A tuple containing two lists of Order objects, 
                                         one for COCONUT and one for COCONUT_COUPON.
        """
        coupon_scholes_orders: List[Order] = []
        coupon_delta_orders: List[Order] = []

        # Retrieve current positions, defaulting to 0 if not present
        coupon_position = state.position.get(COCONUT_COUPON, 0)

        # Retrieve the order depths for COCONUT and COCONUT_COUPON
        coconut_order_depth: OrderDepth = state.order_depths[COCONUT]
        coupon_order_depth: OrderDepth = state.order_depths[COCONUT_COUPON]

        # Get buy and sell orders
        coconut_asks = list(coconut_order_depth.sell_orders.items())
        coconut_bids = list(coconut_order_depth.buy_orders.items())
        coupon_asks = list(coupon_order_depth.sell_orders.items())
        coupon_bids = list(coupon_order_depth.buy_orders.items())

        if coupon_asks and coupon_bids and coconut_asks and coconut_bids:
            best_coconut_ask = coconut_asks[0][0]
            best_coconut_bid = coconut_bids[0][0]
            best_coupon_ask = coupon_asks[0][0]
            best_coupon_bid = coupon_bids[0][0]

            if best_coconut_ask and best_coconut_bid and best_coupon_ask and best_coupon_bid:

                coupon_mid = (best_coupon_ask + best_coupon_bid) / 2
                coconut_mid = (best_coconut_ask + best_coconut_bid) / 2
                self.coupon_mid_prices[state.timestamp] = coupon_mid
                self.coconut_mid_prices[state.timestamp] = coconut_mid
                black_scholes_est = self.black_scholes_call(coconut_mid)

                sell_limit = -self.coupon_position_limit - coupon_position
                buy_limit = self.coupon_position_limit - coupon_position

                # Generate Black-Scholes based orders
                for bid_price, bid_volume in coupon_bids:
                    if black_scholes_est + 6 < bid_price:
                        max_sell_volume = max(sell_limit, -bid_volume)
                        coupon_scholes_orders.append(Order(COCONUT_COUPON, bid_price, max_sell_volume))
                        sell_limit -= max_sell_volume
                                
                for ask_price, ask_volume in coupon_asks:
                    if black_scholes_est - 6 > ask_price:
                        max_buy_volume = min(buy_limit, -ask_volume)
                        coupon_scholes_orders.append(Order(COCONUT_COUPON, ask_price, max_buy_volume))
                        buy_limit -= max_buy_volume
                
                profitable_ask_price = math.ceil(black_scholes_est + 10)
                coupon_scholes_orders.append(Order(COCONUT_COUPON, profitable_ask_price, sell_limit))
                
                profitable_bid_price = math.floor(black_scholes_est - 10)
                coupon_scholes_orders.append(Order(COCONUT_COUPON, profitable_bid_price, buy_limit))

            # Generated instantaneous delta-based orders
            previous_timestamp = state.timestamp - 5000
            if previous_timestamp in self.coupon_mid_prices:

                previous_coupon_mid_price = self.coupon_mid_prices[previous_timestamp]
                previous_coconut_mid_price = self.coconut_mid_prices[previous_timestamp]

                coupon_price_change = coupon_mid - previous_coupon_mid_price
                coconut_price_change = coconut_mid - previous_coconut_mid_price

                # Avoid zero division error
                if coconut_price_change != 0:
                    delta = coupon_price_change / coconut_price_change

                    # Basically, coupon is 2.5xing the value sensitivity of coconuts
                    if delta >= 2.5:

                        # if both moving up (revert the position) (sell for now)
                        if coupon_price_change > 0:
                            for bid_price, bid_volume in coupon_bids:
                                max_sell_volume = max(-self.coupon_position_limit - coupon_position, -bid_volume)
                                coupon_delta_orders.append(Order(COCONUT_COUPON, bid_price, max_sell_volume))
                                coupon_position += max_sell_volume
                            
                            max_sell_volume = -self.coupon_position_limit - coupon_position
                            coupon_delta_orders.append(Order(COCONUT_COUPON, best_coupon_bid, max_sell_volume))
                        
                        # If both moving down (revert the position) (buy for now)
                        if coupon_price_change < 0:
                            for ask_price, ask_volume in coupon_asks:
                                max_buy_volume = min(self.coupon_position_limit - coupon_position, -ask_volume)
                                coupon_delta_orders.append(Order(COCONUT_COUPON, ask_price, max_buy_volume))
                                coupon_position += max_buy_volume
                            
                            max_buy_volume = self.coupon_position_limit - coupon_position
                            coupon_delta_orders.append(Order(COCONUT_COUPON, best_coupon_bid, max_buy_volume))

                    # If coupon is 2.5x the value sensitivity of coconuts in the opp direction
                    if delta <= -2.5:
                        # If coupon going down, and coconut going up (buy)
                        if coupon_price_change < 0:
                            for ask_price, ask_volume in coupon_asks:
                                max_buy_volume = min(self.coupon_position_limit - coupon_position, -ask_volume)
                                coupon_delta_orders.append(Order(COCONUT_COUPON, ask_price, max_buy_volume))
                                coupon_position += max_buy_volume
                            
                            max_buy_volume = self.coupon_position_limit - coupon_position
                            coupon_delta_orders.append(Order(COCONUT_COUPON, best_coupon_bid, max_buy_volume))

                        # IF coupon going up, and coconut going down (sell)
                        if coupon_price_change > 0:
                            for bid_price, bid_volume in coupon_bids:
                                max_sell_volume = max(-self.coupon_position_limit - coupon_position, -bid_volume)
                                coupon_delta_orders.append(Order(COCONUT_COUPON, bid_price, max_sell_volume))
                                coupon_position += max_sell_volume
                            
                            max_sell_volume = -self.coupon_position_limit - coupon_position
                            coupon_delta_orders.append(Order(COCONUT_COUPON, best_coupon_bid, max_sell_volume))

        # Sufficient black scholes order takes precedence over instantaneous delta
        if len(coupon_scholes_orders) > 2:
            return coupon_scholes_orders
        else:
            return coupon_delta_orders
        

    def run(self, state: TradingState):
        """Execute the trading strategy for various symbols.

        This method generates trading orders for multiple symbols based on the current trading state and 
        consolidates the results into a dictionary. It also handles special cases such as conversions and 
        returns additional trader data.

        Args:
            state (TradingState): The current trading state containing market data, positions, and observations.

        Returns:
            Tuple[Dict[str, List[Order]], int, str]: A tuple containing:
                - A dictionary mapping symbols to their respective lists of Order objects.
                - The number of conversions performed.
                - Additional trader data as a string.
        """
        results = {}
        conversions = 0
        trader_data = ""

        # Generate orders for each symbol
        starfruit_orders = self.generate_starfruit_orders(state)
        amethyst_orders = self.generate_amethyst_orders(state)
        orchid_orders, conversions = self.generate_orchid_orders(state)
        strawberry_orders, gift_basket_orders = self.round_3_trades(state)
        coconut_coupon_orders = self.generate_coconut_and_coupon_orders(state)

        # Store orders for each symbol in the result dictionary
        results[STARFRUIT] = starfruit_orders
        results[AMETHYST] = amethyst_orders
        results[ORCHIDS] = orchid_orders
        results[STRAWBERRIES] = strawberry_orders
        results[GIFT_BASKET] = gift_basket_orders
        results[COCONUT_COUPON] = coconut_coupon_orders

        return results, conversions, trader_data
