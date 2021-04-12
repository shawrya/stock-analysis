import dash
import bs4
import requests
import pathlib
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import talib as ta
from dash.dependencies import State , Output, Input
from plotly.subplots import make_subplots
from bs4 import BeautifulSoup
from app import app
from datetime import datetime


layout = html.Div([
            dbc.Row([

                dbc.Col([

                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div(id='stock_price_history')
                                ]),
                            ],style={'background-color':'#CCD7EA'}),
                        ]),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div(id='share_statistics'),
                                ]),
                            ],style={'background-color':'#CCD7EA'}),
                        ]),
                    ],style={'width':'auto'}),
                    html.Br()
                ],width={'size':3}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dcc.DatePickerRange(
                                        id='date_picker',
                                        clearable  = True,
                                    ),
                                ]),

                                dbc.Col([
                                    dcc.RadioItems(
                                        id='graph_select',
                                        options=[
                                            {'label': 'Line', 'value': 'ln'},
                                            {'label': 'Candlestick', 'value': 'cn'},
                                        ],
                                        value='ln',
                                        labelStyle={'display': 'inline-block',"margin-right": "10px"}
                                    ),
                                ]),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Br(),
                                    dcc.Dropdown(id='technical_indicators_customization',
                                                options=[
                                                    {'label': 'Absolute Price Oscillator', 'value': 'APO'},
                                                    {'label': 'Aroon Oscillator', 'value': 'AROONOSC'},
                                                    {'label': 'Simple moving averge', 'value':'SMA'},
                                                    {'label': 'bollengier Bands', 'value': 'bbs'},
                                                    {'label': 'Exponential Moving Average','value':'EMA'},
                                                    {'label': 'Moving average','value':'MA'},
                                                    {'label': 'Triple Exponential Moving Average ','value':'T3'},
                                                    {'label': 'Weighted Moving Average','value':'WMA'},
                                                    {'label': 'Commodity Channel Index','value':'CCI'},
                                                    {'label': 'Chande Momentum Oscillator','value':'CMO'},
                                                    {'label': 'Moving Average Convergence/Divergence','value':'MACD'},
                                                    {'label': 'Relative Strength Index','value':'RSI'},
                                                    {'label': 'Stochastic','value':'STOCH'},
                                                    {'Label': 'Chaikin A/D Oscillator','value':'ADOSC'},
                                                ],
                                                multi = True,
                                                searchable = True,
                                                value = " "
                                    ),
                                    dcc.Loading(children=[
                                        dcc.Graph(id='hist_graph',figure={}),
                                    ],type='cube',fullscreen=True),
                                ]),

                            ]),


                        ]),
                    ],style={'background-color':'#CCD7EA'}),
                ],width={'size':9}),
            ]),
])

#-----classes-----

