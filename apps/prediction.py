import dash
import keras
import pickle
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from keras.models import Sequential
from keras.layers import Dense,LSTM
from dash.dependencies import Input,Output
from app import app
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense,LSTM
import keras
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import math


layout = html.Div([
            html.Div([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div(id='o_p')
                            ]),
                        ],style={'background-color':'#CCD7EA'}),
                    ],width={'size':4}),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Loading(children=[dcc.Graph(id='o_p_graph',figure=go.Figure({

                                }))],type='graph',fullscreen=True),
                                html.Div([
                                    html.H1(id='tom_value')
                                ])
                            ]),
                        ],style={'background-color':'#CCD7EA'}),
                    ],width={'size':8}),
                ]),
            ]),
])


@app.callback(Output(component_id="o_p",component_property="children")
            ,Input(component_id="search_box",component_property="value"))

def model_load(value):
    apple_model = keras.models.load_model(r".\machinelearning_models\apple_model.h5")
    amd_model = keras.models.load_model(r".\machinelearning_models\amd_model.h5")
    facebook_model = keras.models.load_model(r".\machinelearning_models\facebook_model.h5")
    ibm_model = keras.models.load_model(r".\machinelearning_models\IBM_model.h5")
    infy_model = keras.models.load_model(r".\machinelearning_models\infy_model.h5")
    kodk_model = keras.models.load_model(r".\machinelearning_models\kodk_model.h5")
    msft_model = keras.models.load_model(r".\machinelearning_models\msft_model.h5")
    sbux_model = keras.models.load_model(r".\machinelearning_models\sbux_model.h5")
    tsla_model = keras.models.load_model(r".\machinelearning_models\tsla_model.h5")
    ttm_model = keras.models.load_model(r".\machinelearning_models\ttm_model.h5")
    twtr_model = keras.models.load_model(r".\machinelearning_models\twtr_model.h5")
    value = value.upper()
    if value == "AAPL":
        model = apple_model
    if value == "AMD":
        model = amd_model
    if value == "FB":
        model = facebook_model
    if value == "IBM":
        model = ibm_model
    if value == "INFY":
        model = infy_model
    if value == "KODK":
        model = kodk_model
    if value == "MSFT":
        model = msft_model
    if value == "SBUX":
        model = sbux_model
    if value == "TSLA":
        model = tsla_model
    if value == "TTM":
        model =ttm_model
    if value == "TWTR":
        model = twtr_model


    df = pd.read_excel(f".\\data\\{value}.xlsx")
    data = df.filter(["close"])
    dataset = data.values
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)
    training_data_len=math.ceil(len(dataset)*0.8)
    print(training_data_len)

    train_data=scaled_data[0:training_data_len,:]
    x_train =[]
    y_train =[]
    for i in range(70,len(train_data)):
        x_train.append(train_data[i-70:i,0])
        y_train.append(train_data[i,0])
        if i<=70:
            print(x_train)
            print(y_train)

    test_data=scaled_data[training_data_len-70:,:]
    x_test=[]
    y_test=dataset[training_data_len:,:]
    for i in range(70,len(test_data)):
        x_test.append(test_data[i-70:i,0])

    x_train = np.array(x_train)
    y_train = np.array(y_train)
    x_test=np.array(x_test)
    x_test=np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))

    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    print(predictions)




    valid = data[training_data_len:]
    valid["prediction"] = predictions
    df_c = len(df)
    _ = len(valid)
    c15 = _ - 15
    valid = valid[c15:]
    df_cal = df_c - 15
    dff = df[df_cal:]
    valid['date'] = dff['date'].dt.date
    print("all models loaded")
    return  dbc.Table.from_dataframe(valid, style={"font-size":"15px"})




@app.callback(Output(component_id="o_p_graph",component_property="figure")
            ,Input(component_id="search_box",component_property="value"))

