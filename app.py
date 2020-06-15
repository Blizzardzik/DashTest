import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly
import json
import requests as req
import pandas as pd
import numpy as np

##getting data for us covid cases as time series from covid api
def getDataFromApiUS():
    jsonCovidDataUS=req.get('https://api.covid19api.com/total/dayone/country/united-states')
    jsonCovidDataUS.json()
    dataUS = jsonCovidDataUS.json()
    CovidDataUS = pd.json_normalize(dataUS)
    CovidDataUS=CovidDataUS.set_index('Date')
    return CovidDataUS
##making a line chart using plotly
#def graphLineChart(dataframe):

 #   return html.Div([
 #       dcc.Graph(
 #           id='bar-chart',
#           config={'displayModeBar': True},
 #           figure={fig=go.Figure(),
  #                      fig.add_trace(go.Scatter(x=dataframe.index,y=dataframe['Recovered'],
   #                 mode='lines',
   #                 name='Recovered')),
   # fig.add_trace(go.Scatter(x=dataframe.index,y=dataframe['Deaths'],
   #                 mode='lines',
   #                 name='Deaths')),
   # fig.add_trace(go.Scatter(x=dataframe.index,y=dataframe['Active'],
   #                 mode='lines',
   #                 name='Active'))
   # })])

##another api call with summary data for all countries
def summaryDataFromApi():
    jsonCovidData=req.get('https://api.covid19api.com/summary')
    NormalizeCovid=jsonCovidData.json()['Countries']
    CovidData = pd.json_normalize(NormalizeCovid)
    CovidDataSummary=CovidData.set_index('Date')
    return CovidDataSummary
##bar chart with summary data
def barChartSummary(CovidDataSummary):
    return html.Div([
        dcc.Graph(
            id='bar-chart',
            config={'displayModeBar': True},
            figure=(go.Figure(data=[go.Bar(y=CovidDataSummary['TotalDeaths'], x=CovidDataSummary['CountryCode'])], layout_title_text="Total Deaths by Country Covid-2019"
                              )))])










external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H2('Covid app'),
    html.H3('Summary by country - deaths'),
    html.Div([barChartSummary(summaryDataFromApi())
              ])
                      ])

#@app.callback(dash.dependencies.Output('display-value', 'children'),
#              [dash.dependencies.Input('dropdown', 'value')])
#def display_value(value):
#    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)