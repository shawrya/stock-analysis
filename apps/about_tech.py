import dash
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.dependencies import State , Output, Input
from app import app
layout = html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.H1("SMA")
                                    ],width={"offset":5}),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.Br(),
                                        html.Div([
                                            html.A("A simple moving average (SMA) is an arithmetic moving average calculated by adding recent prices and then dividing that figure by the number of time periods in the calculation average. For example, one could add the closing price of a security for a number of time periods and then divide this total by that same number of periods. Short-term averages respond quickly to changes in the price of the underlying security, while long-term averages are slower to react.",style= {"font-size":"20px"})
                                        ]),
                                    ]),

                                ]),
                                html.Br(),

                            ]),
                        ]),
                    ],style={'background-color':'#CCD7EA'},),
                ]),


                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.H1("RSI")
                                    ],width={"offset":5}),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.Br(),
                                        html.Div([
                                            html.A("The relative strength index (RSI) is a momentum indicator used in technical analysis that measures the magnitude of recent price changes to evaluate overbought or oversold conditions in the price of a stock or other asset. The RSI is displayed as an oscillator (a line graph that moves between two extremes) and can have a reading from 0 to 100. The indicator was originally developed by J. Welles Wilder Jr. and introduced in his seminal 1978 book New Concepts in Technical Trading Systems.",style= {"font-size":"20px"})
                                        ]),
                                    ]),
                                ]),
                                html.Br()
                            ]),
                        ]),
                    ],style={'background-color':'#CCD7EA'},),
                ]),


                dbc.Col([
                    dbc.Card([
                        #dbc.CardImg(src="C:/python_files/stock/assets/keanu.png", style={'width':'520px'},top=True),
                        dbc.CardBody([
                            html.Div([
                                dbc.Row([

                                    dbc.Col([
                                        html.H1("APO")
                                    ],width={"offset":5}),
                                ]),

                                dbc.Row([
                                    dbc.Col([
                                        html.Br(),
                                        html.Div([
                                            html.A("APO is calculated as the difference between two price moving averages and it is basically another name for the MACD indicator. We may call it by different names: OsMA, APO, MACD or simply two moving averages - in reality this is the same technical indicators. Crossovers of two moving averages correspond to crossovers of APO (MACD) and zero central signal line around it oscillates",style= {"font-size":"20px"}),
                                        ]),
                                    ]),
                                ]),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                            ]),
                        ]),
                    ],style={'background-color':'#CCD7EA'},),
                ]),



            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.H1("BOLLINGER BANDS")
                                    ],width={"offset":2}),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.Br(),
                                        html.Div([
                                            html.A("A Bollinger Band® is a technical analysis tool defined by a set of trendlines plotted two standard deviations (positively and negatively) away from a simple moving average (SMA) of a security's price, but which can be adjusted to user preferences.Bollinger Bands® were developed and copyrighted by famous technical trader John Bollinger, designed to discover opportunities that give investors a higher probability of properly identifying when an asset is oversold or overbought.",style= {"font-size":"20px"})
                                        ]),
                                    ]),
                                ]),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                            ]),
                        ]),
                    ],style={'background-color':'#CCD7EA'},),
                ]),


                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.H1("Aroon Oscillator")
                                    ],width={"offset":2}),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.Br(),
                                        html.Div([
                                            html.A("The Aroon indicator is a technical indicator that is used to identify trend changes in the price of an asset, as well as the strength of that trend. In essence, the indicator measures the time between highs and the time between lows over a time period. The idea is that strong uptrends will regularly see new highs, and strong downtrends will regularly see new lows. The indicator signals when this is happening, and when it isn't.The indicator consists of the \"Aroon up\" line, which measures the strength of the uptrend, and the \"Aroon down\" line, which measures the strength of the downtrend..",style= {"font-size":"20px"})
                                        ]),
                                    ]),
                                ]),
                                html.Br(),
                            ]),
                        ]),
                    ],style={'background-color':'#CCD7EA'},),
                ]),


                dbc.Col([
                    dbc.Card([
                        #dbc.CardImg(src="/assets/keanu.png", style={'width':'auto','height':'20px'},top=True),
                        dbc.CardBody([
                            html.Div([
                                dbc.Row([

                                    dbc.Col([
                                        html.H1("Exponential Moving Average")
                                    ]),
                                ]),

                                dbc.Row([
                                    dbc.Col([
                                        html.Br(),
                                        html.Div([
                                            html.A("An exponential moving average (EMA) is a type of moving average (MA) that places a greater weight and significance on the most recent data points. The exponential moving average is also referred to as the exponentially weighted moving average. An exponentially weighted moving average reacts more significantly to recent price changes than a simple moving average (SMA), which applies an equal weight to all observations in the period.",style= {"font-size":"20px"})
                                        ]),
                                    ]),
                                ]),
                                html.Br(),
                                html.Br(),

                                html.Br(),
                            ]),
                        ]),
                    ],style={'background-color':'#CCD7EA'},),
                ]),



            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.H1("Moving Average")
                                    ],width={"offset":2}),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.Br(),
                                        html.Div([
                                            html.A("n statistics, a moving average is a calculation used to analyze data points by creating a series of averages of different subsets of the full data set. In finance, a moving average (MA) is a stock indicator that is commonly used in technical analysis. The reason for calculating the moving average of a stock is to help smooth out the price data by creating a constantly updated average price.By calculating the moving average, the impacts of random, short-term fluctuations on the price of a stock over a specified time-frame are mitigated.",style= {"font-size":"20px"})
                                        ]),
                                    ]),
                                ]),
                                html.Br(),
                            ]),
                        ]),
                    ],style={'background-color':'#CCD7EA'},),
                ]),


                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.H1("Commodity Channel Index")
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.Br(),
                                        html.Div([
                                            html.A("Developed by Donald Lambert, the Commodity Channel Index​ (CCI) is a momentum-based oscillator used to help determine when an investment vehicle is reaching a condition of being overbought or oversold.This technical indicator is also used to assess price trend direction and strength. This information allows traders to determine if they want to enter or exit a trade, refrain from taking a trade, or add to an existing position. In this way, the indicator can be used to provide trade signals when it acts in a certain way.KEY TAEAWAYS",style= {"font-size":"20px"})
                                        ]),
                                    ]),
                                ]),
                                html.Br(),
                            ]),
                        ]),
                    ],style={'background-color':'#CCD7EA'},),
                ]),


                dbc.Col([
                    dbc.Card([
                        #dbc.CardImg(src="C:/python_files/stock/assets/keanu.png", style={'width':'520px'},top=True),
                        dbc.CardBody([
                            html.Div([
                                dbc.Row([

                                    dbc.Col([
                                        html.H1("Chande Momentum Oscilator")
                                    ],),
                                ]),

                                dbc.Row([
                                    dbc.Col([
                                        html.Br(),
                                        html.Div([
                                            html.A("The Chande momentum oscillator is a technical momentum indicator invented by Tushar Chande. The author introduced the indicator in his 1994 book “The New Technical Trader “. The formula calculates the difference between the sum of recent gains and the sum of recent losses and then divides the result by the sum of all price movement over the same period.",style= {"font-size":"20px"})
                                        ]),
                                    ]),
                                ]),

                                html.Br(),
                                html.Br(),
                                html.Br(),
                            ]),
                        ]),
                    ],style={'background-color':'#CCD7EA'},),
                ]),



            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.H1("Moving Average Convergence/Divergence")
                                    ],),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.Br(),
                                        html.Div([
                                            html.A("Moving average convergence divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price. The MACD is calculated by subtracting the 26-period exponential moving average (EMA) from the 12-period EMA. The result of that calculation is the MACD line. A nine-day EMA of the MACD called the \"signal line,\" is then plotted on top of the MACD line, which can function as a trigger for buy and sell signals. ",style= {"font-size":"20px"})
                                        ]),
                                    ]),
                                ]),
                                html.Br(),
                            ]),
                        ]),
                    ],style={'background-color':'#CCD7EA'},),
                ]),


                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.H1("Stochastic")
                                    ],width={"offset":3}),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.Br(),
                                        html.Div([
                                            html.A("A stochastic oscillator is a momentum indicator comparing a particular closing price of a security to a range of its prices over a certain period of time. The sensitivity of the oscillator to market movements is reducible by adjusting that time period or by taking a moving average of the result. It is used to generate overbought and oversold trading signals, utilizing a 0–100 bounded range of values. Stochastic oscillator charting generally consists of two lines: one reflecting the actual value of the oscillator for each session, and one reflecting its three-day simple moving average. ",style= {"font-size":"20px"})
                                        ]),
                                    ]),
                                ]),
                                html.Br(),
                            ]),
                        ]),
                    ],style={'background-color':'#CCD7EA'},),
                ]),


                dbc.Col([
                    dbc.Card([
                        #dbc.CardImg(src="C:/python_files/stock/assets/keanu.png", style={'width':'520px'},top=True),
                        dbc.CardBody([
                            html.Div([
                                dbc.Row([

                                    dbc.Col([
                                        html.H1("Chaikin A/D Oscillator")
                                    ],width={"offset":2}),
                                ]),

                                dbc.Row([
                                    dbc.Col([
                                        html.Br(),
                                        html.Div([
                                            html.A("The relative strength index (RSI) is a momentum indicator used in technical analysis that measures the magnitude of recent price changes to evaluate overbought or oversold conditions in the price of a stock or other asset. The RSI is displayed as an oscillator (a line graph that moves between two extremes) and can have a reading from 0 to 100. The indicator was originally developed by J. Welles Wilder Jr. and introduced in his seminal 1978 book New Concepts in Technical Trading Systems.",style= {"font-size":"20px"})
                                        ]),
                                    ]),
                                ]),

                                html.Br(),
                                
                            ]),
                        ]),
                    ],style={'background-color':'#CCD7EA'},),
                ]),



            ]),
            html.Br(),
],className='ccontent')



