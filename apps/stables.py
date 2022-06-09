
from itertools import accumulate
# from turtle import color
import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random



def app():
    
    page = st.container()
    


    query_id = "e9b9351a-7cfc-41a6-b217-d8f0d477424e"
    df_y = pd.read_json(
        f"https://api.flipsidecrypto.com/api/v2/queries/{query_id}/data/latest",
    convert_dates=["TIMESTAMP_NTZ"],
    )
    # page.write(df_y)
    # fig.add_trace(go.Candlestick(x=df['DAYZ'], open=df['MEDIAN(RATE)'], high=df['high'], low=df['MAX(RATE)'], close=df['MEDIAN(RATE)']) )
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                row_width=[0.2, 0.7])

    # include candlestick with rangeselector
    fig.add_trace(go.Candlestick(x=df_y['DAYZ'],open=df_y['MEDIAN(RATE)'], high=df_y['MAX(RATE)'],low=df_y['MIN(RATE)'], close=df_y['AVG(RATE)'],name="OHLC"), row=1, col=1)

    # include a go.Bar trace for volumes
    fig.add_trace(go.Bar(x=df_y['DAYZ'], y=df_y['SUM(USDT_IN)'],
                showlegend=False), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    page.plotly_chart(fig)


    page.write("https://ftx.com/api/markets/CUSDT-PERP/candles?resolution=14400")

    df = requests.get('https://ftx.com/api/markets/CUSDT-PERP/candles?resolution=14400').json()
    df = pd.DataFrame(df['result'])
    page.write("FTX cUSDT Perp")

    # st.write(df)
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                row_width=[0.2, 0.7])

    # include candlestick with rangeselector
    fig.add_trace(go.Candlestick(x=df['startTime'],open=df['open'], high=df['high'],low=df['low'], close=df['close'],name="OHLC"), row=1, col=1)

    # include a go.Bar trace for volumes
    fig.add_trace(go.Bar(x=df['startTime'], y=df['volume'],
                showlegend=False), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    page.plotly_chart(fig)



    page.write("https://ftx.com/api/markets/CUSDT/USDT/candles?resolution=14400")


    df = requests.get('https://ftx.com/api/markets/CUSDT/USDT/candles?resolution=14400').json()
    df = pd.DataFrame(df['result'])
    page.write("FTX cUSDT USDT")

    # st.write(df)
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                row_width=[0.2, 0.7])

    # include candlestick with rangeselector
    fig.add_trace(go.Candlestick(x=df['startTime'],open=df['open'], high=df['high'],low=df['low'], close=df['close'],name="OHLC"), row=1, col=1)

    # include a go.Bar trace for volumes
    fig.add_trace(go.Bar(x=df['startTime'], y=df['volume'],
                showlegend=False), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    page.plotly_chart(fig)





    page.write("https://ftx.us/api/markets/CUSDT/USDT/candles?resolution=144000")


    df = requests.get('https://ftx.us/api/markets/CUSDT/USDT/candles?resolution=14400').json()
    df = pd.DataFrame(df['result'])
    # st.write("FTX US cUSDT USDT")

    # page.write(df)
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                row_width=[0.2, 0.7])

    # include candlestick with rangeselector
    fig.add_trace(go.Candlestick(x=df['startTime'],open=df['open'], high=df['high'],low=df['low'], close=df['close'],name="OHLC"), row=1, col=1)

    # include a go.Bar trace for volumes
    fig.add_trace(go.Bar(x=df['startTime'], y=df['volume'],
                showlegend=False), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    page.plotly_chart(fig)







    page.write("https://ftx.us/api/markets/CUSDT/USD/candles?resolution=14400")


    df = requests.get('https://ftx.us/api/markets/CUSDT/USD/candles?resolution=14400').json()
    df = pd.DataFrame(df['result'])
    page.write("FTX US cUSDT USD")

    # st.write(df)

    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                row_width=[0.2, 0.7])

    # include candlestick with rangeselector
    fig.add_trace(go.Candlestick(x=df['startTime'],open=df['open'], high=df['high'],low=df['low'], close=df['close'],name="OHLC"), row=1, col=1)

    # include a go.Bar trace for volumes
    fig.add_trace(go.Bar(x=df['startTime'], y=df['volume'],
                showlegend=False), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    page.plotly_chart(fig)

    # page.write('https://ftx.com/api/markets/CUSDT/USDT/candles?resolution=14400&start_time=1623110400')


    # df = requests.get('https://ftx.com/api/markets/CUSDT/USDT/candles?resolution=14400&start_time=1623110400').json()

    # df = pd.DataFrame(df['result'])
    # page.write("FTX cUSDT USDT")
    # # page.write(df)
    # fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
    #             vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
    #             row_width=[0.2, 0.7])

    # # include candlestick with rangeselector
    # fig.add_trace(go.Candlestick(x=df['startTime'],open=df['open'], high=df['high'],low=df['low'], close=df['close'],name="OHLC"), row=1, col=1)

    # # include a go.Bar trace for volumes
    # fig.add_trace(go.Bar(x=df['startTime'], y=df['volume'],
    #             showlegend=False), row=2, col=1)

    # fig.update(layout_xaxis_rangeslider_visible=False)
    # page.plotly_chart(fig)
    
    page.write("https://ftx.us/api/markets/CUSDT/USD/candles?resolution=14400")

    df = requests.get('https://ftx.us/api/markets/CUSDT/USD/candles?resolution=14400').json()
    df = pd.DataFrame(df['result'])
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                row_width=[0.2, 0.7])

    # include candlestick with rangeselector
    fig.add_trace(go.Candlestick(x=df['startTime'],open=df['open'], high=df['high'],low=df['low'], close=df['close'],name="OHLC"), row=1, col=1)

    # include a go.Bar trace for volumes
    fig.add_trace(go.Bar(x=df['startTime'], y=df['volume'],
                showlegend=False), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    page.plotly_chart(fig)



    page.write("https://ftx.com/api/markets/USDT/USD/candles?resolution=14400")

    df = requests.get('https://ftx.com/api/markets/USDT/USD/candles?resolution=14400').json()
    df = pd.DataFrame(df['result'])
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                row_width=[0.2, 0.7])

    # include candlestick with rangeselector
    fig.add_trace(go.Candlestick(x=df['startTime'],open=df['open'], high=df['high'],low=df['low'], close=df['close'],name="OHLC"), row=1, col=1)

    # include a go.Bar trace for volumes
    fig.add_trace(go.Bar(x=df['startTime'], y=df['volume'],
                showlegend=False), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    page.plotly_chart(fig)





    page.write("https://ftx.us/api/markets/USDT/USD/candles?resolution=14400")

    df = requests.get('https://ftx.us/api/markets/USDT/USD/candles?resolution=14400').json()
    df = pd.DataFrame(df['result'])
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                row_width=[0.2, 0.7])

    # include candlestick with rangeselector
    fig.add_trace(go.Candlestick(x=df['startTime'],open=df['open'], high=df['high'],low=df['low'], close=df['close'],name="OHLC"), row=1, col=1)

    # include a go.Bar trace for volumes
    fig.add_trace(go.Bar(x=df['startTime'], y=df['volume'],
                showlegend=False), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    page.plotly_chart(fig)
    


