def model_load1(value):
    apple_model = keras.models.load_model(r".\machinelearning_models\apple_model.h5")
    amd_model = keras.models.load_model(r".\machinelearning_models\amd_model.h5")
    facebook_model = keras.models.load_model(r".\machinelearning_models\facebook_model.h5")
    ibm_model = keras.models.load_model(r".\machinelearning_models\IBM_model.h5")
    infy_model = keras.models.load_model(r".\machinelearning_models\infy_model.h5")
    kodk_model = keras.models.load_model(r".\machinelearning_models\kodk_model.h5")
    msft_model = keras.models.load_model(r".\machinelearning_models\msft_model.h5")
    sbux_model = keras.models.load_model(r".\machinelearning_models\sbux_model.h5")
    tsla_model = keras.models.load_model(r".\machinelearning_models\tsla_model.h5")
    ttm_model = keras.models.load_model(r".\machinelearning_models\ttm_model.h5")
    twtr_model = keras.models.load_model(r".\machinelearning_models\twtr_model.h5")
    value = value.upper()
    if value == "AAPL":
        model = apple_model
    if value == "AMD":
        model = amd_model
    if value == "FB":
        model = facebook_model
    if value == "IBM":
        model = ibm_model
    if value == "INFY":
        model = infy_model
    if value == "KODK":
        model = kodk_model
    if value == "MSFT":
        model = msft_model
    if value == "SBUX":
        model = sbux_model
    if value == "TSLA":
        model = tsla_model
    if value == "TTM":
        model =ttm_model
    if value == "TWTR":
        model = twtr_model


    df = pd.read_excel(f".\\data\\{value}.xlsx")
    data = df.filter(["close"])
    dataset = data.values
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)
    training_data_len=math.ceil(len(dataset)*0.8)
    print(training_data_len)

    train_data=scaled_data[0:training_data_len,:]
    x_train =[]
    y_train =[]
    for i in range(70,len(train_data)):
        x_train.append(train_data[i-70:i,0])
        y_train.append(train_data[i,0])
        if i<=70:
            print(x_train)
            print(y_train)

    test_data=scaled_data[training_data_len-70:,:]
    x_test=[]
    y_test=dataset[training_data_len:,:]
    for i in range(70,len(test_data)):
        x_test.append(test_data[i-70:i,0])

    x_train = np.array(x_train)
    y_train = np.array(y_train)
    x_test=np.array(x_test)
    x_test=np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))

    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    print(predictions)




    valid = data[training_data_len:]
    valid["prediction"] = predictions
    df_date = pd.read_excel(f".\\data\\{value}.xlsx")
    df_date = df_date.filter(['date'])
    df_date = df_date[training_data_len:]
    valid['date'] = df_date
    df_c = len(df)
    _ = len(valid)
    c15 = _ - 15
    valid = valid[c15:]
    print("all models loaded")

    print('valid columns',valid.columns)

    df1 = pd.read_excel(f".\\data\\{value}.xlsx")

    figure = make_subplots(shared_yaxes=True,shared_xaxes=True,vertical_spacing=0.0,rows=1,cols=1)

    figure.append_trace(go.Scatter(
                            name = 'Actual Values',
                            x = valid['date'],
                            y = valid['close']
                                    )
           , row=1,col=1)

    figure.append_trace(go.Scatter(
                            name = 'Predicted values',
                            x = valid['date'],
                            y = valid['prediction']
                                    )
           , row=1,col=1)


    figure.update_layout(xaxis_rangeslider_visible=False,paper_bgcolor='#CCD7EA',plot_bgcolor = '#CCD7EA')
    return  figure

@app.callback(Output(component_id="tom_value",component_property="children")
            ,Input(component_id="search_box",component_property="value"))

def y_func(value):
    apple_model = keras.models.load_model(r".\machinelearning_models\apple_model.h5")
    amd_model = keras.models.load_model(r".\machinelearning_models\amd_model.h5")
    facebook_model = keras.models.load_model(r".\machinelearning_models\facebook_model.h5")
    ibm_model = keras.models.load_model(r".\machinelearning_models\IBM_model.h5")
    infy_model = keras.models.load_model(r".\machinelearning_models\infy_model.h5")
    kodk_model = keras.models.load_model(r".\machinelearning_models\kodk_model.h5")
    msft_model = keras.models.load_model(r".\machinelearning_models\msft_model.h5")
    sbux_model = keras.models.load_model(r".\machinelearning_models\sbux_model.h5")
    tsla_model = keras.models.load_model(r".\machinelearning_models\tsla_model.h5")
    ttm_model = keras.models.load_model(r".\machinelearning_models\ttm_model.h5")
    twtr_model = keras.models.load_model(r".\machinelearning_models\twtr_model.h5")
    value = value.upper()
    if value == "AAPL":
        model = apple_model
    if value == "AMD":
        model = amd_model
    if value == "FB":
        model = facebook_model
    if value == "IBM":
        model = ibm_model
    if value == "INFY":
        model = infy_model
    if value == "KODK":
        model = kodk_model
    if value == "MSFT":
        model = msft_model
    if value == "SBUX":
        model = sbux_model
    if value == "TSLA":
        model = tsla_model
    if value == "TTM":
        model =ttm_model
    if value == "TWTR":
        model = twtr_model
    df = pd.read_excel(f".\\data\\{value}.xlsx")
    data = df.filter(["close"])
    dataset = data.values
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)
    scaled_data = scaled_data[-100:,:]
    x_test = []
    for i in range(70,len(scaled_data)):
        x_test.append(scaled_data[i-70:i,0])
    x_test = np.array(x_test)
    x_test=np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    predictions = predictions[-16][0]
    print(predictions)
    message = f"Tommorow's price would be {predictions}"
    return message
