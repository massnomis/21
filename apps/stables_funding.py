
from itertools import accumulate
import pandas as pd
import streamlit as st
import plotly.express as px
import requests
from plotly.subplots import make_subplots
import plotly.graph_objects as go
# from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import random
# @st.cache(suppress_st_warning=True)

def app():   
    page = st.container()

    page.write("https://ftx.com/api/markets/USDT-PERP/candles?resolution=14400")

    df = requests.get('https://ftx.com/api/markets/USDT-PERP/candles?resolution=14400').json()
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
    page.write('usdt perp')

    xyz2 = requests.get('https://ftxpremiums.com/assets/data/funding_data/USDT-PERP.json').json()

    xyz2 = pd.DataFrame(xyz2)

    xyz2['rate'] = xyz2['rate'].astype(float)
    xyz2['time'] =  pd.to_datetime(xyz2['time'], unit='s')
    xyz2 = xyz2.sort_values(by="time")






    xyz2['rate'] = xyz2['rate'] * 1000
    xyz2['accumulated']  = (list(accumulate(xyz2['rate'])))

    bbbbbb = px.line(xyz2,x='time',y='rate',render_mode="SVG")
    page.plotly_chart(bbbbbb)
    bbbbbbb = px.line(xyz2,x='time',y='accumulated',render_mode="SVG")
    page.plotly_chart(bbbbbbb)
    page.write('cusdt perp')
    xyz22 = requests.get('https://ftxpremiums.com/assets/data/funding_data/CUSDT-PERP.json').json()

    xyz22 = pd.DataFrame(xyz22)
    xyz22['rate'] = xyz22['rate'].astype(float)
    xyz22['time'] =  pd.to_datetime(xyz22['time'], unit='s')
    xyz22 = xyz22.sort_values(by="time")






    xyz22['rate'] = xyz22['rate'] * 1000
    xyz22['accumulated']  = (list(accumulate(xyz22['rate'])))

    bbbbbb = px.line(xyz22,x='time',y='rate',render_mode="SVG")
    page.plotly_chart(bbbbbb)
    bbbbbbb = px.line(xyz22,x='time',y='accumulated',render_mode="SVG")
    page.plotly_chart(bbbbbbb)




    
    custom_lending = requests.get(f"https://ftx.com/api/spot_margin/history?coin=USD&start_time=960368456&end_time=1854597556").json()

    custom_lending = pd.DataFrame(custom_lending['result'])
    custom_lending['rate'] = custom_lending['rate'].astype(float)
    custom_lending['time'] =  pd.to_datetime(custom_lending['time'])
    custom_lending = custom_lending.sort_values(by="time", ascending=True)

    custom_lending['accumulated']  = (list(accumulate(custom_lending['rate'] * custom_lending['size'])))

    custom_lending['rate'] = custom_lending['rate'] * 24 * 36500
    # page.write(custom_lending)
    bbbbbb = px.line(custom_lending,x='time',y='rate',render_mode="SVG")
    page.plotly_chart(bbbbbb)

    bbbbbbbb = px.line(custom_lending,x='time',y='size',render_mode="SVG")
    page.plotly_chart(bbbbbbbb)
    bbbbbbb = px.line(custom_lending,x='time',y='accumulated',render_mode="SVG")
    page.plotly_chart(bbbbbbb)

    custom_lending = requests.get(f"https://ftx.com/api/spot_margin/history?coin=USDT&start_time=960368456&end_time=1854597556").json()

    custom_lending = pd.DataFrame(custom_lending['result'])
    custom_lending['rate'] = custom_lending['rate'].astype(float)
    custom_lending['time'] =  pd.to_datetime(custom_lending['time'])
    custom_lending = custom_lending.sort_values(by="time", ascending=True)

    custom_lending['accumulated']  = (list(accumulate(custom_lending['rate'] * custom_lending['size'])))

    custom_lending['rate'] = custom_lending['rate'] * 24 * 36500
    # page.write(custom_lending)
    bbbbbb = px.line(custom_lending,x='time',y='rate',render_mode="SVG")
    page.plotly_chart(bbbbbb)

    bbbbbbbb = px.line(custom_lending,x='time',y='size',render_mode="SVG")
    page.plotly_chart(bbbbbbbb)
    bbbbbbb = px.line(custom_lending,x='time',y='accumulated',render_mode="SVG")
    page.plotly_chart(bbbbbbb)
    custom_lending = requests.get(f"https://ftx.us/api/spot_margin/history?coin=USD&start_time=960368456&end_time=1854597556").json()

    custom_lending = pd.DataFrame(custom_lending['result'])
    custom_lending['rate'] = custom_lending['rate'].astype(float)
    custom_lending['time'] =  pd.to_datetime(custom_lending['time'])
    custom_lending = custom_lending.sort_values(by="time", ascending=True)

    custom_lending['accumulated']  = (list(accumulate(custom_lending['rate'] * custom_lending['size'])))

    custom_lending['rate'] = custom_lending['rate'] * 24 * 36500
    # page.write(custom_lending)
    bbbbbb = px.line(custom_lending,x='time',y='rate',render_mode="SVG")
    page.plotly_chart(bbbbbb)

    bbbbbbbb = px.line(custom_lending,x='time',y='size',render_mode="SVG")
    page.plotly_chart(bbbbbbbb)
    bbbbbbb = px.line(custom_lending,x='time',y='accumulated',render_mode="SVG")
    page.plotly_chart(bbbbbbb)

    custom_lending = requests.get(f"https://ftx.us/api/spot_margin/history?coin=USDT&start_time=960368456&end_time=1854597556").json()

    custom_lending = pd.DataFrame(custom_lending['result'])
    custom_lending['rate'] = custom_lending['rate'].astype(float)
    custom_lending['time'] =  pd.to_datetime(custom_lending['time'])
    custom_lending = custom_lending.sort_values(by="time", ascending=True)

    custom_lending['accumulated']  = (list(accumulate(custom_lending['rate'] * custom_lending['size'])))

    custom_lending['rate'] = custom_lending['rate'] * 24 * 36500
    # page.write(custom_lending)
    bbbbbb = px.line(custom_lending,x='time',y='rate',render_mode="SVG")
    page.plotly_chart(bbbbbb)

    bbbbbbbb = px.line(custom_lending,x='time',y='size',render_mode="SVG")
    page.plotly_chart(bbbbbbbb)
    bbbbbbb = px.line(custom_lending,x='time',y='accumulated',render_mode="SVG")
    page.plotly_chart(bbbbbbb)
