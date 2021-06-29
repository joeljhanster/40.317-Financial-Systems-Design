# In[1]:
import PySimpleGUI as sg
import tkinter as tk
    
sg.theme('Default1')
data = ['a','b','c']

col1 = sg.Column([[sg.Frame(layout=[
            [sg.T("Path to server app:"), sg.In(), sg.Button('Browse')],
            [sg.T("Server host:", size=(14,1)), sg.In(size=(20,1))],
            [sg.T("Server port number:"), sg.In(size=(10,1))]],
        title='Settings',
        font='Gotham')],
    [sg.Frame(layout=[[sg.Button("Launch Server"), sg.Button("Shut Down Server")],
                                          [sg.Button("Open the Market",bg='blue'), sg.Button("Close the Market")],
                                          [sg.Button("Clear Trade History")]],title='Controls',font='Gotham')]])


tab1_layout = [[col1]]   

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

layout = [[sg.TabGroup([[sg.Tab('Settings and Controls', tab1_layout, tooltip='tip'), 
         sg.Tab('Metrics and Market', tab2_layout)]], tooltip='TIP2')]]
    
win = sg.Window('Trading Game Administrator', layout, icon='SUTDLogo.ico')

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
    
# In[1]:


