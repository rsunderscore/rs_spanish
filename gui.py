# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 19:28:36 2021

@author: Rob
based on the pySimpleGUI cookbook
"""
import PySimpleGUI as sg
import spanishstuff

testlist = []

def ex1():
    #sg.theme('BluePurple')
    
    layout = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(15,1), key='-OUTPUT-')],
              [sg.Input(key='-IN-')],
              [sg.Button('Show'), sg.Button('Exit'), sg.T('result'), sg.T(size=(15,1), key='result')]]
    
    window = sg.Window('Pattern 2B', layout)
    
    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Show':
            # Update the "output" text element to be the value of "input" element
            if values['-IN-'] == 'fred':
                res = 'YOU WIN!'
            else:
                res = 'oops, no.'
            window['result'].update(res + " " + values['-IN-'])
    
    window.close()


def multi_q_window():
    import PySimpleGUI as sg
    import pandas as pd
    
    layout = []
    for i in range(10):
        layout.append([sg.T('Question'+str(i)), sg.I(key=f'answer{i}')])
        
    layout.append([sg.Button('Show'), sg.Button('Exit'), sg.T('result'), sg.T(size=(15,1), key='result')])
    
    #print(layout)
    
    window = sg.Window('built up form', layout)
    while True:  # Event Loop
        event, values = window.read()
        print(event, pd.Series(values))
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Show':
            #print('show')
            #Update the "output" text element to be the value of "input" element
            if values['answer0'] == 'fred':
                res = 'YOU WIN!'
            else:
                res = 'oops, no.'
            window['result'].update(res + " " + values['answer0'])
    window.close()
    
def test_multi_q_window():
    multi_q_window()