@app.callback(
    Output("sma_collapse", "is_open"),
    [Input("formula_sma", "n_clicks")],
    [State("sma_collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    '''
    this function is used to open collapse bar
    '''
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("rsi_collapse", "is_open"),
    [Input("formula_rsi", "n_clicks")],
    [State("rsi_collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    '''
    this function is used to open collapse bar
    '''
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("apo_collapse", "is_open"),
    [Input("formula_apo", "n_clicks")],
    [State("apo_collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    '''
    this function is used to open collapse bar
    '''
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("bbs_collapse", "is_open"),
    [Input("formula_bbs", "n_clicks")],
    [State("bbs_collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    '''
    this function is used to open collapse bar
    '''
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("aroon_collapse", "is_open"),
    [Input("formula_aroon", "n_clicks")],
    [State("aroon_collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    '''
    this function is used to open collapse bar
    '''
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("ema_collapse", "is_open"),
    [Input("formula_ema", "n_clicks")],
    [State("ema_collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    '''
    this function is used to open collapse bar
    '''
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("ma_collapse", "is_open"),
    [Input("formula_ma", "n_clicks")],
    [State("ma_collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    '''
    this function is used to open collapse bar
    '''
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("cci_collapse", "is_open"),
    [Input("formula_cci", "n_clicks")],
    [State("cci_collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    '''
    this function is used to open collapse bar
    '''
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("cmo_collapse", "is_open"),
    [Input("formula_cmo", "n_clicks")],
    [State("cmo_collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    '''
    this function is used to open collapse bar
    '''
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("macd_collapse", "is_open"),
    [Input("formula_macd", "n_clicks")],
    [State("macd_collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    '''
    this function is used to open collapse bar
    '''
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("stoch_collapse", "is_open"),
    [Input("formula_stoch", "n_clicks")],
    [State("stoch_collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    '''
    this function is used to open collapse bar
    '''
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("ad_collapse", "is_open"),
    [Input("formula_ad", "n_clicks")],
    [State("ad_collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    '''
    this function is used to open collapse bar
    '''
    if n:
        return not is_open
    return is_open
