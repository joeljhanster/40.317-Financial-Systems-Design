# What does the exchange client do?
# Requests
# Submit filled order
# Register Team
# Request Team Metrics
# Get Last Trade Price
from copy import deepcopy

class ExchangeClient:
    def __init__(self, exchange):
        self.exchange = exchange
    
    def submit_order(self, order, price, size, trade_factory):
        # Check if matches with any unmatched trade
        unmatched_trade = deepcopy(self.exchange.unmatched_trade)
        dir_type = order.dir
        team_id = order.team_id
        matched = False

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
                    matched = True
                    # TODO: If matched then update Order status to FILLED
                    break
                
        # Else append to unmatched trade
        if not matched:
            # Create new unmatched trade and append to the exchange list
            trade = trade_factory.add_unmatched_trade(order, price, size)
            self.exchange.unmatched_trade.append(trade)

            # TODO: If not matched then update Order status to SUBMITTED
    
    def get_team_metrics(self, team):
        return f"{team.id}_{team.name}_{team.pnl}_{team.matched_trades}_{team.unmatched_trades}_{team.error_trades}"

    def get_all_team_metrics(self):
        metrics = ""
        for team in self.exchange.teams:
            metrics += " "
            metrics += self.get_team_metrics(team)
        return metrics