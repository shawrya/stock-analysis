import datetime
import requests
import bs4
import re
import json
from bs4 import BeautifulSoup
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.graph_objs as go
import pandas as pd
import datetime as dt
import talib as ta
from plotly.subplots import make_subplots
from datetime import datetime
from pytz import timezone
from newsapi import NewsApiClient
from app import app
from dash.dependencies import Input, Output, State


layout = html.Div([
            html.Div([],id='company',),
            dcc.Interval(id='company_load',interval=10000,n_intervals=0),
            html.Br(),
            html.Div([
                dbc.Row([
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                html.Div([],id='company_table'),
                                dcc.Interval(id='company_table_update',interval=10000,n_intervals=0),
                            ]),
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                html.Div([],id='news_column'),
                            ]),
                        ]),
                    ],width={'size':3}),

                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.Div([
                                            dbc.Row([
                                                dbc.Col([
                                                    dcc.RadioItems(
                                                        id='graph_select',
                                                        options=[
                                                            {'label': 'Line', 'value': 'ln'},
                                                            {'label': 'Candlestick', 'value': 'cn'},
                                                        ],
                                                        value='ln',
                                                        labelStyle={'display': 'inline-block',"margin-right": "10px"}
                                                    )
                                                ],width={'offset':9}),
                                            ]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dcc.Graph(id='livegraph',figure={},),
                                                ]),
                                            ]),

                                        ]),
                                    ]),
                                ],style={'background-color':'#CCD7EA'}),
                            ]),
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.Div([
                                            html.H4('Technical Indicator',style={'padding-left':'35%'}),
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
                                                        multi = True,searchable=True,
                                            ),
                                            dcc.Graph(id='technical_graph',figure={})
                                        ]),
                                    ]),
                                ],style={'background-color':'#CCD7EA'}),
                            ]),
                        ]),
                    ],width={'size':6},),

                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        dbc.Row([
                                            dbc.Col([
                                                html.B('Trend Recommendation',style = {'font-size':'20px','font-family':'nudista-web",Helvetica,Arial,sans-serif'}),
                                                html.Br(),
                                            ],width={'offset':3}),
                                        ]),
                                        dbc.Row([
                                            dbc.Col([
                                                dcc.Graph(id='rating_graph',figure={},style={'height':'50px',}),
                                                html.Br(),
                                                dbc.Button('Info',color='primary',id='info_button'),
                                                dbc.Collapse([
                                                    html.Br(),
                                                    dbc.Card([
                                                        dbc.CardBody([
                                                            dbc.Row([
                                                                dbc.Col(html.H6('1-Strong Buy')),
                                                            ]),
                                                            dbc.Row([
                                                                dbc.Col(html.H6('2-Buy')),
                                                            ]),
                                                            dbc.Row([
                                                                dbc.Col(html.H6('3-Hold')),
                                                            ]),
                                                            dbc.Row([
                                                                dbc.Col(html.H6('4-under performance')),
                                                            ]),
                                                            dbc.Row([
                                                                dbc.Col(html.H6('5-Sell')),
                                                            ]),
                                                        ]),
                                                    ]),
                                                ],id='collapse'),
                                            ]),
                                        ]),


                                    ]),
                                ],style={'background-color':'#CCD7EA'}),
                            ],),
                        ]),

                        html.Br(),

                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        dbc.Row([
                                            dbc.Col([
                                                html.B('Valuation Measures',style = {'font-size':'20px','font-family':'nudista-web",Helvetica,Arial,sans-serif'})
                                            ],width={'offset':3}),
                                        ]),
                                        html.Br(),
                                        dbc.Row([
                                            dbc.Col([
                                                html.Div([

                                                ],id = 'valuation-measure'),
                                            ]),
                                        ]),
                                    ]),
                                ],style={'background-color':'#CCD7EA'}),
                            ]),
                        ]),

                        html.Br(),

                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        dbc.Row([
                                            dbc.Col([
                                                html.B('Company Description',style = {'font-size':'20px','font-family':'nudista-web",Helvetica,Arial,sans-serif'}),
                                            ],width={'offset':3}),

                                        ]),
                                        dbc.Row([
                                            dbc.Col([
                                                html.Br(),
                                                html.A(id="summary",style = {'font-family':'nudista-web",Helvetica,Arial,sans-serif'})
                                            ]),
                                        ]),

                                    ]),
                                ],id='summary_collapse',style={'background-color':'#CCD7EA'}),
                            ])
                        ]),

                        html.Br(),

                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        dbc.Row([
                                            dbc.Col([
                                                html.B('Key Executives',style = {'font-size':'20px','font-family':'nudista-web",Helvetica,Arial,sans-serif'}),
                                            ],width={'offset':4}),
                                        ]),
                                        dbc.Row([
                                            dbc.Col([
                                                html.Br(),

                                                html.Div(id='key-executives')
                                            ]),
                                        ]),

                                    ]),
                                ],style={'background-color':'#CCD7EA'}),
                            ]),
                        ]),


                    ]),
                ]),
            ],id='content'),
        ],className='background_colour')

