from operator import index
from turtle import title
import ccxtpro
import asyncio
from numpy import place
import streamlit as st
import json
import pandas as pd
from itertools import accumulate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

import ccxt
import plotly.express as px

st.set_page_config(layout="wide")





placeholder0 = st.empty()
placeholder1 = st.empty()
placeholder2 = st.empty()
placeholder3 = st.empty()
placeholder_bids = st.empty()
placeholder_asks = st.empty()
placeholder4 = st.empty()
placeholder5 = st.empty()
placeholder6 = st.empty()
placeholder7 = st.empty()
placeholder8 = st.empty()
placeholder9 = st.empty()
placeholder10 = st.empty()
placeholder11 = st.empty()
placeholder12 = st.empty()
placeholder13 = st.empty()
placeholder14 = st.empty()
placeholder15 = st.empty()


exchange = ccxtpro.bitmex({
    'apiKey': 'NOAb2TuyuLgWkYbXOQGH-x9b',
    'secret': '_fAxf57mItdpX-A5KTxXRzJZY3zkeSKdCGlStwa95FAH81Gd',
})
if 'test' in exchange.urls:
    exchange.urls['api'] = exchange.urls['test'] # ←----- switch the base URL to testnet
# st.write(exchange.fetchOpenOrders())


ccxtbus = ccxt.bitmex({
    'apiKey': 'NOAb2TuyuLgWkYbXOQGH-x9b',
    'secret': '_fAxf57mItdpX-A5KTxXRzJZY3zkeSKdCGlStwa95FAH81Gd',
})
if 'test' in ccxtbus.urls:
    ccxtbus.urls['api'] = ccxtbus.urls['test'] # ←----- switch the base URL to testnet
markets = ccxtbus.load_markets()
markets = pd.DataFrame.from_dict(markets)

df1 = pd.DataFrame.from_dict(markets)
df1 = df1.astype(str)
df1 = df1.columns
# st.write(df1)
with placeholder0.container():
    # market="BTC/USDT:USDT"
    market = st.selectbox("Select Market", df1, index=626)


async def OLHC():
    while True:
        ohlc = await exchange.watch_ohlcv(market)
        ohlc = pd.DataFrame(ohlc)
        ohlc.reset_index(drop=True, inplace=False)
        ohlc = ohlc.rename(columns={0: "time", 1: "open", 2: "high", 3: "low", 4: "close", 5: "volume"})
        ohlc['time'] = pd.to_datetime(ohlc['time'], unit='ms')
        with placeholder1:
            fig = go.Figure()
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
            vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
            row_width=[0.2, 0.7])
            fig.add_trace(go.Candlestick(x=ohlc['time'], open=ohlc['open'], high=ohlc['high'], low=ohlc['low'], close=ohlc['close'], name = "OHLC"), row=1, col=1)
            fig.add_trace(go.Bar(x=ohlc['time'], y=ohlc['volume'],showlegend=False, name = 'volume'), row=2, col=1)
            fig.update(layout_xaxis_rangeslider_visible=False)
            fig.update_layout(title_text="OHLC")
            st.plotly_chart(fig, use_container_width=True)
async def trades():
    while True:
        trades = await exchange.watch_trades(market)
        tradez = pd.DataFrame.from_dict(trades)
        with placeholder2.container():
            st.plotly_chart(px.scatter(tradez, x="datetime", y="price", color="side", size='amount',color_discrete_sequence=["red", "green"],), use_container_width=True)
async def books():
    spread_bps_df_2 = pd.DataFrame()
    while True:
        orderbook = await exchange.watch_order_book(market)
        bids = orderbook["bids"]
        bids = pd.DataFrame(bids)
        bids = bids.rename(columns={0: "price_bid", 1: "size_bid"})
        asks = orderbook["asks"]
        asks = pd.DataFrame(asks)
        asks.reset_index(drop=True, inplace=False)
        bids.reset_index(drop = True, inplace=False)
        asks = asks.rename(columns={0: "price_ask", 1: "size_ask"})
        asks['accumulated']  = (list(accumulate(asks['size_ask'])))
        asks['accumulated_price']  = (asks['price_ask']) * asks['size_ask']
        asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
        asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']
        bids['accumulated']  = (list(accumulate(bids['size_bid'])))
        bids['accumulated_price']  = (bids['price_bid']) * bids['size_bid']
        bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
        bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']       
        spread_bps_df_add = pd.DataFrame({'time': [datetime.datetime.now()], 'spread_bps': [(((asks['price_ask'][0] - bids['price_bid'][0])/asks['price_ask'][0]) * 10000)]})
        spread_bps_df_2 = spread_bps_df_2.append(spread_bps_df_add)
        with placeholder3:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=asks['price_ask'], y=asks['accumulated'], name="asks"),secondary_y=True,)
            fig.add_trace(go.Scatter(x=bids['price_bid'], y=bids['accumulated'], name="bids"),secondary_y=True,)
            fig.update_layout(title_text="orderbook")
            st.plotly_chart(fig, use_container_width=True)
        with placeholder_bids:
            st.write(bids)
        with placeholder_asks:
            st.write(asks)
            
        with placeholder4:
            st.plotly_chart(px.scatter(spread_bps_df_2, x="time", y="spread_bps"), use_container_width=True)
async def trades_history():
    while True:
        trades = await exchange.fetch_trades(market)
        tradez = pd.DataFrame.from_dict(trades)
        with placeholder5:
            st.write(tradez)
async def main():
    # Schedule three calls *concurrently*:
        await asyncio.gather(
        # trades(),
        books(),
        # OLHC(),
        # trades_ history(),
    )

asyncio.run(main())   