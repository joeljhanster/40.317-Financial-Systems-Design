import PySimpleGUI as sg
import tkinter as tk
    
sg.theme('Default1')
data = ['a','b','c']
sutd_logo = r'' # INSERT PATH TO SUTD LOGO

col1 = sg.Column([[sg.T('SERVER IP ADDRESS', size=(20,1), justification='center', relief=sg.RELIEF_RIDGE), sg.In(size=(25, 1))],
                [sg.T('SERVER PORT', size=(20,1), justification='center', relief=sg.RELIEF_RIDGE), sg.InputText(size=(25, 1))],
                [sg.T()],
                [sg.T()],
                [sg.T('TEAM NAME', size=(12,1), justification='center', relief=sg.RELIEF_RIDGE), sg.InputText(size=(33, 1))],
                [sg.T('FAMILY NAME', size=(15,1), justification='center', relief=sg.RELIEF_RIDGE), sg.In(size=(15, 1))],
                [sg.T('GIVEN NAME', size=(15,1), justification='center', relief=sg.RELIEF_RIDGE), sg.In(size=(15, 1))],
                [sg.Button('ADD MEMBER')],
                [sg.T()],
                [sg.T()],
                [sg.T()],
                [sg.T()],
                [sg.Button('REGISTER TEAM!')]
                ],element_justification ='left')

col2 = sg.Column([[sg.Image(sutd_logo)],
                  [sg.T()],
                  [sg.Button('TEAM MEMBERS')],
                  [sg.Table(values = data, headings=['FULL NAME', 'ROLE', 'ID#'], 
                            auto_size_columns=False, col_widths=[20, 10, 10])]],element_justification ='center')


tab1_layout = [[col1, col2]]   

col3 = sg.Column([[sg.Button('"Trade Warriors" ORDER BOOK', size=(30,1))],
                   [sg.Table(values = [], headings=['ID #', 'SIZE', 'PRICE', 'TYPE', 'STATUS'], auto_size_columns=False, col_widths=[10, 10, 10, 10, 10])],
                  [sg.Button('REFRESH', size=(10,1)), sg.Button('FILL', size=(10,1)), sg.Button('CANCEL', size=(10,1))]
                ],element_justification ='centre')

col4 = sg.Column([[sg.T('P&L', size=(15,1), justification='center', relief=sg.RELIEF_RIDGE)],
                [sg.T('0.00', size=(15,1), justification='center', relief=sg.RELIEF_RIDGE)],
                [sg.T('# MATCHED TRADES', size=(20,1), justification='center', relief=sg.RELIEF_RIDGE)],
                [sg.T('0', size=(20,1), justification='center', relief=sg.RELIEF_RIDGE)],
                [sg.T('# UNMATCHED TRADES', size=(20,1), justification='center', relief=sg.RELIEF_RIDGE)],
                [sg.T('0', size=(20,1), justification='center', relief=sg.RELIEF_RIDGE)],
                [sg.T('# ERROR TRADES', size=(20,1), justification='center', relief=sg.RELIEF_RIDGE)],
                [sg.T('0', size=(20,1), justification='center', relief=sg.RELIEF_RIDGE)],
                ],element_justification ='centre')

tab2_layout = [[col3, col4]]    

layout = [[sg.TabGroup([[sg.Tab('REGISTRATION', tab1_layout, tooltip='tip'), 
         sg.Tab('DASHBOARD', tab2_layout)]], tooltip='TIP2')]]
    
win = sg.Window('Trading Game Team Console', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = win.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED:
        break
    
    elif event == 'ADD MEMBER':
        data.append(values)
        print('SERVER IP ADDRESS is:', values[0])
        print('SERVER PORT is:', values[1])
        print('TEAM NAME is:', values[2])
        print('FAMILY NAME is:', values[3])
        print('GIVEN NAME is:', values[4])
        
    elif event == 'REGISTER TEAM!':
        print('GIVEN NAME is:', values[4])

# Finish up by removing from the screen
win.close()
