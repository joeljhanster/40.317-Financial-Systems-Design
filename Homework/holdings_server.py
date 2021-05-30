# The server code for 40.317 Homework 1.  This code is not complete.

import zmq
import sys
from decimal import Decimal, DecimalException

# To run the server at a non-default port, the user provides the alternate port
# number on the command line.
port = "5890"  # Our default port.
if len(sys.argv) > 1:
    port = sys.argv[1]
    print("Overriding default port to", port)
    _ = int(port)

context = zmq.Context()
# Using "zmq.PAIR" means there is exactly one server for each client
# and vice-versa.  For this application, zmq.PAIR is more appropriate
# than zmq.REQ + zmq.REP (make sure you understand why!).
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:" + port)
print("I am the server, now alive and listening on port", port)

# This server maintains two quantities:
# - the number of shares we currently hold, and
share_balance = 0
# - the amount of cash we currently hold.
cash_balance = Decimal('0')

# (You might find this useful for rounding off cash amounts:)
penny = Decimal('0.01')


# This server must support the following commands:
# - "buy <# of shares> <price per share>"
# - "sell <# of shares> <price per share>"
# - "deposit_cash <amount>"
# - "get_share_balance"
# - "get_cash_balance"
# - "shutdown_server"
# - "help"

# Each of these commands must always return a one-line string.
# This string must begin with "[ERROR] " if any error occurred,
# otherwise it must begin with "[OK] ".

# Any command other than the above must generate the return string
# "[ERROR] Unknown command" .

# The behaviour of each of the above commands, in more detail:

# - "buy <# of shares> <price per share>"
#   Must perform the appropriate validations on these two quantities,
#   then must modify share_balance and cash_balance to reflect the
#   purchase, and return the string "[OK] Purchased" .

# - "sell <# of shares> <price per share>"
#   Must perform the appropriate validations on these two quantities,
#   then must modify share_balance and cash_balance to reflect the
#   sale, and return the string "[OK] Sold" .

# - ""deposit_cash <amount>"
#   Must perform the appropriate validations, i.e. ensure <amount>
#   is a positive number; then must add <amount> to cash_balance, and
#   return the string "[OK] Deposited" .

# - "get_share_balance"
#   Must return "[OK] " followed by the number of shares on hand.

# - "get_cash_balance"
#   Must return "[OK] " followed by the amount of cash on hand.

# - "shutdown_server"
#   Must return the string "[OK] Server shutting down" and then exit.

# - "help"
#   Must return the string "[OK] Supported commands: " followed by
#   a comma-separated list of the above commands.


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
    elif cmd == "help":
        response = "[OK] Supported commands: "
        response += "[buy <# of shares> <price per share>, "
        response += "sell <# of shares> <price per share>, "
        response += "deposit_cash <amount>, "
        response += "get_share_balance, "
        response += "get_cash_balance, "
        response += "shutdown_server, "
        response += "help]"
        socket.send_string(response)
    elif cmd == "buy":
        if len(tokens[1:]) < 2:
            socket.send_string("[ERROR] Two arguments expected, only received {0}.".format(len(tokens[1:])))
        # try:
        #     no_of_shares = int(token[1])
        # except ValueError:
        #     socket.send_string("[ERROR] First argument (# of shares) needs to be an Integer.")
        # try:
        #     price_per_share = float(token[2])
        # except ValueError:
        #     socket.send_string("[ERROR] Secondg argument (price per share) needs to be a Float.")

    else:
        options = tokens[1:]
        # The response is a function of cmd and options:
        response = ...  # YOUR CODE HERE
        socket.send_string(response)
