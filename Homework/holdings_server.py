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

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_positive_number(s):
    if is_number(s):
        return Decimal(s) > 0
    else:
        return False


def is_positive_integer(s):
    if is_positive_number(s):
        return s.isnumeric()
    else:
        return False


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
        if cmd == "buy":
            if len(options) != 2:
                response = (
                    "[ERROR] Format is: "
                    "buy <# of shares> <price per share>"
                ).format(3, 5)
            elif (
                not is_positive_integer(options[0]) or
                not is_positive_number(options[1])
            ):
                response = (
                    "[ERROR] <# of share> is positive integer, "
                    "<price per share> is positive float"
                ).format(3, 5)
            else:
                trade = Decimal(options[0]) * Decimal(options[1])
                if trade > cash_balance:
                    response = (
                        "[ERROR] Cash Balance not enough. "
                        f"{cash_balance} vs trade: {trade}."
                    ).format(3, 5)
                else:
                    cash_balance -= trade
                    share_balance += Decimal(options[0])
                    response = "[OK] Purchased"

        elif cmd == "sell":
            if len(options) != 2:
                response = (
                    "[ERROR] Format is: "
                    "sell <# of shares> <price per share>"
                ).format(3, 5)
            elif (
                not is_positive_integer(options[0]) or
                not is_positive_number(options[1])
            ):
                response = (
                    "[ERROR] <# of share> is positive integer, "
                    "<price per share> is positive float"
                ).format(3, 5)
            else:
                n_shares, price = Decimal(options[0]), Decimal(options[1])
                if n_shares > share_balance:
                    response = (
                        "[ERROR] Share Balance not enough. "
                        f"{share_balance} vs trade: {n_shares}."
                    ).format(3, 5)
                else:
                    cash_balance += n_shares * price
                    share_balance -= n_shares
                    response = "[OK] Sold"

        elif cmd == "deposit_cash":
            if len(options) != 1:
                response = "[ERROR] Format is: deposit_cash <amount>"
            elif not is_positive_number(options[0]):
                response = "[ERROR] <amount> is positive float"
            else:
                amt = Decimal(options[0])
                cash_balance += amt
                response = "[OK] Deposited"

        elif cmd == "get_share_balance":
            if len(options) != 0:
                response = "[ERROR] Format is: get_share_balance"
            else:
                response = f"[OK] {share_balance}"

        elif cmd == "get_cash_balance":
            if len(options) != 0:
                response = "[ERROR] Format is: get_cash_balance"
            else:
                response = f"[OK] {cash_balance}"

        elif cmd == "help":
            if len(options) != 0:
                response = "[ERROR] Format is: help"
            else:
                response = (
                    "[OK] Supported commands: "
                    "buy <# of shares> <price per share>, "
                    "sell <# of shares> <price per share>, "
                    "deposit_cash <amount>, "
                    "get_share_balance, "
                    "get_cash_balance, "
                    "shutdown_server, "
                    "help"
                ).format(3, 5)
        else:
            response = "[ERROR] Unknown command"

        socket.send_string(response)
