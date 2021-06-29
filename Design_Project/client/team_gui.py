import PySimpleGUI as sg
import tkinter as tk
import zmq
import sys
import re

context = zmq.Context()
socket = context.socket(zmq.REQ)
connected = False

sg.theme('Default1')

# Team members
player_names = []
player_ids = []
team_id = None
team_orders = []

# SUTD Logo
sutd_logo = r'' # INSERT PATH TO SUTD LOGO (use OS Directory)

# Team GUI Layouts
col1 = sg.Column([
    [sg.T('SERVER IP ADDRESS', size=(20,1), justification='center', relief=sg.RELIEF_RIDGE),
    sg.In('127.0.0.1', key='-SERVER_HOST-', size=(25, 1))],
    [sg.T('SERVER PORT', size=(20,1), justification='center', relief=sg.RELIEF_RIDGE),
    sg.InputText('5890', key='-SERVER_PORT-', size=(25, 1))],
    [sg.T(key='-SERVER_ERROR-', text_color='red', size=(45,1))],
    [sg.T()],
    [sg.T('TEAM NAME', size=(12,1), justification='center', relief=sg.RELIEF_RIDGE),
    sg.InputText(key='-TEAM_NAME-', size=(33, 1))],
    [sg.T('FAMILY NAME', size=(15,1), justification='center', relief=sg.RELIEF_RIDGE),
    sg.In(key='-FAMILY_NAME-', size=(15, 1))],
    [sg.T('GIVEN NAME', size=(15,1), justification='center', relief=sg.RELIEF_RIDGE),
    sg.In(key='-GIVEN_NAME-', size=(15, 1))],
    [sg.Button('ADD MEMBER', key='-ADD_MEMBER-')],
    [sg.T(key='-MEMBER_ERROR-', text_color='red', size=(45,1))],
    [sg.T()],
    [sg.T()],
    [sg.T()],
    [sg.Button('REGISTER TEAM!', key='-REGISTER_TEAM-')],
    [sg.T(key='-REGISTER_MESSAGE-', size=(45,1))]
], element_justification = 'left')

col2 = sg.Column([
    [sg.Image(sutd_logo)],
    [sg.T()],
    [sg.T('TEAM MEMBERS', size=(20,1), justification='center', relief=sg.RELIEF_RIDGE)],
    [sg.Table(
        key='-PLAYERS_TABLE-',
        values = [],
        headings=['ID #', 'FAMILY NAME', 'GIVEN NAME'], 
        auto_size_columns=False,
        col_widths=[5, 20, 20],
        justification='center'
    )]
], element_justification = 'center')


tab1_layout = [[col1, col2]]   

col3 = sg.Column([
    [sg.T('TEAM ORDER BOOK', key='-BOOK_TITLE-', size=(30,1), justification='center', relief=sg.RELIEF_RIDGE)],
    [sg.Table(key='-ORDER_TABLE-', values = [], headings=['ID #', 'SIZE', 'PRICE', 'TYPE', 'STATUS'], auto_size_columns=False, col_widths=[10, 10, 10, 10, 10])],
    [sg.Button('REFRESH', key='-REFRESH-', size=(10,1)), sg.Button('FILL', size=(10,1)),
    sg.Button('CANCEL', size=(10,1))],
    [sg.T('', key='-ORDER_ERROR-', size=(30, 1))]
], element_justification = 'center')

col4 = sg.Column([[sg.T('P&L', size=(15,1), justification='center', relief=sg.RELIEF_RIDGE)],
                [sg.T('0.00', size=(15,1), justification='center', relief=sg.RELIEF_RIDGE)],
                [sg.T('# MATCHED TRADES', size=(20,1), justification='center', relief=sg.RELIEF_RIDGE)],
                [sg.T('0', size=(20,1), justification='center', relief=sg.RELIEF_RIDGE)],
                [sg.T('# UNMATCHED TRADES', size=(20,1), justification='center', relief=sg.RELIEF_RIDGE)],
                [sg.T('0', size=(20,1), justification='center', relief=sg.RELIEF_RIDGE)],
                [sg.T('# ERROR TRADES', size=(20,1), justification='center', relief=sg.RELIEF_RIDGE)],
                [sg.T('0', size=(20,1), justification='center', relief=sg.RELIEF_RIDGE)],
                ],element_justification = 'center')

tab2_layout = [[col3, col4]]    

layout = [[sg.TabGroup([[sg.Tab('REGISTRATION', tab1_layout, tooltip='tip'), 
         sg.Tab('DASHBOARD', tab2_layout)]], key='-TABS-', change_submits=True, tooltip='TIP2')]]
    