#-----classes-----

class DataPulling:
    def __init__(self,ticker=None):
        url = 'https://finance.yahoo.com/quote/{tickers}?p={tickers}&.tsrc=fin-srch'
        self.url = url.format(tickers=ticker)


    def company_pull(self):
        '''
        This function takes the value from the sites and returns
        (
          apple_price,apple_change_rate,amazon_price,amazon_change_rate,
          microsoft_price,microsoft_change_rate,nasdaq_price,nasdaq_change_rate,
          apple_color_value,amazon_color_value,microsoft_color_value,nasdaq_color_value
        )
        '''
        apple_url = requests.get('https://in.finance.yahoo.com/quote/AAPL?p=AAPL')
        microsoft_url = requests.get('https://in.finance.yahoo.com/quote/MSFT?p=MSFT&.tsrc=fin-srch')
        amazon_url = requests.get('https://in.finance.yahoo.com/quote/AMZN?p=AMZN&.tsrc=fin-srch')
        nasdaq_url = requests.get('https://in.finance.yahoo.com/quote/NQ%3DF?p=NQ%3DF&.tsrc=fin-srch')
        soup=bs4.BeautifulSoup(apple_url.text,features="html.parser")
        apple_price=soup.find_all('div',{'class':'D(ib) Mend(20px)'})[0].find('span').text
        change_rate =soup.find_all('div',{'class':'D(ib) Mend(20px)'})[0]
        apple_change_rate = change_rate.find_all('span',{'data-reactid':'33'})[0].text
        soup=bs4.BeautifulSoup(microsoft_url.text,features="html.parser")
        microsoft_price=soup.find_all('div',{'class':'D(ib) Mend(20px)'})[0].find('span').text
        change_rate =soup.find_all('div',{'class':'D(ib) Mend(20px)'})[0]
        microsoft_change_rate = change_rate.find_all('span',{'data-reactid':'33'})[0].text
        soup=bs4.BeautifulSoup(amazon_url.text,features="html.parser")
        amazon_price=soup.find_all('div',{'class':'D(ib) Mend(20px)'})[0].find('span').text
        amazon_rate =soup.find_all('div',{'class':'D(ib) Mend(20px)'})[0]
        amazon_change_rate = change_rate.find_all('span',{'data-reactid':'33'})[0].text
        soup=bs4.BeautifulSoup(nasdaq_url.text,features="html.parser")
        nasdaq_price=soup.find_all('div',{'class':'D(ib) Mend(20px)'})[0].find('span').text
        nasdaq_rate =soup.find_all('div',{'class':'D(ib) Mend(20px)'})[0]
        nasdaq_change_rate = change_rate.find_all('span',{'data-reactid':'33'})[0].text
        if '-' in apple_change_rate:
            apple_color_value = '#FD0E35'
        else:
            apple_color_value = '#00b300'
        if '-' in microsoft_change_rate:
            microsoft_color_value = '#FD0E35'
        else:
            microsoft_color_value = '#00b300'
        if '-' in amazon_change_rate:
            amazon_color_value = '#FD0E35'
        else:
            amazon_color_value = '#00b300'
        if '-' in nasdaq_change_rate:
            nasdaq_color_value = '#FD0E35'
        else:
            nasdaq_color_value = '#009900'
        return (apple_price,apple_change_rate,amazon_price,amazon_change_rate,microsoft_price,microsoft_change_rate,nasdaq_price,nasdaq_change_rate,apple_color_value,amazon_color_value,microsoft_color_value,nasdaq_color_value)

    def company_values(self,ticker):
        url_ = 'https://in.finance.yahoo.com/quote/{values}?p={values}&.tsrc=fin-srch'
        url = url_.format(values=ticker)
        url = requests.get(url)
        soup=bs4.BeautifulSoup(url.text,features="html.parser")
        price=soup.find_all('div',{'class':'D(ib) Mend(20px)'})[0].find('span').text
        change_rate =soup.find_all('div',{'class':'D(ib) Mend(20px)'})[0]
        change_rate = change_rate.find_all('span',{'data-reactid':'33'})[0].text
        day_range = soup.find_all('td',{'data-test':'DAYS_RANGE-value'})[0].text
        market_cap = soup.find_all('td',{'data-test':'MARKET_CAP-value'})[0].find('span').text
        pe_ratio = soup.find_all('td',{'data-test':'PE_RATIO-value'})[0].find('span').text
        forward_divident_yield = soup.find_all('td',{'data-test':'DIVIDEND_AND_YIELD-value'})[0].text
        volumne=soup.find_all('td',{'data-test':"TD_VOLUME-value"})[0].find('span').text
        if '-' in change_rate:
            color_value = '#cc2900'
        else:
            color_value = '#009900'

        return (price,change_rate,day_range,market_cap,pe_ratio,forward_divident_yield,volumne,color_value)

    def live_data(self):
        url = requests.get(self.url)
        soup=bs4.BeautifulSoup(url.text,features="html.parser")
        price=soup.find_all('div',{'class':'D(ib) Mend(20px)'})[0].find('span').text
        if ',' in price:
            price = float(price.replace(',',''))
        return price

    def get_Volumne(self):
        url = requests.get(self.url)
        soup=bs4.BeautifulSoup(url.text,features="html.parser")
        volumne=soup.find_all('td',{'data-test':"TD_VOLUME-value"})[0].find('span').text
        volumne = float(volumne.replace(',',''))
        return volumne

    def get_rating(self):
        url = requests.get(self.url)
        soup = bs4.BeautifulSoup(url.text,features='html.parser')
        pattern = re.compile(r'\s--\sData\s--\s')
        script_data = soup.find('script',text=pattern).contents[0]
        start = script_data.find('context')-2
        json_data = json.loads(script_data[start:-12])
        a1 = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['recommendationTrend']['trend']
        a3 = a1[0]
        del a3['period']
        a4 = max(a3,key = lambda x: a3[x])
        if a4 == 'strongBuy':
            value = 4
        elif a4 == 'buy':
            value = 2
        elif a4 == 'hold':
            value = 3
        elif a4 == 'sell':
            value = 4
        elif a4 == 'strongSell':
            value = 5
        return value


    def get_summary(self):
        url = requests.get(self.url)
        soup = bs4.BeautifulSoup(url.text,features='html.parser')
        pattern = re.compile(r'\s--\sData\s--\s')
        script_data = soup.find('script',text=pattern).contents[0]
        start = script_data.find('context')-2
        json_data = json.loads(script_data[start:-12])
        summary= json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryProfile']['longBusinessSummary']
        return summary



