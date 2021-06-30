# The server code for 40.317 Homework 2.
import zmq
import sys
import re
from decimal import Decimal, DecimalException

from exchange import Exchange
from exchange_server_class import ExchangeServer
from exchange_client_class import ExchangeClient
from player_factory import PlayerFactory
from team_factory import TeamFactory
from order_factory import OrderFactory
from trade_factory import TradeFactory

# To run the server at a non-default port, the user provides the alternate port
# number on the command line.
host = "127.0.0.1"  # Our 
port = "5890"   # Our default port
if len(sys.argv) == 3:
    host = sys.argv[1]  # 127.0.0.1
    port = sys.argv[2]  # e.g. 5678
    print("Overriding default port to", port)
    _ = int(port)   # What does this do?

context = zmq.Context()
# Using "zmq.PAIR" means there is exactly one server for each client
# and vice-versa.  For this application, zmq.PAIR is more appropriate
# than zmq.REQ + zmq.REP (make sure you understand why!).
socket = context.socket(zmq.REP)
socket.bind(f"tcp://{host}:{port}")
print("I am the server, now alive and listening on port", port)

# Additional Functions
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_positive_number(s):
    if is_number(s):
        return Decimal(s) >= 0
    else:
        return False

def is_positive_integer(s):
    if is_positive_number(s):
        return s.isnumeric()
    else:
        return False

# Instantiate the Exchange
exchange = Exchange()
exchange_server = ExchangeServer(exchange)
exchange_client = ExchangeClient(exchange)

# Instantiate the Factory
player_factory = PlayerFactory()
team_factory = TeamFactory()
order_factory = OrderFactory()
trade_factory = TradeFactory()

