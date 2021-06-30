# What does the exchange server do?
# Opening and closing of market
# Handles the orders
# Calculate Team metrics (daemon thread?)
# Match filled orders (daemon thread?)
# Detect error trade from unmatched trades every 30 seconds (daemon thread)

import time
from datetime import datetime, timedelta
from team import Team
from copy import deepcopy

class ExchangeServer:
    def __init__(self, exchange):
        self.exchange = exchange
    
    def open_market(self):
        print("Opening market")
        self.exchange.is_open = True
        self.exchange.start_time = datetime.now()

    def close_market(self):
        print("Closing market")
        self.exchange.is_open = False
        self.exchange.start_time = None
    
    def get_market_status(self):
        return self.exchange.is_open
    
    def get_start_time(self):
        return self.exchange.start_time
    
    def get_elapsed_time(self):
        if self.exchange.is_open:
            now = datetime.now()
            elapsed_time = now - self.exchange.start_time
            return str(elapsed_time)
        else:
            return None
    
    def get_last_trade_price(self):
        if len(self.exchange.trade_history) > 0:
            last_trade = self.exchange.trade_history[-1]
            return last_trade.price
        else:
            return None
    
    def add_team(self, team):
        if isinstance(team, Team):
            print(self.exchange)
            self.exchange.teams.append(team)

    def update_team_metrics(self, team):
        # Calculate pnl from trade_history
        pnl = 0.0
        matched_trades = 0
        unmatched_trades = 0
        error_trades = 0

        for trade in self.exchange.trade_history:
            # If team filled buy order
            if trade.buy_order and trade.buy_order.team_id == team.id:
                # Profit when trade price is less than buy price
                trade_price = trade.price
                trade_size = trade.size
                buy_price = trade.buy_order.price
                pnl += (buy_price - trade_price) * trade_size
                matched_trades += 1

            # If team filled sell order
            elif trade.sell_order and trade.sell_order.team_id == team.id:
                # Profit when trade price is more than sell price
                trade_price = trade.price
                trade_size = trade.size
                sell_price = trade.sell_order.price
                pnl += (trade_price - sell_price) * trade_size
                matched_trades += 1

        # Calculate trade counts from trade_history, unmatched_trade and error_trade
        for trade in self.exchange.unmatched_trade:
            if (
                (trade.buy_order and trade.buy_order.team_id == team.id) or
                (trade.sell_order and trade.sell_order.team_id == team.id)
            ):
                unmatched_trades += 1
        
        for trade in self.exchange.error_trade:
            if (
                (trade.buy_order and trade.buy_order.team_id == team.id) or
                (trade.sell_order and trade.sell_order.team_id == team.id)
            ):
                error_trades += 1

        # Update team metrics
        team.pnl = pnl
        team.matched_trades = matched_trades
        team.unmatched_trades = unmatched_trades
        team.error_trades = error_trades

    def update_all_team_metrics(self):
        for team in self.exchange.teams:
            self.update_team_metrics(team)
    
    def detect_error_trades(self, trade_factory):
        max_duration = timedelta(seconds=60)   # seconds before unmatched trade is classified as an error
        now = datetime.now()
        unmatched_trade = deepcopy(self.exchange.unmatched_trade)

        for trade in unmatched_trade:
            duration = now - trade.submitted_time

            # Turn unmatched trade to error trade
            if (duration > max_duration):
                # Remove trade from unmatched list
                index = unmatched_trade.index(trade)
                self.exchange.unmatched_trade.pop(index)

                # Update trade status
                trade_factory.change_status(trade, "ERROR")

                # Move trade to error list
                self.exchange.error_trade.append(trade)
    
    def detect_matched_trades(self, order, price, size, trade_factory):
        unmatched_trade = deepcopy(self.exchange.unmatched_trade)
        dir_type = order.dir
        team_id = order.team_id

        for trade in unmatched_trade:
            # Search for respective missing buy or sell trades, and checks whether the trades are from the same team
            if (
                ((dir_type == "BUY" and trade.buy_order is None and trade.sell_order.team_id != team_id) or
                (dir_type == "SELL" and trade.sell_order is None and trade.buy_order.team_id != team_id))
            ):
                # Price has to be a float and size has to be an integer
                if trade.price == price and trade.size == size:
                    # Remove trade from unmatched list
                    index = unmatched_trade.index(trade)
                    self.exchange.unmatched_trade.pop(index)

                    # Update trade status
                    trade_factory.match_trade(trade, order)
                    trade_factory.change_status(trade, "MATCHED")

                    # Move trade to matched list
                    self.exchange.trade_history.append(trade)
                    break
                
