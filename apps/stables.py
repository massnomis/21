
from itertools import accumulate
from turtle import color
import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random



def app():
    page = st.container()

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

    # asdfasdfasdfasdf = px.line(
    #     df, #this is the dataframe you are trying to plot
    #     x = "startTime",
    #     y = ['high','low', 'open','close'],
    #     color = 'volume'
    # )
    # page.plotly_chart(asdfasdfasdfasdf)

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
    # dfCUSDT = px.line(
    #     df, #this is the dataframe you are trying to plot
    #     x = "startTime",
    #     y = ['high','low', 'open','close'],
    #     color = 'volume'
    # )
    # page.plotly_chart(dfCUSDT)

    df = requests.get('https://ftx.us/api/markets/CUSDT/USDT/candles?resolution=14400').json()
    df = pd.DataFrame(df['result'])
    # st.write("FTX US cUSDT USDT")

    page.write(df)
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
    # dfCUSDTU = px.line(
    #     df, #this is the dataframe you are trying to plot
    #     x = "startTime",
    #      y = ['high','low', 'open','close'],
    #     color = 'volume'
    # )
    # page.plotly_chart(dfCUSDTU)

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



    query_id = "e9b9351a-7cfc-41a6-b217-d8f0d477424e"
    df_y = pd.read_json(
        f"https://api.flipsidecrypto.com/api/v2/queries/{query_id}/data/latest",
    convert_dates=["TIMESTAMP_NTZ"],
    )
    page.write(df_y)
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
    # df_y = px.line(
    #     df_y, #this is the dataframe you are trying to plot
    #     x = "DAYZ",
    #     y = ['MIN(RATE)','MAX(RATE)','AVG(RATE)','MEDIAN(RATE)'],
    #     color = 'SUM(CTOKEN_OUT)'

    # )
    # page.plotly_chart(df_y)

    # df = requests.get('https://ftx.com/api/markets/CUSDT/USDT/candles?resolution=86400&start_time=1623110400').json()

    # df = pd.DataFrame(df['result'])
    # page.write("FTX cUSDT USDT")

    # # st.write(df)

    # df = px.scatter(
    #     df, #this is the dataframe you are trying to plot
    #     x = "startTime",
    #     y = ['open','close','high','low']
    # )
    # page.plotly_chart(df)

    # df = requests.get('https://ftx.com/api/markets/USDT/USD/candles?resolution=86400&start_time=1623110400').json()

    # df = pd.DataFrame(df['result'])
    # page.write("FTX USDT USD")

    # # st.write(df)

    # df = px.scatter(
    #     df, #this is the dataframe you are trying to plot
    #     x = "startTime",
    #     y = ['open','close','high','low']
    # )
    # page.plotly_chart(df)


    # df = requests.get('https://ftx.us/api/markets/USDT/USD/candles?resolution=86400&start_time=1623110400').json()

    # df = pd.DataFrame(df['result'])
    # st.write("FTX.US USDT USD")

    # # page.write(df)

    # df = px.scatter(
    #     df, #this is the dataframe you are trying to plot
    #     x = "startTime",
    #     y = ['open','close','high','low']
    # )
    # page.plotly_chart(df)


    # st.write("compare")
    df = requests.get('https://ftx.com/api/markets/CUSDT/USDT/candles?resolution=14400&start_time=1623110400').json()

    df = pd.DataFrame(df['result'])
    page.write("FTX cUSDT USDT")
    page.write(df)
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
        # df_merge_p = px.scatter(
    #     df_merge_1, #this is the dataframe you are trying to plot
    #     x = "startTime",
    #     y = ['high','low','MIN(RATE)','MAX(RATE)','AVG(RATE)','MEDIAN(RATE)']
    # )
    # page.plotly_chart(df_merge_p)
    # query_id = "e9b9351a-7cfc-41a6-b217-d8f0d477424e"
    # df_y = pd.read_json(
    #     f"https://api.flipsidecrypto.com/api/v2/queries/{query_id}/data/latest",
    # convert_dates=["TIMESTAMP_NTZ"],
    # )
    # # st.write(df_y)
    # # st.write(df)

    # df_merge_1 = pd.merge(df , df_y , left_index=True, right_index=True)
    # # df_merge_1 = pd.merge(df, df_y, right_on = 'DAYZ')
    # # st.write(df_merge_1)
    # df_merge_p = px.scatter(
    #     df_merge_1, #this is the dataframe you are trying to plot
    #     x = "startTime",
    #     y = ['high','low','MIN(RATE)','MAX(RATE)','AVG(RATE)','MEDIAN(RATE)']
    # )
    # page.plotly_chart(df_merge_p)

    # df_merge_1['upper_spread'] = (df_merge_1['high'] - df_merge_1['AVG(RATE)'])/df_merge_1['AVG(RATE)']
    # df_merge_1['lower_spread'] = (df_merge_1['AVG(RATE)'] - df_merge_1['low'])/df_merge_1['AVG(RATE)']
    # df_merge_1['bid_ask_spread'] = (df_merge_1['high'] - df_merge_1['low'])/df_merge_1['high']
    # df_merge_pp = px.scatter(
    #     df_merge_1, #this is the dataframe you are trying to plot
    #     x = "startTime",
    #     y = ["bid_ask_spread"]
    # )
    # page.plotly_chart(df_merge_pp)
    # df_merge_ppp = px.scatter(
    #     df_merge_1, #this is the dataframe you are trying to plot
    #     x = "startTime",
    #     y = ["upper_spread"]
    # )
    # page.plotly_chart(df_merge_ppp)
    # df_merge_pppp = px.scatter(
    #     df_merge_1, #this is the dataframe you are trying to plot
    #     x = "startTime",
    #     y = ["lower_spread"]
    # )
    # page.plotly_chart(df_merge_pppp)



    # df2 = requests.get('https://ftx.com/api/markets/CUSDT-PERP/candles?resolution=14400&start_time=1623110400').json()
    # df2 = pd.DataFrame(df2['result'])
    # page.write("FTX cUSDT Perp")
    # query_id = "e9b9351a-7cfc-41a6-b217-d8f0d477424e"
    # df_y = pd.read_json(
    #     f"https://api.flipsidecrypto.com/api/v2/queries/{query_id}/data/latest",
    # convert_dates=["TIMESTAMP_NTZ"],
    # )
    # df_merge_2 = pd.merge(df_y, df2 , left_index=True, right_index=True)

    # # st.write(df_merge_2)

    # df3 = px.scatter(
    #     df_merge_2, #this is the dataframe you are trying to plot
    #     x = "startTime",
    #     y = ['high','low','AVG(RATE)']
    # )
    # page.plotly_chart(df3)

    # df_merge_2['upper_spread'] = (df_merge_2['high'] - df_merge_2['AVG(RATE)'])/df_merge_2['AVG(RATE)']
    # df_merge_2['lower_spread'] = (df_merge_2['AVG(RATE)'] - df_merge_2['low'])/df_merge_2['AVG(RATE)']
    # df_merge_2['bid_ask_spread'] = (df_merge_2['high'] - df_merge_2['low'])/df_merge_2['high']
    # df_merge_pp = px.scatter(
    #     df_merge_2, #this is the dataframe you are trying to plot
    #     x = "startTime",
    #     y = ["bid_ask_spread"]
    # )
    # page.plotly_chart(df_merge_pp)
    # df_merge_ppp = px.scatter(
    #     df_merge_2, #this is the dataframe you are trying to plot
    #     x = "startTime",
    #     y = ["upper_spread"]
    # )
    # page.plotly_chart(df_merge_ppp)
    # df_merge_pppp = px.scatter(
    #     df_merge_2, #this is the dataframe you are trying to plot
    #     x = "startTime",
    #     y = ["lower_spread"]
    # )
    # page.plotly_chart(df_merge_pppp)