while True:
    message = socket.recv()
    decoded = message.decode("utf-8")
    tokens = decoded.split()
    if len(tokens) == 0:
        continue
    cmd = tokens[0]
    if cmd == "shutdown_server":
        socket.send_string("[OK] Server shutting down")
        sys.exit(0)
    else:
        options = tokens[1:]
        print(f"Received: {cmd} {options}")

        # The response is a function of cmd and options:
        response = ""

        ### INSERT COMMANDS HERE ###
        ### TEAM COMMANDS ###
        if cmd == "add_player":
            if len(options) == 0:
                response = "[ERROR] Please provide player name!"
            elif len(options) != 2:
                response = f"[ERROR] Requires 2 args: family_name given_name."
                
            elif (options[0].isalpha() and options[1].isalpha()) is not True:
                response = f"[ERROR] Only alphabetical characters allowed"
            else:
                family_name = options[0].replace("_", " ")
                given_name = options[1].replace("_", " ")

                # Instantiate new Player object, return PlayerID as response
                player = player_factory.add_player(family_name, given_name)
                response = f"[OK] Added Player Id {player.id}"  # player.id needs to be the last argument

        elif cmd == "add_team":
            if len(options) == 0:
                response = "[ERROR] Please provide team name and player ids!"
            elif len(options) == 1:
                team_name = options[0].replace("_", " ")
                response = f"[ERROR] Please provide player ids for Team {team_name}!"
            else:
                team_name = options[0].replace("_", " ")
                player_ids = options[1:]
                players = []
                is_error = False

                # Add each player id to the Team object
                for player_id in player_ids:
                    # Check if id is valid before proceeding
                    # Id must be an integer
                    if not player_id.isdigit():
                        response = f"[ERROR] Received non-integer player id: {player_id}"
                        is_error = True
                        break
                    else:
                        # Check if player is registered, if not error message "Player {id} is not registered"
                        player = player_factory.get_player(int(player_id))
                        if player is None:
                            response = f"[ERROR] Player {player_id} is not registered"
                            is_error = True
                            break
                        players.append(player)
                
                if not is_error:
                    # Instantiate new Team object, return TeamID as response
                    team = team_factory.add_team(team_name, players)

                    # Instantiate Order objects and add to Team object
                    orders = order_factory.create_batch_orders(team.id, 8)
                    team_factory.add_orders(team.id, orders)
                    exchange_server.add_team(team)

                    response = f"[OK] Added Team Id {team.id}"  # team.id needs to be the last argument

        elif cmd == "get_team_live_orders":
            if len(options) == 0:
                response = "[ERROR] Please provide team id!"
            elif len(options) != 1:
                response = "[ERROR] Requires 1 arg: team_id"
            else:
                team_id = options[0]

                # Instantiate Order objects and add to Team object
                orders = team_factory.get_live_orders(team_id)
                if orders == None:
                    response = f"[ERROR] Team id {team_id} does not exist."
                elif len(orders) > 0:
                    # <order_id>_<size>_<price>_<type>_<status>
                    # e.g. 8_50_98.0_BUY_LIVE
                    formatted_orders = order_factory.format_orders(orders)
                    response = f"[OK] {formatted_orders.strip()}"
                else:
                    response = "[ERROR] Team currently has no live orders"

        # TODO
        elif cmd == "get_team_metrics":
            # <teamID>
            # return <PnL> <matchedTradeCount> <unmatchedTradeCount> <errorTradeCount>
            if len(options) == 0:
                response = "[ERROR] Please provide team id!"
            elif len(options) != 1:
                response = f"[ERROR] Requires 1 arg: team_id"
            else:
                team_id = options[0]
                team = team_factory.get_team(team_id)
                if team == None:
                    response = f"[ERROR] Team id {team_id} does not exist."
                else:
                    exchange_server.update_team_metrics(team)
                    metrics = exchange_client.get_team_metrics(team)
                    response = f"[OK] {metrics}"
                    # # TODO: Get PnL
                    # pnl = team.pnl
                    # # TODO: Get Trade Counts
                    # t_cnts = team_factory.get_team_trades_counts(team_id)
                    # fmt = ' '.join([str(x) for x in t_cnts])

                    # response = f"[OK] {pnl} {fmt}"

        # TODO
        elif cmd == "submit_and_match":
            # <idToFill>,<teamID>,<fillOrder.TradePrice>,<fillOrder.TradeSize>
            if len(options) != 4:
                response = "[ERROR] Requires 4 args: order_id team_id trade_price trade_size"
            elif (
                not is_positive_integer(options[0]) or
                not is_positive_integer(options[1]) or
                not is_positive_number(options[2]) or
                not is_positive_integer(options[3])
            ):
                response = "[ERROR] Values must be positive integers!"
            else:
                order_id = int(options[0])
                team_id = int(options[1])
                trade_price = float(options[2])
                trade_size = int(options[3])

                # Check if market is open
                market_status = exchange_server.get_market_status()
                if market_status:
                    # TODO: Trade size must be <= order size

                    # Check correct value
                    order = order_factory.get_order(order_id, team_id)
                    print(order)
                    if order:
                        exchange_client.submit_order(order, trade_price, trade_size, trade_factory)
                        response = f"[OK] Order ID {order_id} is successfully submitted!"
                    else:
                        response = f"[ERROR] Order ID {order_id} not found!"
                else:
                    response = f"[ERROR] Market is closed!"

        # TODO
        elif cmd == "cancel_live_order":
            # <idToCancel> <teamId>
            if len(options) != 2:
                response = f"[ERROR] Requires 2 arg: order_id team_id"
            else:
                raise NotImplementedError("hHAHAHAHAHAHAHAHAHA")
            pass


        ### TODO ADMIN COMMANDS ###
        elif cmd == "open_market":
            if len(options) != 0:
                response = f"[ERROR] Required no arguments, found {len(options)}"
            else:
                exchange_server.open_market()
                status = exchange_server.get_market_status()

                if status:
                    response = "[OK] Market opened"
                else:
                    response = "[ERROR] Failed to open market"

        elif cmd == "close_market":
            if len(options) != 0:
                response = f"[ERROR] Required no arguments, found {len(options)}"
            else:
                exchange_server.close_market()
                status = exchange_server.get_market_status()

                if not status:
                    response = "[OK] Market closed"
                else:
                    response = "[ERROR] Failed to close market"
        
        elif cmd == "get_elapsed_time":
            elapsed_time = exchange_server.get_elapsed_time()
            if elapsed_time:
                response = f"[OK] {elapsed_time}"
            else:
                response = f"[ERROR] Market is closed!"
        
        elif cmd == "get_start_time":
            response = exchange_server.get_start_time()
        
        elif cmd == "get_market_status":
            status = exchange_exchange.get_market_status()
            if status:
                response = "[OK] Market opened"
            else:
                response = "[OK] Market closed"
        
        elif cmd == "get_all_team_metrics":
            if len(options) != 0:
                response = f"[ERROR] Required no arguments, found {len(options)}"
            else:
                exchange_server.update_all_team_metrics()
                metrics = exchange_client.get_all_team_metrics()
                response = f"[OK] {metrics.strip()}"
        
        elif cmd == "get_last_trade_price":
            if len(options) != 0:
                response = f"[ERROR] Required no arguments, found {len(options)}"
            else:
                last_price = exchange_server.get_last_trade_price()
                if last_price:
                    response = f"[OK] {last_price}"
                else:
                    response = "[ERROR] Trade history is empty"

        socket.send_string(response)