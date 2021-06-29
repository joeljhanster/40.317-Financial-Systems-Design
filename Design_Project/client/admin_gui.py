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
    [sg.Frame(layout=[[sg.Button("Launch Server", button_color=('green')), sg.Button("Shut Down Server", button_color=('red'))],
                                          [sg.Button("Open the Market",button_color=('green')), sg.Button("Close the Market", button_color=('red'))],
                                          [sg.Button("Clear Trade History", button_color=('white'))]],title='Controls',font='Gotham')]])


tab1_layout = [[col1]]   

col2 = sg.Column([[sg.Frame(layout=[
            [sg.T("Team"), sg.T(" "*30), sg.T("P&L")],
            [sg.T("Team_A"), sg.T(" "*30), sg.In(size=(20,1))],
            [sg.T("Team_B"), sg.T(" "*30), sg.In(size=(20,1))]],
        title='Metrics',
        font='Gotham')],
    [sg.Frame(layout=[[sg.T("Elapsed time since open:"), sg.In(size=(10,1))],
                                          [sg.T("Last trade price:"), sg.In(size=(10,1))]],title='Market',font='Gotham')]])


tab2_layout = [[col2]]    

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


