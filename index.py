import dash
import datetime
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
from dash.dependencies import Input,Output
import time
from app import app
from apps import visualization,about_tech,about,historic_data,prediction,analysis
PLOTLY_LOGO = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0FcNqYbJ7ML8oWcV-NQHIREj5y2amoIZLqQ&usqp=CAU"

app.title = 'Stock Dashboard'
app.layout = html.Div([
                dcc.Location(id='url'),
                html.A([
                    dbc.NavbarSimple(children=[
                        dbc.NavItem(dbc.NavLink("Visualization", href="/visualization",style={'font-size':'25px','font-family':'nudista-web",Helvetica,Arial,sans-serif','color':'#000000','padding-right':'10px'}),),
                        dbc.NavItem(html.A(style={"font-size":"25px","text-align":"center","padding-right":"10px","padding-left":"10px"})),
                        dbc.NavItem(dbc.NavLink("Prediction", href="/prediction",style={'font-family':'nudista-web",Helvetica,Arial,sans-serif','color':'#000000'})),
                        dbc.NavItem(html.A(style={"font-size":"25px","text-align":"center","padding-right":"10px","padding-left":"10px"})),
                        dbc.NavItem(dbc.NavLink("Historic", href="/historic_data",style={'font-family':'nudista-web",Helvetica,Arial,sans-serif','color':'#000000'})),
                        dbc.NavItem(html.A(style={"font-size":"25px","text-align":"center","padding-right":"10px","padding-left":"10px"})),
                        dbc.NavItem(dbc.NavLink("About Technical Indicators", href="/technical_indicators",style={'font-family':'nudista-web",Helvetica,Arial,sans-serif','color':'#000000'})),
                        dbc.NavItem(html.A(style={"font-size":"25px","text-align":"center","padding-right":"10px","padding-left":"10px"})),
                        dbc.NavItem(dbc.NavLink("More Detail", href="/analysis",style={'font-family':'nudista-web",Helvetica,Arial,sans-serif','color':'#000000'})),
                        dbc.NavItem(html.A(style={"font-size":"25px","text-align":"center","padding-right":"10px","padding-left":"10px"})),
                    ],brand='Agilrio',brand_style={'font-size':'25px','font-family':'nudista-web",Helvetica,Arial,sans-serif'},expand='lg',fluid = True,className='purple-gradient',style={'font-size':'25px','font-family':'nudista-web",Helvetica,Arial,sans-serif','color':'#000000'}),
                ]),
                html.Br(),
                html.Div([
                    dbc.Row([
                        dbc.Col(html.H4('Search Ticker',style={'font-family':'nudista-web",Helvetica,Arial,sans-serif','font-size':'25px'}),width={'size':'auto'}),
                        dbc.Col( dcc.Dropdown(value='MSFT',searchable=True,placeholder='Enter Company name',id="search_box",options=[{'label':'TESLA','value' : 'TSLA'},
                                                                                                                                                    {'label':'INFOSYS','value' : 'INFY'},
                                                                                                                                                    {'label':'MICROSOFT','value' : 'MSFT'},
                                                                                                                                                    {'label':'APPLE','value' : 'AAPL'},
                                                                                                                                                {'label':'ABBOT','value' : 'ABT'},
                                                                                                                                                   {'label':'KODAK','value' : 'KODK'},
                                                                                                                                                   {'label':'TATA','value' : 'TTM'},
                                                                                                                                                   {'label':'STARBUCKS','value' : 'SBUX'},
                                                                                                                                                   {'label':'IBM','value' : 'IBM'},
                                                                                                                                                {'label':'FACEBOOK','value' : 'FB'},
                                                                                                                                                   {'label':'TWITTER','value' : 'TWTR'},
                                                                                                                                                   {'label':'AMD','value' : 'AMD'},
                                    ]),width={'size':3},
                                ),
                        dbc.Col(html.H4('Last updated Time',style={'font-size':'25px','font-family':'nudista-web",Helvetica,Arial,sans-serif'}),width={'size':'auto','offset':5}),
                        dbc.Col(html.H4(id="time_",style={'font-size':'25px'}),width={'size':'auto'}),
                        dcc.Interval(id="time_updated",interval=60000,n_intervals=0),
                    ],no_gutters=False)
                ],className="content"),
                html.Br(),
                html.Div([],id="page_content",className='ccontent'),

],className='hide_scroll')


@app.callback(Output("page_content","children"),Input("url","pathname"))
def render_page_content(pathname):
    if pathname == "/visualization":
        return visualization.layout
    elif pathname == "/prediction":
        return prediction.layout
    elif pathname == "/historic_data":
        return historic_data.layout
    elif pathname == "/about":
        return html.P("This is about")
    elif pathname == "/technical_indicators":
        return about_tech.layout
    elif pathname == "/analysis":
        return analysis.layout


    else:
        return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ])

@app.callback(Output("time_",'children'),
             Input("time_updated","n_intervals"))
def update(n):
    '''
    this function is for updating time
    '''
    value=datetime.datetime.now()
    value=value.strftime("%H:%M")
    value=str(value)
    print(value)
    return value

if __name__ == '__main__':
    app.run_server()
