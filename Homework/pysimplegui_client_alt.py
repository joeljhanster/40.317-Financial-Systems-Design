import zmq
import sys
import PySimpleGUI as sg
import datetime

def getTime():
    return datetime.datetime.now().strftime('%H:%M:%S')

# ZMQ ==================================================================================

port = "5890"  # Our default server port.
if len(sys.argv) > 1:
    port = sys.argv[1]
    print("Overriding default port to", port)
    ignored = int(port)

context = zmq.Context()
socket = context.socket(zmq.PAIR)
print("Connecting to server...")
socket.connect("tcp://localhost:" + port)

# PySimpleGUI ==============================================================================

main = sg.Column([
    [sg.Frame(  title='Balances', 
                layout=[    [sg.Text("Shares"), sg.Text("Cash", pad=(100, 0))],
                            [sg.Text('0', key='-SHARES-', size=(19, 1)), sg.Text('0', key='-CASH-', size=(19, 1))]],
                font = 'Gotham')],
    
    [sg.Frame(  title='Deposit Cash',
                layout=[    [sg.InputText('0', key='-DEPOSIT-', size=(25, 1)), sg.Button('Deposit')]],
                font = 'Gotham')],
    
    [sg.Frame(  title='Buy Shares', 
                layout=[    [sg.Text("Quantity"), sg.Text("Price per Share", pad=(100, 0))],
                            [sg.InputText('0', key='-QTY_BUY_SHARES-', size=(19, 1)), sg.InputText('0', key='-BUY_PRICE_PER_SHARE-', size=(19, 1)), sg.Button('Buy')]],
                font = 'Gotham')],
    
    [sg.Frame(  title='Sell Shares', 
                layout=[    [sg.Text("Quantity"), sg.Text("Price per Share", pad=(100, 0))],
                            [sg.InputText('0', key='-QTY_SELL_SHARES-', size=(19, 1)), sg.InputText('0', key='-SELL_PRICE_PER_SHARE-', size=(19, 1)), sg.Button('Sell')]],
                font = 'Gotham')],
    
    [sg.Button('Close Server & Quit')],
    
    # Time and VWAP Display
    [sg.Frame(  title='',   
                layout=[    [sg.Text(size=(40, 1), key='-VWAP-')]])]

    ], element_justification ='center')


console_input = sg.Frame(  title='',
                    layout=[[sg.Text("Direct Console Access")],
                            [sg.Input(key='-CONSOLE_IN-'), sg.Button('Ok')]])

console_output = sg.Text(size=(50, 4), key='-CONSOLE_OUT-')

layout = [ [main], [console_input], [console_output] ]

window = sg.Window('Holdings Manager', layout, finalize=True)

# Initialise request string.
rq = ''

# EVENT LOOP ==========================================================================
while True:

    # Update GUI =====================================

    # Update cash balance
    socket.send_string("get_cash_balance")
    message = socket.recv().decode("utf-8")
    # print(message)
    window['-CASH-'].update(message[5:])

    # Update share balance
    socket.send_string("get_share_balance")
    message = socket.recv().decode("utf-8")
    # print(message)
    window['-SHARES-'].update(message[5:])

    # Display Time and VWAP
    socket.send_string("get_latest_vwaps")
    message = socket.recv().decode("utf-8")
    # print(message)
    _, buy_vwap, sell_vwap = message.split()
    window['-VWAP-'].update(f"{getTime()}: Buy VWAP={buy_vwap}, Sell VWAP={sell_vwap} ")


    # Wait for Button Press =========================
    event, values = window.read()
    

    # Button Press Cases ============================
    if event == 'Close Server & Quit':
        socket.send_string("shutdown_server")
        message = socket.recv().decode("utf-8")
        print(message)
        break

    if event == sg.WINDOW_CLOSED:
        print('GUI: Quit')
        break
    
    if event == 'Ok':
        rq = values['-CONSOLE_IN-']

    if event == 'Deposit':
        rq = f"deposit_cash {values['-DEPOSIT-']}"

    if event == 'Buy':
        rq = f"buy {values['-QTY_BUY_SHARES-']} {values['-BUY_PRICE_PER_SHARE-']}"
    
    if event == 'Sell':
        rq = f"sell {values['-QTY_SELL_SHARES-']} {values['-SELL_PRICE_PER_SHARE-']}"

    socket.send_string(rq)
    message = socket.recv().decode("utf-8")
    print(message)
    window['-CONSOLE_OUT-'].update(message)