class news_grabber:
    def __init__(self):
        self.api_key='d5215a048a894c8497df641e9f8ad76e'
        self.newsapi = NewsApiClient(api_key=self.api_key)

    def get_news(self,company_name):
        self.data = self.newsapi.get_everything(q=company_name,language='en',sort_by='relevancy',page=2)
        self.results = self.data['articles'].copy()
        self.news_df = pd.DataFrame(self.results)
        return self.news_df


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





#----all callbacks----
@app.callback(Output(component_id='company',component_property='children'),
            [Input(component_id='company_load',component_property='n_interval')]
)
def update(n):
    '''
    This function is called after every 10 seconds to refresh the company cards
    '''
    c = DataPulling()
    apple_price,apple_change_rate,amazon_price,amazon_change_rate,microsoft_price,microsoft_change_rate,nasdaq_price,nasdaq_change_rate,apple_color_value,amazon_color_value,microsoft_color_value,nasdaq_color_value = c.company_pull()
    company_card = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.I(className="fab fa-apple",style={"font-size":"50px"}),
                        ],width=2),
                        dbc.Col([
                            html.H1('Apple',style={'text-align':'bottom'},className='text_color_blue'),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Br(),
                            html.H2('$ '+apple_price,className='text_color_blue'),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.H4(apple_change_rate,className='text_color_blue'),
                        ]),
                    ]),
                ])
            ],className='card_background',inverse=True)
        ],width={"size":3}),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.I(className="fab fa-amazon",style={"font-size":"50px"}),
                        ],width=2),
                        dbc.Col([
                            html.H2('Amazon',style={'text-align':'bottom'},className='text_color_blue'),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Br(),
                            html.H2('$ '+amazon_price,className='text_color_blue'),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.H4(amazon_change_rate,className='text_color_blue'),
                        ]),
                    ]),
                ])
            ],className='card_background',inverse=True)
        ],width={"size":3}),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.I(className="fab fa-microsoft",style={"font-size":"50px"}),
                        ],width=2),
                        dbc.Col([
                            html.H2('Microsoft',style={'text-align':'bottom'},className='text_color_blue'),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Br(),
                            html.H2('$ '+microsoft_price,className='text_color_blue'),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.H4(microsoft_change_rate,className='text_color_blue'),
                        ]),
                    ]),
                ])
            ],className='card_background',inverse=True)
        ],width={"size":3}),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.I(className="fas fa-chart-line",style={"font-size":"50px"}),
                        ],width=2),
                        dbc.Col([
                            html.H2('Nasdaq',style={'text-align':'bottom'},className='text_color_blue'),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Br(),
                            html.H2('$ '+nasdaq_price,className='text_color_blue'),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.H4(nasdaq_change_rate,className='text_color_blue'),
                        ]),
                    ]),
                ])
            ],className='card_background',inverse=True)
        ],width={"size":3}),
    ]),
    return company_card

