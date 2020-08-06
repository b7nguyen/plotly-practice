#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 16:41:52 2020

@author: b7nguyen

Fred Dashboard
User can select FRED stats and start and end date. 
A submit button will execute the changes. Default settings are the mortgage 
rate. 

Layout: Top left screen, select FRED stat. Top right screen select end start date. 
Bottom of screen, display line chart with X - as date, Y - rate or dollar amount


"""

import pandas_datareader as pdr
import pandas as pd
import datetime


from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash
import re

from datetime import datetime as dt

symbols = ['MORTGAGE30US', 'MORTGAGE15US', 'MORTGAGE5US']

#To get data from FRED (Federal Reserve Economic Data )
start = datetime.datetime (2005, 5, 1)
end = datetime.datetime (2020, 6, 1)
df = pdr.DataReader('MORTGAGE30US', 'fred', start, end)
df.reset_index(level=0, inplace=True) #df has date as the index. We want it as column



#step1: start the app
app = dash.Dash()

#%%
#step2: Setting up the plot. In this case, we use the Scatter object with mode = lines
#since we want to represent a time series line chart. The object is a dictionary with 
#data = go.Scatter object and layout = go.Layout
graph_line_figure = {'data':[go.Scatter(x=df.iloc[:,0],
                               y=df.iloc[:,1],
                               mode='lines')],
                     'layout':go.Layout(title='FRED',
                               xaxis={'title':df.columns[0]},
                               yaxis={'title':df.columns[1]}) }


                        
#step3: Create the html objects. Each will have its own unique object ID so we can 
#reference the object accordingly. Remember that dcc is the dash core component. 

#step3a: Create dcc.Graph
list_html_line_graph = [dcc.Graph(id='line_graph',
                        figure=graph_line_figure)]

#step3b: Create date picker object
date_selection = dcc.DatePickerRange(id='date_picker',
                                      min_date_allowed=dt(1950, 1, 1),
                                      max_date_allowed=dt.today(),
                                      initial_visible_month=dt(2000, 1, 1,),
                                      start_date=dt(2000, 1, 1).date(),
                                      end_date=dt.today().date())

#step3c: Create symbol selection as drop down. 
symbol_selection = dcc.Dropdown(id='symbol_choice',
                                 options=[{'label':i, 'value':i} for i in symbols],
                                 value='MORTGAGE30US',
                                 multi=True)

#step3d: Create a submit button. html is a dash html component
submit_button = html.Button(id='submit_button',
                            children='Submit')


#step4: Put together the layout with all objects created in step 3. 
    
app.layout = html.Div([ html.H1('Mortgage Rate Dash'),
                        html.Div([html.H3('Enter the dates'), 
                                  date_selection,], 
                                  style={'display':'inline-block', 'verticalAlign':'top'}),
                        html.Div([html.H3('Enter the loan type'), 
                                  symbol_selection], 
                                  style={'display':'inline-block'}),
                        html.Div(submit_button),
                        html.Div(list_html_line_graph) ])


#step5: Create callback
@app.callback(Output('line_graph', 'figure'),
              [Input('submit_button', 'n_clicks')], #Not sure if n_clicks is needed
              [State('symbol_choice', 'value'),
               State('date_picker', 'start_date'),
               State('date_picker', 'end_date')])
def output(n_clicks, symbol, start_date, end_date):
    #To get data from FRED (Federal Reserve Economic Data )
    # start = datetime.datetime (2005, 5, 1)
    # end = datetime.datetime (2020, 6, 1)
    # df = pdr.DataReader('MORTGAGE30US', 'fred', start, end)
    # df.reset_index(level=0, inplace=True) #df has date as the index. We want it as column
    print('in Callback')
    #TBD work with stripping time and date. Date is in string format year/month/day
    start_date = re.split(r'\W+', start_date)
    start = datetime.datetime(int(start_date[0]), int(start_date[1]), int(start_date[2]) )
    
    end_date = re.split(r'\W+', end_date)
    end = datetime.datetime(int(end_date[0]), int(end_date[1]), int(end_date[2]) )
    
    scatter_list = [] 
    
    #start = datetime.datetime (start_date.year, start_date.month, start_date.day)
    #end = datetime.datetime (end_date.year, end_date.month, end_date.day)
    print(f'start date is {start}\n')
    print(f'end date is {end}\n')
    print(f'symbol is {symbol} type is {type(symbol)}\n')
    
    symbol_list = []
    
    if (type(symbol)==str):
        symbol_list.append(symbol)
    else:
        symbol_list = symbol

    for i in symbol_list: 
        print(f'i symbol is {i}\n')
        df = pdr.DataReader(i, 'fred', start, end)
        df.reset_index(level=0, inplace=True) #df has date as the index. We want it as column
        
        scatter_list.append(go.Scatter(x=df.iloc[:,0], y=df.iloc[:,1], mode='lines'))
        

    figure = {'data':scatter_list,
              'layout':go.Layout(title='FRED',
                           xaxis={'title':df.columns[0]},
                           yaxis={'title':df.columns[1]}) }
    return figure


#Run app
if __name__ == '__main__': 
    app.run_server()

