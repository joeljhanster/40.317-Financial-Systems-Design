# The server code for 40.317 Homework 2.
import zmq
import sys

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
socket = context.socket(zmq.PAIR)
socket.bind(f"tcp://{host}:{port}")
print("I am the server, now alive and listening on port", port)

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

        socket.send_string(response)