@app.callback(Output(component_id="company_table",component_property="children"),
            [Input(component_id="company_table_update",component_property="n_intervals"),
            Input(component_id="search_box",component_property="value")])

def update(n,v):
    '''
    this function is used to present opening, closing and many other values
    '''
    c2 = DataPulling()
    price,change_rate,day_range,market_cap,pe_ratio,forward_divident_yield,volumne,color_value = c2.company_values(v)

    company_values = dbc.Card([
        dbc.CardBody([
            dbc.Row(
                dbc.Col(
                    html.H3('Key Data',className='keydata_font'),
                    width={'size':'auto','offset':3}
                )
            ),
            dbc.Row([
                dbc.Col([html.Br()])
            ]),
            dbc.Row([
                dbc.Col([html.H5('Open',className='keydata_font')]),
                dbc.Col(html.H5(price,style={'color':color_value})),
            ],justify="between",),
            dbc.Row([
                dbc.Col([html.H5('Change Rate',className='keydata_font')]),
                dbc.Col(html.H5(change_rate,style={'color':color_value})),
            ],justify="between"),
            dbc.Row([
                dbc.Col([html.H5('Day Range',className='keydata_font')]),
                dbc.Col(html.H5(day_range,className='keydata_font')),
            ],justify="between"),
            dbc.Row([
                dbc.Col([html.H5('Market Cap',className='keydata_font')]),
                dbc.Col(html.H5(market_cap,className='keydata_font')),
            ],justify="between"),
            dbc.Row([
                dbc.Col([html.H5('PE Ratio',className='keydata_font')]),
                dbc.Col(html.H5(pe_ratio,className='keydata_font')),
            ],justify="between"),
            dbc.Row([
                dbc.Col([html.H5('Forward divident yield',className='keydata_font')]),
                dbc.Col(html.H5(forward_divident_yield,className='keydata_font')),
            ],justify="between"),
            dbc.Row([
                dbc.Col([html.H5('Volumne',className='keydata_font')]),
                dbc.Col(html.H5(volumne,className='keydata_font')),
            ],justify="between"),
        ]),
    ],style={'width':'90%','background-color':'#CCD7EA'})
    return company_values



