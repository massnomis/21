from itertools import accumulate
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import random
def app():   
    page = st.container()

    tftkn = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/9e36dbae-40e6-4443-a54a-b7166e78ed71/data/latest')
    page.write("Commercial Paper: Within decentralized Finance, a look into TruFi")
    page.markdown('https://app.truefi.io/lend')

    page.write("Accumulated Yield on Selected Paper Pools")

    llal = px.line(tftkn,x='DAYZ',y='PRICE', color = 'TFTOKEN',render_mode="SVG")
    page.plotly_chart(llal)
    # page.write(tftkn)
    page.write("Annualized Yeilds on TruFi Pools")

    mmm = px.line(tftkn,x='DAYZ',y='APY', color = 'TFTOKEN',render_mode="SVG")
    page.plotly_chart(mmm)

    AAVE_RATES = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/ba4e1748-bd25-413d-becc-5adb8fd0042a/data/latest')
    page.write("Comparable Money Market rates.")
    llal = px.line(AAVE_RATES,x='DAYZZZ',y='APY', color = 'RESERVE_NAME',render_mode="SVG")
    page.plotly_chart(llal)



    page.write("USDT")

    filter = AAVE_RATES['RESERVE_NAME']=='USDT'
    filter = AAVE_RATES.where(filter, inplace = False)
    filterUSDT = filter.dropna(how='all')

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                row_width=[0.2, 0.7])
                # DAYZZZ	RESERVE_NAME
# AVG(RESERVE_PRICE)	MEDIAN(RESERVE_PRICE)	MIN(RESERVE_PRICE)	MAX(RESERVE_PRICE)
    # include candlestick with rangeselector\
    # MEDIAN(TOTAL_LIQUIDITY_TOKEN)
    fig.add_trace(go.Candlestick(x=filterUSDT['DAYZZZ'],open=filterUSDT['AVG(RESERVE_PRICE)'], high=filterUSDT['MAX(RESERVE_PRICE)'],low=filterUSDT['MIN(RESERVE_PRICE)'], close=filterUSDT['MEDIAN(RESERVE_PRICE)'],name="OHLC"), row=1, col=1)

    # include a go.Bar trace for volumes
    fig.add_trace(go.Bar(x=filterUSDT['DAYZZZ'], y=filterUSDT['MEDIAN(TOTAL_LIQUIDITY_TOKEN)'],
                showlegend=False), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    page.plotly_chart(fig)




    page.write("USDC")
    filter = AAVE_RATES['RESERVE_NAME']=='USDC'
    filter = AAVE_RATES.where(filter, inplace = False)
    filterUSDC = filter.dropna(how='all')

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                row_width=[0.2, 0.7])
                # DAYZZZ	RESERVE_NAME
# AVG(RESERVE_PRICE)	MEDIAN(RESERVE_PRICE)	MIN(RESERVE_PRICE)	MAX(RESERVE_PRICE)
    # include candlestick with rangeselector\
    # MEDIAN(TOTAL_LIQUIDITY_TOKEN)
    fig.add_trace(go.Candlestick(x=filterUSDC['DAYZZZ'],open=filterUSDC['AVG(RESERVE_PRICE)'], high=filterUSDC['MAX(RESERVE_PRICE)'],low=filterUSDC['MIN(RESERVE_PRICE)'], close=filterUSDC['MEDIAN(RESERVE_PRICE)'],name="OHLC"), row=1, col=1)

    # include a go.Bar trace for volumes
    fig.add_trace(go.Bar(x=filterUSDC['DAYZZZ'], y=filterUSDC['MEDIAN(TOTAL_LIQUIDITY_TOKEN)'],
                showlegend=False), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    page.plotly_chart(fig)



    page.write("BUSD")
    filter = AAVE_RATES['RESERVE_NAME']=='BUSD'
    filter = AAVE_RATES.where(filter, inplace = False)
    filterBUSD = filter.dropna(how='all')

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                row_width=[0.2, 0.7])
                # DAYZZZ	RESERVE_NAME
# AVG(RESERVE_PRICE)	MEDIAN(RESERVE_PRICE)	MIN(RESERVE_PRICE)	MAX(RESERVE_PRICE)
    # include candlestick with rangeselector\
    # MEDIAN(TOTAL_LIQUIDITY_TOKEN)
    fig.add_trace(go.Candlestick(x=filterBUSD['DAYZZZ'],open=filterBUSD['AVG(RESERVE_PRICE)'], high=filterBUSD['MAX(RESERVE_PRICE)'],low=filterBUSD['MIN(RESERVE_PRICE)'], close=filterBUSD['MEDIAN(RESERVE_PRICE)'],name="OHLC"), row=1, col=1)

    # include a go.Bar trace for volumes
    fig.add_trace(go.Bar(x=filterBUSD['DAYZZZ'], y=filterBUSD['MEDIAN(TOTAL_LIQUIDITY_TOKEN)'],
                showlegend=False), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    page.plotly_chart(fig)


    page.write("TUSD")
    filter = AAVE_RATES['RESERVE_NAME']=='TUSD'
    filter = AAVE_RATES.where(filter, inplace = False)
    filterTUSD = filter.dropna(how='all')

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                row_width=[0.2, 0.7])
                # DAYZZZ	RESERVE_NAME
# AVG(RESERVE_PRICE)	MEDIAN(RESERVE_PRICE)	MIN(RESERVE_PRICE)	MAX(RESERVE_PRICE)
    # include candlestick with rangeselector\
    # MEDIAN(TOTAL_LIQUIDITY_TOKEN)
    fig.add_trace(go.Candlestick(x=filterTUSD['DAYZZZ'],open=filterTUSD['AVG(RESERVE_PRICE)'], high=filterTUSD['MAX(RESERVE_PRICE)'],low=filterTUSD['MIN(RESERVE_PRICE)'], close=filterTUSD['MEDIAN(RESERVE_PRICE)'],name="OHLC"), row=1, col=1)

    # include a go.Bar trace for volumes
    fig.add_trace(go.Bar(x=filterTUSD['DAYZZZ'], y=filterTUSD['MEDIAN(TOTAL_LIQUIDITY_TOKEN)'],
                showlegend=False), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    page.plotly_chart(fig)


