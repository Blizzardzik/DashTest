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
def kpiChartGraph(CovidDataSummary):
    return html.Div([
        dcc.Graph(id='kpi-chart', config={'displayModeBar':True}, figure=go.Figure(go.Indicator(
       mode="number+gauge+delta",
       gauge={'shape': "bullet",
              'bgcolor': 'white',
              'bar': {'color': "red"},
              'threshold': {
                  'line': {'color': "grey", 'width': 2},
                  'thickness': 0.75, 'value': 500000}, },

       value=CovidDataSummary['TotalDeaths'].sum(),
       delta={'reference': 500000},
       domain={'x': [0, 1], 'y': [0, 1]},
       title={'text': "<b>     Deaths</b><br><span style='color: gray; font-size:0.8em'>Covid 2019</span>",
              'font': {"size": 13}}))
                  )])
##this function creates a map in plotly taking CovidDataSummary data call from api - data frame as input
def cloropethMap(CovidDataSummary):
    return html.Div([
        dcc.Graph(id='chloropeth-map', config={'displayModeBar':True}, figure={
                'data': [
                    # map
                    go.Choropleth(
                        locations=CovidDataSummary['Country'],
                        z=CovidDataSummary['TotalDeaths'],
                        text=CovidDataSummary['Country'],
                        locationmode='country names',
                        colorscale='Reds',
                        autocolorscale=False,
                        reversescale=False,
                        marker_line_color='darkgray',
                        marker_line_width=0.5,
                        colorbar_tickprefix='Deaths  :',
                        colorbar_title='Covid-2019<br>Total Deaths',
                    )

                ],
                'layout': go.Layout(
                    title_text='Covid-2019 Countries by Total Deaths',
                    geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    projection_type='equirectangular'
                    ),
                    annotations=[dict(
                        x=0.55,
                        y=0.1,
                        xref='paper',
                        yref='paper',
                        text='Source: <a href="https://api.covid19api.com/">\
                                Covid-2019 open API</a>',
                        showarrow=False
                    )]
                )
            }
        )
    ])
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
              ]),
    html.H4('Total confirmed deaths so far - 500k as the target'),
    html.Div([kpiChartGraph(summaryDataFromApi())]),
    html.Div([cloropethMap(summaryDataFromApi())])
                      ])

#@app.callback(dash.dependencies.Output('display-value', 'children'),
#              [dash.dependencies.Input('dropdown', 'value')])
#def display_value(value):
#    return 'You have selected "{}"'.format(value)


## CSS
external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                 "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                 "//fonts.googleapis.com/css?family=Dosis:Medium",
                 "https://cdn.rawgit.com/plotly/dash-app-stylesheets/62f0eb4f1fadbefea64b2404493079bf848974e8/dash-uber-ride-demo.css",
                 "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})


if __name__ == '__main__':
    app.run_server(debug=True)