@app.callback(Output(component_id='news_column',component_property='children'),
            [Input(component_id="search_box",component_property="value")]
)
def nes_update(value):
    '''
    this function returns news as per the company value in the search box
    '''
    values = value.upper()
    if(values in ['AAPL','MSFT','TSLA','ABBT','AMD','FB','IBM','INFY','KODK','SBUCKS','TSLA','TATA','TWTR']):
        a1=news_grabber()
        news_dataframe = a1.get_news(company_name=f'{values}')
        news_dataframe =news_dataframe['title']
        a1 = news_dataframe.to_numpy()
        a1 = a1[:18]
        company = f'{values}'
        news_dataframe1 = pd.DataFrame({"News related to "+company:a1})
    else:
        dash.no_update
    return dbc.Card([
            dbc.CardBody([
                dbc.Table.from_dataframe(news_dataframe1,style={'font-family':'nudista-web",Helvetica,Arial,sans-serif','color':'black'})
            ])
    ],style={'width':'90%','background-color':'#CCD7EA'})

datetime_ = []
open_ = []
close = []
high = []
low = []
volume =[]
@app.callback(Output(component_id='livegraph',component_property='figure'),
            Input(component_id='search_box',component_property='value'),
            Input(component_id='company_table_update',component_property='n_intervals'),
            Input(component_id='graph_select',component_property='value')
)
def livegraph(value,n,se):
    '''
    live price updation code
    '''
    ll = DataPulling(ticker=value)
    america = timezone('US/Eastern')
    sa_time = datetime.now(america)
    close.append(float(ll.live_data()))
    if len(close)!=1:
        open_.append(close[-2])
    else:
        open_.append(close[-1])
    datetime_.append(sa_time.strftime('%H:%M:%S'))
    high.append(max(close))
    low.append(min(close))
    volume.append(ll.get_Volumne())
    print('open',open_)
    print('close',close)
    print('low',low)
    print('high',high)
    print('datetime',datetime_)
    print('live graph update')
    if se =='ln':
        figure = go.Figure(data=[
                            go.Scatter(
                                x=datetime_,
                                y=open_,
                                mode='lines'
                            )
        ],layout=go.Layout(xaxis={'title':'Time','showgrid':False,'tickfont':{'family':'nudista-web",Helvetica,Arial,sans-serif','size':15}},
                           yaxis={'title':'Dollars','showgrid':False,'tickfont':{'family':'nudista-web",Helvetica,Arial,sans-serif','size':15}},
                           title = 'Live Graph',
                           titlefont={'family':'nudista-web",Helvetica,Arial,sans-serif','size':30},
                           paper_bgcolor='#CCD7EA',
                           plot_bgcolor = '#CCD7EA'

        ))
        figure.update_layout(template="seaborn",margin=dict(l=2,r=2,b=5))
    else :
        figure  = go.Figure(data=[
                            go.Candlestick(
                                x= datetime_,
                                open=open_,
                                close=close,
                                high = high,
                                low = low,
                            ),

        ],layout=go.Layout(xaxis={'title':'Time','showgrid':True,'tickfont':{'family':'nudista-web",Helvetica,Arial,sans-serif','size':15}},
                           yaxis={'title':'Dollars','showgrid':True,'tickfont':{'family':'nudista-web",Helvetica,Arial,sans-serif','size':15}},
                           title = 'Live Graph',
                           titlefont={'family':'nudista-web",Helvetica,Arial,sans-serif','size':30},
                           paper_bgcolor='#CCD7EA',
                           plot_bgcolor = '#CCD7EA'

        ))
        figure.update_layout(template="seaborn",margin=dict(l=2,r=2,b=5))



    return figure


