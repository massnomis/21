
from itertools import accumulate
import pandas as pd
import streamlit as st
import plotly.express as px
import requests
from plotly.subplots import make_subplots
import plotly.graph_objects as go
# @st.cache(suppress_st_warning=True)
def app():
    page = st.container()
        
    custom_lending0 = requests.get(f"https://ftx.us/api/spot_margin/history?coin=USD&start_time=960368456&end_time=1854597556").json()
    page.write("FTX US USD Spot Margin")

    custom_lending0 = pd.DataFrame(custom_lending0['result'])
    custom_lending0['rate'] = custom_lending0['rate'].astype(float)
    custom_lending0['time'] =  pd.to_datetime(custom_lending0['time'])
    custom_lending0 = custom_lending0.sort_values(by="time", ascending=True)


# custom_lending['accumulated']  = (list(accumulate(custom_lending['rate'] * custom_lending['size'])))

    custom_lending0['rateAPY'] = custom_lending0['rate'] * 24 * 36500
    custom_lending0['interest'] = custom_lending0['rate'] * custom_lending0['size']
    # page.write(custom_lending1)
    # aaa = px.line(custom_lending1,x='time',y='rate')
    # page.plotly_chart(aaa)
    FTX_US_USD_Spot_Margin1 = px.line(custom_lending0,x='time',y='rateAPY', render_mode="SVG")
    page.plotly_chart(FTX_US_USD_Spot_Margin1)
    FTX_US_USD_Spot_Margin2 = px.line(custom_lending0,x='time',y='size',render_mode="SVG")
    page.plotly_chart(FTX_US_USD_Spot_Margin2)
    FTX_US_USD_Spot_Margin3 = px.line(custom_lending0,x='time',y='interest',render_mode="SVG")
    page.plotly_chart(FTX_US_USD_Spot_Margin3)

    custom_lending1 = requests.get(f"https://ftx.us/api/spot_margin/history?coin=USDT&start_time=960368456&end_time=1854597556").json()
    page.write("FTX US USDT Spot Margin")

    custom_lending1 = pd.DataFrame(custom_lending1['result'])
    custom_lending1['rate'] = custom_lending1['rate'].astype(float)
    custom_lending1['time'] =  pd.to_datetime(custom_lending1['time'])
    custom_lending1 = custom_lending1.sort_values(by="time", ascending=True)

# custom_lending['accumulated']  = (list(accumulate(custom_lending['rate'] * custom_lending['size'])))

    custom_lending1['rateAPY'] = custom_lending1['rate'] * 24 * 36500
    custom_lending1['interest'] = custom_lending1['rate'] * custom_lending1['size']
    # page.write(custom_lending1)
    # aaa = px.line(custom_lending1,x='time',y='rate')
    # page.plotly_chart(aaa)
    aaa = px.line(custom_lending1,x='time',y='rateAPY',render_mode="SVG")
    page.plotly_chart(aaa)
    aa = px.line(custom_lending1,x='time',y='size',render_mode="SVG")
    page.plotly_chart(aa)
    a = px.line(custom_lending1,x='time',y='interest',render_mode="SVG")
    page.plotly_chart(a)
    custom_lending1 = requests.get(f"https://ftx.us/api/spot_margin/history?coin=CUSDT&start_time=960368456&end_time=1854597556").json()
    page.write("FTX US CUSDT Spot Margin")

    custom_lending1 = pd.DataFrame(custom_lending1['result'])
    custom_lending1['rate'] = custom_lending1['rate'].astype(float)
    custom_lending1['time'] =  pd.to_datetime(custom_lending1['time'])
    custom_lending1 = custom_lending1.sort_values(by="time", ascending=True)

# custom_lending['accumulated']  = (list(accumulate(custom_lending['rate'] * custom_lending['size'])))

    custom_lending1['rateAPY'] = custom_lending1['rate'] * 24 * 36500
    custom_lending1['interest'] = custom_lending1['rate'] * custom_lending1['size']
    # page.write(custom_lending1)
    # aaa = px.line(custom_lending1,x='time',y='rate')
    # page.plotly_chart(aaa)
    aaa = px.line(custom_lending1,x='time',y='rateAPY',render_mode="SVG")
    page.plotly_chart(aaa)
    aa = px.line(custom_lending1,x='time',y='size',render_mode="SVG")
    page.plotly_chart(aa)
    a = px.line(custom_lending1,x='time',y='interest',render_mode="SVG")
    page.plotly_chart(a)

