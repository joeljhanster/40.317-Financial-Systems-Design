# In[1]:
import PySimpleGUI as sg

cash_balance = 0

col1 = sg.Column([
    # Categories frame
    [sg.Frame(layout=[[sg.Text("Shares"), sg.Text("Cash", pad=(100, 0))],
                      [sg.InputText(cash_balance, size=(19, 1)), sg.InputText('0', size=(19, 1))]],
              title='Balances', font = 'Gotham')],
    
    [sg.Frame(layout=[[sg.InputText('0', size=(25, 1)), sg.Button('Deposit')]],
              title='Deposit Cash', font = 'Gotham')],
    
    [sg.Frame(layout=[[sg.Text("Quantity"), sg.Text("Price per Share", pad=(100, 0))],
                      [sg.InputText('0', size=(19, 1)), sg.InputText('0', size=(19, 1)), sg.Button('Buy')]],
              title='Buy Shares', font = 'Gotham')],
    
    [sg.Frame(layout=[[sg.Text("Quantity"), sg.Text("Price per Share", pad=(100, 0))],
                      [sg.InputText('0', size=(19, 1)), sg.InputText('0', size=(19, 1)), sg.Button('Sell')]],
              title='Sell Shares', font = 'Gotham')],
    
    [sg.Button('Close Server & Quit', 'center')],
    
    [sg.Frame(layout=[[sg.Button('Save'), sg.Button('Delete'), sg.Sizer(280, 10)]], title='')]
    
    ], element_justification ='center')

# Define the window's contents
layout = [ [col1] ]

# Create the window
#window = sg.Window('Holdings Manager', icon = 'SUTD Logo.ico', layout)
window = sg.Window('Holdings Manager', layout, icon='SUTDLogo.ico').read(close=True)


# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    # Output a message to the window
    window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")

# Finish up by removing from the screen
window.close()