win = sg.Window('Trading Game Team Console', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = win.read()

    # Read input values
    server_host = values['-SERVER_HOST-']
    server_port = values['-SERVER_PORT-']
    team_name = values['-TEAM_NAME-']
    family_name = values['-FAMILY_NAME-']
    given_name = values['-GIVEN_NAME-']

    # print('SERVER IP ADDRESS is:', server_host)
    # print('SERVER PORT is:', server_port)
    # print('TEAM NAME is:', team_name)
    # print('FAMILY NAME is:', family_name)
    # print('GIVEN NAME is:', given_name)

    # Clear error messages
    win['-SERVER_ERROR-'].update("")
    win['-MEMBER_ERROR-'].update("")
    win['-REGISTER_MESSAGE-'].update("")
    win['-ORDER_ERROR-'].update("")

    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED:
        # TODO: Clear data (team, members, orders)
        break
    
    # See if server information are filled
    elif len(server_host) == 0 or len(server_port) == 0:
        error = "Please fill in the missing server details!"
        win['-SERVER_ERROR-'].update(error)
    
    # User wants to add member
    elif event == '-ADD_MEMBER-':
        regex = "[^A-Za-z0-9]"
        family_name = re.sub(regex, " ", family_name)
        given_name = re.sub(regex, " ", given_name)

        # Check for valid player names
        if len(family_name.strip()) == 0 or len(given_name.strip()) == 0:
            error = "Please fill in the missing information!"
            win['-MEMBER_ERROR-'].update(error)
        else:
            # Connect to server
            socket.connect(f"tcp://{server_host}:{server_port}")

            # Add player to server, get player id
            sanitized_family_name = family_name.replace(" ", "_")
            sanitized_given_name = given_name.replace(" ", "_")
            request = f"add_player {sanitized_family_name} {sanitized_given_name}"
            
            socket.send_string(request)
            message = socket.recv().decode("utf-8")
            status = message.split()[0]

            if status == '[OK]':
                player_id = message.split()[-1]
                player_ids.append(player_id)
                player_names.append([player_id, family_name, given_name])
                win['-PLAYERS_TABLE-'].update(player_names)
            elif status == '[ERROR]':
                win['-MEMBER_ERROR-'].update(message)

    # User wants to register team
    elif event == '-REGISTER_TEAM-': 
        # Check for valid team name
        if len(team_name.strip()) == 0:
            error = "Please fill in the team name!"
            win['-REGISTER_MESSAGE-'].update(error)
            win['-REGISTER_MESSAGE-'].update(text_color='red')
        elif len(player_ids) == 0:
            error = "Please add members before creating a team!"
            win['-REGISTER_MESSAGE-'].update(error)
            win['-REGISTER_MESSAGE-'].update(text_color='red')
        else:
            # Connect to server
            socket.connect(f"tcp://{server_host}:{server_port}")

            # Add team to server, get team id
            sanitized_team_name = team_name.replace(" ", "_")
            sanitized_player_ids = " ".join(player_ids)
            request = f"add_team {sanitized_team_name} {sanitized_player_ids}"
            
            socket.send_string(request)
            message = socket.recv().decode("utf-8")
            status = message.split()[0]

            if status == '[OK]':
                team_id = message.split()[-1]
                win['-REGISTER_MESSAGE-'].update(message)
                win['-REGISTER_MESSAGE-'].update(text_color='green')
                win['-BOOK_TITLE-'].update(f'"{team_name.upper()}" ORDER BOOK')
                
                # Disable all elements to prevent further editing
                win['-SERVER_HOST-'].update(disabled=True)
                win['-SERVER_PORT-'].update(disabled=True)
                win['-SERVER_PORT-'].update(disabled=True)
                win['-TEAM_NAME-'].update(disabled=True)
                win['-FAMILY_NAME-'].update(disabled=True)
                win['-GIVEN_NAME-'].update(disabled=True)
                win['-ADD_MEMBER-'].update(disabled=True)
                win['-SERVER_PORT-'].update(disabled=True)
                win['-REGISTER_TEAM-'].update(disabled=True)

            elif status == '[ERROR]':
                win['-REGISTER_MESSAGE-'].update(message)
                win['-REGISTER_MESSAGE-'].update(text_color='red')
    
    # Update team details when user changes tabs or refreshes
    elif event == '-TABS-' or event == '-REFRESH-':
        if team_id is None:
            # Show error message to register team first
            error = "Please register team first!"
            win['-ORDER_ERROR-'].update(error)
            win['-ORDER_ERROR-'].update(text_color='red')
        else:
            # Connect to server
            socket.connect(f"tcp://{server_host}:{server_port}")

            # Get team live orders
            request = f"get_team_live_orders {team_id}"
            socket.send_string(request)
            message = socket.recv().decode("utf-8")
            status = message.split()[0]

            if status == '[OK]':
                # [order_id, size, price, type, status]
                orders = message.split()[1:]
                team_orders = []
                for order_str in orders:
                    order = order_str.split("_")
                    team_orders.append(order)
                win['-ORDER_TABLE-'].update(team_orders)
            elif status == '[ERROR]':
                win['-ORDER_ERROR-'].update(message)
                win['-ORDER_ERROR-'].update(text_color='red')
            
            # TODO: Get P&L & trades status (team metrics)
            # request = f"get_team_metrics {team_id}"
            # socket.send_string(request)
            # message = socket.recv().decode("utf-8")
            # status = message.split()[0]

            # if status == '[OK]':
            #     pass
            # elif status == '[ERROR]':
            #     pass

# Finish up by removing from the screen
win.close()