class technical_indicators:
    ''' here we will be taking the values from the historic dataset for checking the accuracy '''
    def __init__(self,dfh):
        self.df_selector = dfh
        self.df_selector.sort_values(by=['date'],ascending=[True],inplace=True)
        self.df = self.df_selector.copy()

    def calculations(self):
        '''calculations'''
        self.df['rsi'] = ta.RSI(self.df['close'],timeperiod=5)
        self.df['apo'] = ta.APO(self.df['close'],fastperiod=10,slowperiod=5,matype=0)
        self.df['upperband'], self.df['middleband'], self.df['lowerband'] = ta.BBANDS(self.df['close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
        self.df['ema'] = ta.EMA(self.df['close'],timeperiod=5)
        self.df['ma'] = ta.MA(self.df['close'], timeperiod=5, matype=0)
        self.df['sma'] = ta.MA(self.df['close'], timeperiod=5)
        self.df['t3'] = ta.T3(self.df['close'], timeperiod=5, vfactor=0)
        self.df['wma'] = ta.WMA(self.df['close'],timeperiod=5)
        self.df['aroonosc'] = ta.AROONOSC(self.df['high'],self.df['low'],timeperiod=5)
        self.df['cci'] = ta.CCI(self.df['high'],self.df['low'],self.df['close'],timeperiod=5)
        self.df['cmo'] = ta.CMO(self.df['close'],timeperiod=14)
        self.df['macd'], self.df['macdsignal'], self.df['macdhist'] = ta.MACDEXT(self.df['close'], fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
        self.df['slowk'], self.df['slowd'] = ta.STOCH(self.df['high'], self.df['low'], self.df['close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        self.df['fastk'],self.df['fastd'] = ta.STOCHRSI(self.df['close'], timeperiod=5, fastk_period=5, fastd_period=3, fastd_matype=0)
        self.df['ultosc'] = ta.ULTOSC(self.df['high'], self.df['low'], self.df['close'], timeperiod1=7, timeperiod2=14, timeperiod3=28)
        self.df['adosc'] = ta.ADOSC(self.df['high'],self.df['low'],self.df['close'],self.df['volume'],fastperiod=3,slowperiod=10)
        return self.df



class analysis():
    def __init__(self,value='MSFT'):
        self.df = pd.read_excel(f'.\data\{value}.xlsx')
        ti = technical_indicators(self.df)
        self.df = ti.calculations()


    def correlations(self,value = 'close'):
        '''
             This function is used to find the correlations
        '''
        self.df.drop(columns=['adjusted_close','volume','low','high'],inplace = True)
        correlations = self.df.corr()
        correlations.drop(['open',value,'upperband','middleband', 'lowerband','macdhist', 'slowk', 'slowd', 'fastk', 'fastd'],inplace=True)
        correlations = correlations[value]
        co_relation = pd.DataFrame({'Values':correlations.index,
                                    'Co-relation with close':correlations.values
                                   })
        co_relation = co_relation.round(4)
        return co_relation

    def other_calculations(self,start_date = datetime.now()):
        end_date = start_date + timedelta(weeks=-12)
        df = self.df[self.df['date'] > end_date]
        df = self.df[self.df['date'] < start_date]
        average_volume_3months = round(self.df['volume'].mean(),2)
        high_3months = round(self.df['high'].max())
        low_3months = round(self.df['low'].min())
        days_10 = start_date + timedelta(days=-12)
        df = self.df[self.df['date'] > end_date]
        average_volume_10days = round(self.df['volume'].mean(),2)
        print(average_volume_3months,'\n',high_3months,'\n',low_3months,'\n',average_volume_10days)




#----callbacks-----
#this will visualise the  historic data
@app.callback(Output(component_id='stock_price_history',component_property='children'),
            Input(component_id='search_box',component_property='value')
)

def visualation_update(value):
    # url = 'https://in.finance.yahoo.com/quote/{values}/key-statistics?p={values}'
    # url = url.format(values=value)
    # url = requests.get(url)
    # soup = bs4.BeautifulSoup(url.text,features='html.parser')
    # sph =[]
    # for i in ['95','102','109','116','123','130']:
    #     sph.append(soup.find_all('td',{'data-reactid':i})[0].text)
    # vm = pd.DataFrame(
    #     {
    #         'Stock Price History':['Beta (5Y monthly)','52-week change','S&P500 52-week change', '52-week high','52-week low','50 day moving average'],
    #         '':sph
    #     }
    # )
    a= analysis(value)
    vm = a.correlations()
    return dbc.Table.from_dataframe(vm)



@app.callback(Output(component_id='share_statistics',component_property='children'),
            Input(component_id='search_box',component_property='value')
)

def statistics_update(value):
    url = 'https://in.finance.yahoo.com/quote/{values}/key-statistics?p={values}'
    url = url.format(values=value)
    url = requests.get(url)
    soup = bs4.BeautifulSoup(url.text,features='html.parser')
    ss = []
    for i in ['151','158','165','172','179']:
        ss.append(soup.find_all('td',{'data-reactid':i})[0].text)

    sst = pd.DataFrame(
        {
            'Share statisctics' : ['Avg Vol(3 month)', 'Avg vol(10-day)','Shares outstanding', 'Float, % held by insiders', '% held by institutions'],
            '':ss
        }
    )
    return dbc.Table.from_dataframe(sst)


@app.callback(Output(component_id='hist_graph',component_property='figure'),
            Input(component_id='search_box',component_property='value'),
            Input(component_id='date_picker',component_property='start_date'),
            Input(component_id='date_picker',component_property='end_date'),
            Input(component_id='graph_select',component_property='value'),
            Input(component_id='technical_indicators_customization',component_property='value')
)

def hist_graph_update(value,start_date,end_date,custvalues,ddvalues):
    DATA_PATH = pathlib.Path(__file__).parent.joinpath('data')
    filename = '\\python_files\\stock\\data\\{}.xlsx'.format(value)
    df = pd.read_excel(filename)
    if start_date is not None:
        start_date1 = start_date
        print(start_date)
        df = df[df['date']>=start_date1]
    if end_date is not None:
        end_date1 = end_date
        print(end_date1)
        df = df[df['date']<=end_date1]

    ti = technical_indicators(df)
    df_ = ti.calculations()

    print('Technical selected ',ddvalues)
    count=1

    if 'APO' in ddvalues:
        count = count + 1
    if 'RSI' in ddvalues:
        count = count + 1
    if 'MACD' in ddvalues:
        count = count + 1
    if  'RSI' in ddvalues:
        count = count + 1
    if 'AROONOSC' in ddvalues:
        count = count + 1
    if 'MA' in ddvalues:
        count = count + 1
    if 'WMA' in ddvalues:
        count = count +1
    if 'CCI' in ddvalues:
        count = count +1
    if 'CMO' in ddvalues:
        count = count +1
    if 'T3' in ddvalues:
        count = count +1


    figure = make_subplots(shared_xaxes=True,vertical_spacing=0.0,rows=count,cols=1)
    i=1
    if 'APO' in ddvalues:
        figure.append_trace(go.Scatter(
                                name = 'Apo',
                                x = df_['date'],
                                y = df_['apo'],
                            )
        , row=i, col=1)
        figure.update_xaxes(showgrid=False,showticklabels=False,row=i,col=1)
        figure.update_yaxes(showgrid=False,range=[-30,30],row=i,col=1)
        i += 1

    if "RSI" in ddvalues:
        figure.append_trace(go.Scatter(
                                name = 'Rsi',
                                x = df_['date'],
                               y = df_['rsi'],
                           )
        , row=i , col=1)
        figure.update_xaxes(showgrid=False,showticklabels=False,row=i,col=1)
        figure.update_yaxes(showgrid=False,range=[0,100],row=i,col=1)
        i += 1

    if "MACD" in ddvalues:
        figure.append_trace(
                        go.Scatter(
                            name="macd",
                            x= df_['date'],
                            y=df_['macd'],
                        )
        ,row=i,col=1)
        figure.update_xaxes(showgrid=False,row=i,col=1)
        figure.update_yaxes(showgrid=False,row=i,col=1)
        i += 1

    if "AROONOSC" in ddvalues:
        figure.append_trace(
                        go.Scatter(
                            name="aroonosc",
                            x= df_['date'],
                            y=df_['aroonosc'],
                        )
        ,row=i,col=1)
        figure.update_xaxes(showgrid=False,row=i,col=1)
        figure.update_yaxes(showgrid=False,row=i,col=1)
        i += 1


    if "MA" in ddvalues:
        figure.append_trace(
                        go.Scatter(
                            name="ma",
                            x= df_['date'],
                            y=df_['ma'],
                        )
        ,row=i,col=1)
        figure.update_xaxes(showgrid=False,row=i,col=1)
        figure.update_yaxes(showgrid=False,row=i,col=1)
        i += 1

    if "T3" in ddvalues:
        figure.append_trace(
                        go.Scatter(
                            name="t3",
                            x= df_['date'],
                            y=df_['t3'],
                        )
        ,row=i,col=1)
        figure.update_xaxes(showgrid=False,row=i,col=1)
        figure.update_yaxes(showgrid=False,row=i,col=1)
        i += 1

    if "WMA" in ddvalues:
        figure.append_trace(
                        go.Scatter(
                            name="wma",
                            x= df_['date'],
                            y=df_['wma'],
                        )
        ,row=i,col=1)
        figure.update_xaxes(showgrid=False,row=i,col=1)
        figure.update_yaxes(showgrid=False,row=i,col=1)
        i += 1

    if "CCI" in ddvalues:
        figure.append_trace(
                        go.Scatter(
                            name="cci",
                            x= df_['date'],
                            y=df_['cci'],
                        )
        ,row=i,col=1)
        figure.update_xaxes(showgrid=False,row=i,col=1)
        figure.update_yaxes(showgrid=False,row=i,col=1)
        i += 1

    if "CMO" in ddvalues:
        figure.append_trace(
                        go.Scatter(
                            name="cmo",
                            x= df_['date'],
                            y=df_['cmo'],
                        )
        ,row=i,col=1)
        figure.update_xaxes(showgrid=False,row=i,col=1)
        figure.update_yaxes(showgrid=False,row=i,col=1)
        i += 1


    a=i
    if custvalues =='ln':
        figure.append_trace(go.Scatter(
            name='price',
            x=df_['date'],
            y=df_['open'],
        ),row=a,col=1)
    else:
        figure.append_trace(go.Candlestick(
            name='price',
            x=df_['date'],
            open=df_['open'], high=df_['high'],
            low=df_['low'], close=df_['close'],meta={'rangeselector':False,'rangeslider':{'visible':False}}
        ),row=a,col=1)

    if 'EMA' in ddvalues:
        figure.add_trace(go.Scatter(
                        name='Ema',
                        x = df_['date'],
                        y=df_['ema'],
        ),row=a,col=1)

    if 'SMA' in ddvalues:
        figure.add_trace(go.Scatter(
                        name='Sma',
                        x = df_['date'],
                        y=df_['sma'],
        ),row=a,col=1)

    if 'bbs' in ddvalues:
        figure.add_trace(go.Scatter(
                        name='upper',
                        x = df_['date'],
                        y=df_['upperband'],
        ),row=a,col=1)

        figure.add_trace(go.Scatter(
                        name='middle',
                        x = df_['date'],
                        y=df_['middleband'],
        ),row=a,col=1)

        figure.add_trace(go.Scatter(
                        name='lower',
                        x = df_['date'],
                        y=df_['lowerband'],
        ),row=a,col=1)
    figure.update_xaxes(showgrid=False,row=a,col=1)
    figure.update_yaxes(showgrid=False,row=a,col=1)

    figure.update_xaxes(rangeslider={'visible':False}, row=a, col=1)

    size_def = 10 - count


    figure.update_layout(height=5200/size_def,xaxis_rangeslider_visible=False,paper_bgcolor='#CCD7EA',plot_bgcolor = '#CCD7EA')
    figure.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            type="date"
        )
    )



    return figure
