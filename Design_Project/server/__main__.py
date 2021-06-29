# The server code for 40.317 Homework 2.
import zmq
import sys
import re

from exchange import Exchange
from player_factory import PlayerFactory
from team_factory import TeamFactory
from order_factory import OrderFactory

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

# Instantiate the Exchange
exchange = Exchange()
player_factory = PlayerFactory()
team_factory = TeamFactory()
order_factory = OrderFactory()

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
        if cmd == "add_player":
            if len(options) == 0:
                response = "[ERROR] Please provide player name!"
            elif len(options) != 2:
                response = f"[ERROR] Required 2 arguments, found {len(options)}"
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

                    response = f"[OK] Added Team Id {team.id}"  # team.id needs to be the last argument

        elif cmd == "get_team_live_orders":
            if len(options) == 0:
                response = "[ERROR] Please provide team id!"
            elif len(options) != 1:
                response = f"[ERROR] Required 1 argument, found {len(options)}"
            else:
                team_id = options[0]

                # Instantiate Order objects and add to Team object
                orders = team_factory.get_live_orders(team_id)
                if len(orders) > 0:
                    # <order_id>_<size>_<price>_<type>_<status>
                    # e.g. 8_50_98.0_BUY_LIVE
                    formatted_orders = order_factory.format_orders(orders)
                    response = f"[OK]{formatted_orders}"
                else:
                    response = "[ERROR] Team currently has no live orders"

        elif cmd == "open_market":
            if len(options) != 0:
                response = f"[ERROR] Required no arguments, found {len(options)}"
            else:
                exchange.open_market()
                status = exchange.get_market_status()

                if status:
                    response = "[OK] Market opened"
                else:
                    response = "[ERROR] Failed to open market"

        elif cmd == "close_market":
            if len(options) != 0:
                response = (f"[ERROR] Required no arguments, found {len(options)}")
            else:
                exchange.close_market()
                status = exchange.get_market_status()

                if not status:
                    response = "[OK] Market closed"
                else:
                    response = "[ERROR] Failed to close market"
        
        elif cmd == "get_elapsed_time":
            response = exchange.get_elapsed_time()
        
        elif cmd == "get_start_time":
            response = exchange.start_time
        
        elif cmd == "get_market_status":
            status = exchange.get_market_status()
            if status:
                response = "[OK] Market opened"
            else:
                response = "[OK] Market closed"

        

        socket.send_string(response)