@app.callback(Output(component_id='technical_graph',component_property='figure'),
            [Input(component_id='technical_indicators_customization',component_property='value'),
            Input(component_id='company_table_update',component_property='n_intervals'),
            ]
)
def update12(value,n):
    '''
    this function is used to update the rating
    '''
    print(value)
    if len(open_) >= 5:
        df = pd.DataFrame({
            'date':datetime_,
            'open':open_,
            'close':close,
            'high':high,
            'low':low,
            'volume':volume
        })
        df.drop_duplicates(subset=['date'],inplace=True)
        t1 = technical_indicators(df)
        df_1= t1.calculations()



        print(df_1)

        count=1

        if 'APO' in value:
            count = count + 1
        if 'RSI' in value:
            count = count + 1
        if 'MACD' in value:
            count = count + 1
        if  'RSI' in value:
            count = count + 1

        print('time',df_1['date'])
        figure = make_subplots(shared_xaxes=True,vertical_spacing=0.0,rows=count,cols=1)
        i=1
        if 'APO' in value:
            figure.append_trace(go.Scatter(
                                    name = 'Apo',
                                    x = df_1['date'],
                                    y = df_1['apo'],
                                )
            , row=i, col=1)
            figure.update_xaxes(showgrid=False,showticklabels=False,row=i,col=1)
            figure.update_yaxes(showgrid=False,range=[-30,30],row=i,col=1)
            i += 1

        if "RSI" in value:
            figure.append_trace(go.Scatter(
                                    name = 'Rsi',
                                    x = df_1['date'],
                                   y = df_1['rsi'],
                               )
            , row=i , col=1)
            figure.update_xaxes(showgrid=False,showticklabels=False,row=i,col=1)
            figure.update_yaxes(showgrid=False,range=[0,100],row=i,col=1)
            i += 1

        if "MACD" in value:
            figure.append_trace(
                            go.Scatter(
                                name="macd",
                                x= df_1['date'],
                                y=df_1['macd'],
                            )
            ,row=i,col=1)
            figure.update_xaxes(showgrid=False,row=i,col=1)
            figure.update_yaxes(showgrid=False,row=i,col=1)
            i += 1


        a=i

        figure.append_trace(go.Scatter(
            name='price',
            x=df_1['date'],
            y=df_1['open'],
        ),row=a,col=1)


        if 'EMA' in value:
            figure.add_trace(go.Scatter(
                            name='Ema',
                            x = df_1['date'],
                            y=df_1['ema'],
            ),row=a,col=1)

        if 'SMA' in value:
            figure.add_trace(go.Scatter(
                            name='Sma',
                            x = df_1['date'],
                            y=df_1['sma'],
            ),row=a,col=1)

        if 'bbs' in value:
            figure.add_trace(go.Scatter(
                            name='upper',
                            x = df_1['date'],
                            y=df_1['upperband'],
            ),row=a,col=1)

            figure.add_trace(go.Scatter(
                            name='middle',
                            x = df_1['date'],
                            y=df_1['middleband'],
            ),row=a,col=1)

            figure.add_trace(go.Scatter(
                            name='lower',
                            x = df_1['date'],
                            y=df_1['lowerband'],
            ),row=a,col=1)
        figure.update_xaxes(showgrid=False,row=a,col=1)
        figure.update_yaxes(showgrid=False,row=a,col=1)

        figure.update_xaxes(rangeslider={'visible':False}, row=a, col=1)

        size_def = 5 - count


        figure.update_layout(height=1200/size_def,xaxis_rangeslider_visible=False,paper_bgcolor='#CCD7EA',plot_bgcolor = '#CCD7EA')


        return figure

    else:
        figure={}
        return figure


