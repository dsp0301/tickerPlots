import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, State, Output
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objs as go
import request_stock_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.H4('TickerPlots'),

    html.Div([
        dcc.Loading(children=[
            dcc.Graph(id='stock-chart', style={'width':'100%'})
        ]),
        html.Div("Free Version of AlphaVantage API can only make 2 requests per minute.\
                  Please wait 30 to 60 seconds before updating again.")
    ], style={'width': '700px', 'display': 'inline-block'}),

    html.Div([
        html.Div(children=[
            html.Label('Technical Indicators'),
            dcc.Checklist(
                id='tech-indicators',
                options=[
                    {'label': 'SMA', 'value': 'sma'},
                    {'label': 'EMA', 'value': 'ema'}
                ],
                value=['sma'],
                labelStyle={'display': 'inline-block'}
            ),
        ], style={'display': 'inline-block',
                  'padding-top': '10px',
                  'margin-right': '35px'}),
        html.Div([
            dcc.Input(id='ticker-input', value='TSLA', type='text'),
            html.Button('Update', id='update_btn'),
        ], style={'display': 'inline-block'}),
    ]),


], style={'width': '100vw',
          'height': '100vh',
          'text-align': 'center'})


@app.callback(
    Output('stock-chart', 'figure'),
    [Input('update_btn', 'n_clicks')],
    [State('ticker-input', 'value'),
     State('tech-indicators', 'value')])
def update_stock_chart(n_clicks, ticker, tech_indicators):

    sma = 'sma' in tech_indicators
    ema = 'ema' in tech_indicators

    try:
        df = request_stock_data.fetch_stock_data(ticker, sma=sma, ema=ema)
    except:
        raise PreventUpdate

    traces = []

    trace = go.Candlestick(
                x=df.index,
                open=df['1. open'],
                high=df['2. high'],
                low=df['3. low'],
                close=df['4. close'],
                name='OHLC')
    traces.append(trace)

    if sma:
        sma_trace = go.Scatter(
                        x=df.index,
                        y=df['SMA'],
                        mode='lines',
                        name='SMA',
                        line={'color': 'cyan'})
        traces.append(sma_trace)

    if ema:
        ema_trace = go.Scatter(
                        x=df.index,
                        y=df['EMA'],
                        mode='lines',
                        name='EMA',
                        line={'color': 'blue'})
        traces.append(ema_trace)

    layout= {'title': ticker,
             'plot_bgcolor': 'rgba(0,0,0,0)',
             'paper_bgcolor': 'rgba(0,0,0,0)',
             'font': {'size': 18,
                      'color': "rgb(99, 99, 100)"}}

    return {
        'data': traces,
        'layout': layout
    }

if __name__ == '__main__':
    app.run_server(debug=True)
