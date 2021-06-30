import PySimpleGUI as sg
import tkinter as tk
import zmq
import sys
import subprocess

context = zmq.Context()
socket = context.socket(zmq.REQ)

def run_server(path, host, port):
    cmd = f'python3 "{path}" {host} {port}'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)

# Variables
launched = True
market_status = False

sg.theme('Default1')

col1 = sg.Column([
    [sg.Frame(layout=[
        [sg.T("Path to server app:"), sg.In(key="-SERVER_PATH-", change_submits=True), sg.FolderBrowse(key="-IN-")],
        [sg.T("Server host:", size=(14,1)), sg.In('127.0.0.1', key='-SERVER_HOST-', size=(20,1))],
        [sg.T("Server port number:"), sg.In('5890', key='-SERVER_PORT-', size=(10,1))]],
        title='Settings',
        font='Gotham')
    ],
    [sg.Frame(layout=[
        [sg.Button("Launch Server", key='-LAUNCH_SERVER-', button_color=('green')),
        sg.Button("Shut Down Server", key='-SHUTDOWN_SERVER-', button_color=('red'))],
        [sg.Button("Open the Market", key='-OPEN_MARKET-', button_color=('green')),
        sg.Button("Close the Market", key='-CLOSE_MARKET-', button_color=('red'))],
        [sg.Button("Clear Trade History", key='-CLEAR_TRADE-', button_color=('white'))]],
        title='Controls',
        font='Gotham')
    ]
])


tab1_layout = [[col1]]   

col2 = sg.Column([
    [sg.Frame(layout=[
        [sg.Table(
            key='-TEAMS_TABLE-',
            values=[],
            headings=['Team', 'P&L'],
            auto_size_columns=False,
            col_widths=[10, 20],
            justification='left'
        )]
        # [sg.T("Team"), sg.T(" "*30), sg.T("P&L")],
        # [sg.T("Team_A"), sg.T(" "*30), sg.In(size=(20,1))],
        # [sg.T("Team_B"), sg.T(" "*30), sg.In(size=(20,1))]
        ],
        title='Metrics', font='Gotham')],
    [sg.Frame(layout=[
        [sg.T("Elapsed time since open:"), sg.T('#NA', key="-ELAPSED_TIME-", size=(10,1))],
        [sg.T("Last trade price:"), sg.T('#NA', key="-LAST_TRADE_PRICE-", size=(10,1))]],
        title='Market', font='Gotham')]
    ])


tab2_layout = [[col2]]

layout = [[sg.TabGroup([[sg.Tab('Settings and Controls', tab1_layout, tooltip='tip'), 
         sg.Tab('Metrics and Market', tab2_layout)]], key='-TABS-', change_submits=True, tooltip='TIP2')]]
    
win = sg.Window('Trading Game Administrator', layout, icon='SUTDLogo.ico')

# Display and interact with the Window using an Event Loop
while True:
    event, values = win.read()

    # Read input values
    server_path = values['-SERVER_PATH-']
    server_host = values['-SERVER_HOST-']
    server_port = values['-SERVER_PORT-']

    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED:
        break
    
    # TODO: # Admin launches server
    # elif event == '-LAUNCH_SERVER-':
    #     run_server(server_path, server_host, server_port)
    #     launched = True
    
    # elif event == '-SHUTDOWN_SERVER-':
    #     # Connect to server
    #     socket.connect(f"tcp://{server_host}:{server_port}")

    #     # Shut down server
    #     request = "shutdown_server"
    #     socket.send_string(request)
    #     message = socket.recv().decode("utf-8")
    #     print(message)

    #     socket.disconnect(f"tcp://{server_host}:{server_port}")

    elif event == '-OPEN_MARKET-':
        # Connect to server
        socket.connect(f"tcp://{server_host}:{server_port}")

        # Send request to open market
        request = 'open_market'
        socket.send_string(request)
        message = socket.recv().decode("utf-8")
        status = message.split()[0]
        if status == '[OK]':
            print(message)
            market_status = True
        elif status == '[ERROR]':
            print(message)
    
    elif event == '-CLOSE_MARKET-':
        # Connect to server
        socket.connect(f"tcp://{server_host}:{server_port}")

        # Send request to open market
        request = 'close_market'
        socket.send_string(request)
        message = socket.recv().decode("utf-8")
        status = message.split()[0]
        if status == '[OK]':
            print(message)
            market_status = False
        elif status == '[ERROR]':
            print(message)
    
    elif event == '-TABS-':
        # if launched:

        # Connect to server
        socket.connect(f"tcp://{server_host}:{server_port}")

        # Update all team metrics
        request = 'get_all_team_metrics'
        socket.send_string(request)
        message = socket.recv().decode("utf-8")
        status = message.split()[0]
        if status == '[OK]':
            metrics = message.split()[1:]
            team_metrics = []
            for metrics_str in metrics:
                metric = metrics_str.split("_")
                team_id = metric[0]
                team_name = metric[1]
                team_pnl = metric[2]
                team_matched = metric[3]
                team_unmatched = metric[4]
                team_error = metric[5]
                team_metrics.append(metric[1:3])
            win['-TEAMS_TABLE-'].update(team_metrics)

        elif status == '[ERROR]':
            print(message)
    
    # Get market elapsed time and last trade price
    if launched:
        if not market_status:
            win['-ELAPSED_TIME-'].update('#NA')
            win['-LAST_TRADE_PRICE-'].update('#NA')
        else:
            # Connect to server
            socket.connect(f"tcp://{server_host}:{server_port}")

            # Send request to get elapsed time
            request = 'get_elapsed_time'
            socket.send_string(request)
            message = socket.recv().decode("utf-8")
            status = message.split()[0]
            if status == '[OK]':
                print(message)
                win['-ELAPSED_TIME-'].update(message.split()[-1])
            elif status == '[ERROR]':
                print(message)
                win['-ELAPSED_TIME-'].update('#NA')

            # Send request to get last trade price
            request = 'get_last_trade_price'
            socket.send_string(request)
            message = socket.recv().decode("utf-8")
            status = message.split()[0]
            if status == '[OK]':
                print(message)
                win['-LAST_TRADE_PRICE-'].update(message.split()[-1])
            elif status == '[ERROR]':
                print(message)
                win['-LAST_TRADE_PRICE-'].update('#NA')

# Finish up by removing from the screen
win.close()