@app.callback(
    Output("collapse", "is_open"),
    [Input("info_button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    '''
    this function is used to open collapse bar
    '''
    if n:
        return not is_open
    return is_open



@app.callback(Output(component_id='rating_graph',component_property='figure'),
            [Input(component_id='search_box',component_property='value')]
)
def update_ratting(value):
    d1 = DataPulling(value)
    val1 = d1.get_rating()
    print(val1)
    fig = go.Figure(go.Bar(
                            x=[val1],
                            y=['rating'],
                            orientation='h'
                        )
                )
    fig.update_layout(
        margin = dict(l=10,r=10,t=10,b=10),
    )
    fig.update_xaxes(scaleratio=1,range=[1,5])
    return fig


@app.callback(Output(component_id="summary",component_property="children"),
            [Input(component_id="search_box",component_property="value")]
)
def update_summary(value):
    d1 = DataPulling(value)
    val1 = d1.get_summary()
    i = 0
    _ = 0
    while _ != 4:
        if val1[i] == '.':
            i = i + 1
            _ = _ + 1
        else:
            i = i + 1
    print("i=",i)
    val1 = val1[:i]
    return val1

@app.callback(Output(component_id='key-executives',component_property='children'),
            Input(component_id='search_box',component_property='value')
)
def update_executives(value):
    if value=='AAPL':
        info = pd.DataFrame(
            {
                'Name' :['Jeffrey E. Williams','Kevin M. Lynch','Luca Maestri','Timothy Donald Cook'],
                'Title' :['Chief Operating Officer','Vice President-Technology','Chief Financial Officer & Senior Vice President','Chief Executive Officer & Director']
            }
        )
    elif value == 'MSFT':
        info = pd.DataFrame(
            {
                'Name' :['Amy E. Hood','Bill Duff',"David M. O'Hara",'James Kevin Scott',"Kirk Koenigsbauer","Satya Nadella"],
                'Title' :['Chief Financial Officer & Executive Vice President', 'CFO-Operating Systems Group','Chief Financial Officer-Online Services Division','Chief Technology Officer & Executive VP','COO & VP-Experiences & Devices Group','Chief Executive Officer & Non-Independent Director']
            }
        )
    elif value == 'TSLA':
        info = pd.DataFrame(
            {
                'Name' :['Elon Reeve Musk'],
                'Title' :['Technoking of Tesla']
            }
        )
    elif value == 'INFY':
        info = pd.DataFrame(
            {
                'Name' :['Anand Swaminathan','Jayesh Sanghrajka','Nilanjan Roy','Ravi Kumar S.','Salil S.','U. B. Pravin Rao'],
                'Title' :['Executive VP-Communications, Media & Technology','Executive VP & Deputy Chief Financial Officer','Co-President & Deputy Chief Operating Officer','Executive Officer', 'MD & Executive Director','Chief Operating Officer & Executive Director']
            }
        )

    else:
        info = pd.DataFrame(
            {
                'Name' :['Amy E. Hood','Bill Duff',"David M. O'Hara",'James Kevin Scott',"Kirk Koenigsbauer","Satya Nadella"],
                'Title' :['Chief Financial Officer & Executive Vice President', 'CFO-Operating Systems Group','Chief Financial Officer-Online Services Division','Chief Technology Officer & Executive VP','COO & VP-Experiences & Devices Group','Chief Executive Officer & Non-Independent Director']
            }
        )

    return dbc.Table.from_dataframe(info)
@app.callback(Output(component_id='valuation-measure',component_property='children'),
            Input(component_id='search_box',component_property='value')
)

def visualation_update(value):
    url = 'https://in.finance.yahoo.com/quote/{values}/key-statistics?p={values}'
    url = url.format(values=value)
    url = requests.get(url)
    soup = bs4.BeautifulSoup(url.text,features='html.parser')
    bea =[]
    for i in ['21','28','35','42','49','56','63','70','77']:
        bea.append(soup.find_all('td',{'data-reactid':i})[0].text)
    vm = pd.DataFrame(
        {
            'Valuations':['Market Cap','Enterprise Value','Trailing P/E','Forward P/E','PEG Ratio','Price/sale(ttm)','Price/Book(mrq)','Enterprise Value/Revenue','Enterprise Value'],
            '':bea
        }
    )
    return dbc.Table.from_dataframe(vm),
