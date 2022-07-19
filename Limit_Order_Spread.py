import ccxt
import streamlit as st
import pandas as pd
from itertools import accumulate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import chain
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import math
import asyncio
import os
import sys
from pprint import pprint
import json
  
st.set_page_config(layout="wide")
current_exchange = st.selectbox("exchange", ccxt.exchanges, index=21) 

if current_exchange== 'bitmex':
    exchange = ccxt.bitmex({
        'apiKey': 'NOAb2TuyuLgWkYbXOQGH-x9b',
        'secret': '_fAxf57mItdpX-A5KTxXRzJZY3zkeSKdCGlStwa95FAH81Gd',
    })
else:
    st.write("exchange not integrated")

if 'test' in exchange.urls:
    exchange.urls['api'] = exchange.urls['test']

market_data = pd.DataFrame(exchange.load_markets()).astype(str)
st.write(market_data)
Market_list = market_data.columns


Trading_Market = st.selectbox("Trading Market", Market_list)
Hedging_Market = st.selectbox("Hedge Market", Market_list)

Trading_Market_Precision = (precision_load[Trading_Market]['precision'])
Hedging_Market_Precision = (precision_load[Hedging_Market]['precision'])


Trading_Market_Data = pd.DataFrame(exchange.fetch_ticker(Trading_Market)).astype(str)
Hedging_Market_Data = pd.DataFrame(exchange.fetch_ticker(Hedging_Market)).astype(str)
Trading_Order_Book = exchange.fetchOrderBook(Trading_Market)
Trading_Order_Book_Bids = pd.DataFrame(Trading_Order_Book['bids'])
Trading_Order_Book_Asks = pd.DataFrame(Trading_Order_Book['asks'])

#Hedging_Order_Book = exchange.fetchOrderBook(Hedging_Market)

#for i in Trading_Order_book

st.write(Trading_Market_Data)
st.write(Hedging_Market_Data)
st.write(Trading_Order_Book)
st.write(Trading_Order_Book_Bids)


df1 = df1['result']
asks = df1['asks']
bids = df1['bids']
asks = pd.DataFrame(asks)
bids = pd.DataFrame(bids)
asks = asks.rename(columns={0: "price", 1: "size"})
bids = bids.rename(columns={0: "price", 1: "size"})

asks['accumulated_size']  = (list(accumulate(asks['size'])))
asks['accumulated_price']  = (asks['price']) * asks['size']
asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated_size']
asks['cash_equivelant'] = asks['accumulated_size'] * asks['accumulated_avg_price']


bids['accumulated_size']  = (list(accumulate(bids['size'])))
bids['accumulated_price']  = (bids['price']) * bids['size']
bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated_size']
bids['cash_equivelant'] = bids['accumulated_size'] * bids['accumulated_avg_price']




column = bids["price"]
max_value_dated_futures = column.max()
st.write("best ask dated futures", max_value_dated_futures)


column = asks["price"]
min_value_dated_futures = column.min()
st.write("best bid dated futures", min_value_dated_futures)

spred_dated = min_value_dated_futures - max_value_dated_futures
st.write("spread dated futures", spred_dated)



spred_dated_BPS = spred_dated/min_value_dated_futures*1000
st.write("spread dated futures", spred_dated_BPS, "bps")
# asks['price'] = asks[0]
# asks['size'] = asks[1]
for i in range(1, 2):
    cols = st.columns(2)
    cols[0].subheader("bids")

    cols[0].write(bids)
    cols[1].subheader("asks")

    cols[1].write(asks)
    

fig = make_subplots(specs=[[{"secondary_y": True}]])
# Add traces
fig.add_trace(
    go.Scatter(x=asks['price'], y=asks['accumulated_size'], name="asks"),
    secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=bids['price'], y=bids['accumulated_size'], name="bids"),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text="orderbook"
)

# Set x-axis title


st.plotly_chart(fig, use_container_width=True)



# fig = make_subplots(specs=[[{"secondary_y": True}]])
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Bar(x=asks['price'], y=asks['size'], name="asks"),
    secondary_y=True,
)

fig.add_trace(
    go.Bar(x=bids['price'], y=bids['size'], name="bids"),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text="orderbook"
)

# Set x-axis title
st.plotly_chart(fig, use_container_width=True)

# fig = make_subplots(specs=[[{"secondary_y": True}]])
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=asks['accumulated_avg_price'], y=asks['cash_equivelant'], name="asks"),
    secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=bids['accumulated_avg_price'], y=bids['cash_equivelant'], name="bids"),
    secondary_y=True,
)




   