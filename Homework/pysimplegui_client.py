import PySimpleGUI as sg
import zmq
import sys
from time import sleep
from datetime import datetime

port = "5890"  # Our default server port.
if len(sys.argv) > 1:
    port = sys.argv[1]
    print("Overriding default port to", port)
    ignored = int(port)

context = zmq.Context()
# Using "zmq.PAIR" means there is exactly one server for each client
# and vice-versa.  For this application, zmq.PAIR is more appropriate
# than zmq.REQ + zmq.REP (make sure you understand why!).
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:" + port)


def get_share_balance():
    # Get share balance
    cmd = 'get_share_balance'
    socket.send_string(cmd)
    message = socket.recv().decode("utf-8").split()

    if message[0] == '[OK]':
        share_balance = message[1]
    else:
        share_balance = '0'

    return share_balance


def get_cash_balance():
    # Get çash balance
    cmd = 'get_cash_balance'
    socket.send_string(cmd)
    message = socket.recv().decode("utf-8").split()

    if message[0] == '[OK]':
        cash_balance = message[1]
    else:
        cash_balance = '0'

    return cash_balance


def get_latest_vwaps():
    # Get latest vwaps
    cmd = 'get_latest_vwaps'
    socket.send_string(cmd)
    message = socket.recv().decode("utf-8").split()
    if message[0] == '[OK]':
        buy_vwap = message[1]
        sell_vwap = message[2]
    else:
        buy_vwap = 'N/A'
        sell_vwap = 'N/A'

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    return f'{current_time} Buy VWAP={buy_vwap}, Sell VWAP={sell_vwap}'


share_balance = get_share_balance()
cash_balance = get_cash_balance()
latest_vwaps = get_latest_vwaps()

col1 = sg.Column([
    # Categories frame
    [sg.Frame(
        layout=[
            [
                sg.Text("Shares"),
                sg.Text("Cash", pad=(100, 0))
            ],
            [
                sg.Text(share_balance, size=(19, 1), key='-SHARE_BALANCE-'),
                sg.Text(cash_balance, size=(19, 1), key='-CASH_BALANCE-')
            ]
        ],
        title='Balances',
        font='Gotham'
    )],

    [sg.Frame(
        layout=[
            [
                sg.InputText('0', size=(25, 1)),
                sg.Button('Deposit')
            ]
        ],
        title='Deposit Cash',
        font='Gotham'
    )],

    [sg.Frame(
        layout=[
            [
                sg.Text("Quantity"),
                sg.Text("Price per Share", pad=(100, 0))
            ],
            [
                sg.InputText('0', size=(19, 1)),
                sg.InputText('0', size=(19, 1)),
                sg.Button('Buy')]
            ],
        title='Buy Shares',
        font='Gotham'
    )],

    [sg.Frame(
        layout=[
            [
                sg.Text("Quantity"),
                sg.Text("Price per Share", pad=(100, 0))
            ],
            [
                sg.InputText('0', size=(19, 1)),
                sg.InputText('0', size=(19, 1)),
                sg.Button('Sell')
            ]
        ],
        title='Sell Shares',
        font='Gotham'
    )],

    [sg.Button('Close Server & Quit')],

    [sg.Frame(
        layout=[
            [sg.Text(latest_vwaps, size=(75, 1), key='-LATEST_VWAPS-')]
        ],
        title='Latest VWAPS',
        font='Gotham'
    )],

    [sg.Frame(
        layout=[
            [sg.Text('', size=(75, 1), key='-INFO_MESSAGE-')]
        ],
        title='Info Message',
        font='Gotham'
    )]

    ], element_justification='center')

# Define the window's contents
layout = [[col1]]

# Create the window
window = sg.Window('Holdings Manager', layout, icon='SUTDLogo.ico')

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    message = ''

    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Close Server & Quit':
        cmd = 'shutdown_server'
        socket.send_string(cmd)
        break

    if event == 'Deposit':
        deposit_cash = values[0]
        cmd = f'deposit_cash {deposit_cash}'
        socket.send_string(cmd)
        message = socket.recv()

    elif event == 'Buy':
        buy_qty = values[1]
        buy_price = values[2]
        cmd = f'buy {buy_qty} {buy_price}'
        socket.send_string(cmd)
        message = socket.recv()

    elif event == 'Sell':
        sell_qty = values[3]
        sell_price = values[4]
        cmd = f'sell {sell_qty} {sell_price}'
        socket.send_string(cmd)
        message = socket.recv()

    message = message.decode("utf-8")
    response = message.split()[0]
    window['-INFO_MESSAGE-'].update(message)
    if response == '[OK]':
        print(message)
        # Print success message (green)
        window['-INFO_MESSAGE-'].update(text_color='green')
    elif response == '[ERROR]':
        print(message)
        # Print error message (orange)
        window['-INFO_MESSAGE-'].update(text_color='orange')

    # Get share balance
    share_balance = get_share_balance()
    window['-SHARE_BALANCE-'].update(share_balance)

    # Get çash balance
    cash_balance = get_cash_balance()
    window['-CASH_BALANCE-'].update(cash_balance)

    # Get latest vwaps
    latest_vwaps = get_latest_vwaps()
    window['-LATEST_VWAPS-'].update(latest_vwaps)

# Finish up by removing from the screen
window.close()
sys.exit(0)
