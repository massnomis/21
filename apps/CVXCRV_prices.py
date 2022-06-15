# from CurveSim import pool
from itertools import accumulate
import streamlit as st
import plotly
import math
import requests
import plotly.express as px
import pandas as pd
import random
import matplotlib as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def app():
    page = st.container()
    # A = 50


    # CRV = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/d6b45546-4c33-4453-83ed-b0c29f24a2f1/data/latest",
    # convert_dates=["TIMESTAMP_NTZ"],
    # )


    # cvxCRV = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/7fc0fc1b-503c-49ef-8c28-236b849c29fc/data/latest",
    # convert_dates=["TIMESTAMP_NTZ"],
    # )



    # CRV_b = CRV['BALANCE'].iloc[0]
    # cvxCRV_b = cvxCRV['BALANCE'].iloc[0]

    # assets = 2
    # p0 = CRV_b
    # p1 = cvxCRV_b


    # p = pool(A, [p0, p1], assets, p=None, tokens=None, fee=15*10**6)
    # page.write("0: CRV")
    # page.write("1: cvxCRV")


    # page.write(p.xp())




    # def make_lists(r, func):
    #     t = list(r)
    #     return t, [func(x) for x in t]


    # xlist, ylist = make_lists(range(1000,100000000 +1, 1000), lambda i: p.dydxfee(0, 1, i))
    # # xlist, ylist = make_lists([i / 10 for i in range(100)], lambda x: math.sin(x))

    # df = pd.DataFrame(list(zip(xlist, ylist)), columns = ['x','y'])

    # aaa = px.scatter(
    #     df, #this is the dataframe you are trying to plot
    #     x = 'x',
    #     y = 'y'
    #     ,render_mode="SVG"
    # )
    # page.write('CRV-CVXCRV')
    # page.plotly_chart(aaa)



    # xlist, ylist = make_lists(range(1000,100000000 +1, 1000), lambda i: p.dydxfee(1, 0, i))
    # xlist, ylist = make_lists([i / 10 for i in range(100)], lambda x: math.sin(x))

    # df = pd.DataFrame(list(zip(xlist, ylist)), columns = ['x','y'])

    # aaa = px.scatter(
    #     df, #this is the dataframe you are trying to plot
    #     x = 'x',
    #     y = 'y',render_mode="SVG"

    # )
    # page.write('CVXCRV-CRV')
    # page.plotly_chart(aaa)
    df4 = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/e67ea397-b602-49b4-9e04-007960d14e78/data/latest')
    # st.write(df4)

    lll = px.line(df4,x='DAYZ',y=['PRICE_CVXCRV','PRICE_CRV']  ,render_mode="SVG")
    page.plotly_chart(lll)
    # llal = px.line(df4,x='DAYZ',y=['PRICE_CVXCRV','PRICE_CRV'])
    # st.plotly_chart(llal)
    mmm = px.line(df4,x='DAYZ',y='BPS_SPREAD'  ,render_mode="SVG")
    page.plotly_chart(mmm)







    # st.write(xyz)
    
    page.write("https://ftx.com/api/markets/CRV-PERP/candles?resolution=14400")

    df = requests.get('https://ftx.com/api/markets/CRV-PERP/candles?resolution=14400').json()
    df = pd.DataFrame(df['result'])

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

    # page.markdown('https://llama.airforce/#/votium/overview')

    xyz = requests.get('https://ftxpremiums.com/assets/data/funding_data/CRV-PERP.json').json()

    xyz = pd.DataFrame(xyz)
    xyz['rate'] = xyz['rate'].astype(float)
    xyz['time'] =  pd.to_datetime(xyz['time'], unit='s')
    xyz = xyz.sort_values(by="time")




    xyz = pd.DataFrame(xyz)
    # print(xyz)
    # print(xyz.columns)
    xyz['rate'] = xyz['rate'] * 1000

    xyz['accumulated'] = (list(accumulate(xyz['rate'])))


    bbbbbb = px.line(xyz,x='time',y='rate')
    page.plotly_chart(bbbbbb)
    bbbbbbb = px.line(xyz,x='time',y='accumulated')
    page.plotly_chart(bbbbbbb)
    # page.write("https://ftx.com/api/markets/CVX-PERP/candles?resolution=14400")

    # df = requests.get('https://ftx.com/api/markets/CVX-PERP/candles?resolution=14400').json()
    # df = pd.DataFrame(df['result'])

    # # st.write(df)
    # # Create figure with secondary y-axis
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

    # # page.markdown('https://llama.airforce/#/votium/overview')

    # xyz = requests.get('https://ftxpremiums.com/assets/data/funding_data/CVX-PERP.json').json()

    # xyz = pd.DataFrame(xyz)
    # xyz['rate'] = xyz['rate'].astype(float)
    # xyz['time'] =  pd.to_datetime(xyz['time'], unit='s')
    # xyz = xyz.sort_values(by="time")




    # xyz = pd.DataFrame(xyz)
    # # print(xyz)
    # # print(xyz.columns)
    # xyz['rate'] = xyz['rate'] * 1000

    # xyz['accumulated'] = (list(accumulate(xyz['rate'])))


    # bbbbbb = px.line(xyz,x='time',y='rate')
    # page.plotly_chart(bbbbbb)
    # bbbbbbb = px.line(xyz,x='time',y='accumulated')
    # page.plotly_chart(bbbbbbb)





































