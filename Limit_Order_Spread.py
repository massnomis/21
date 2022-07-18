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

Trading_Market_Data = pd.DataFrame(exchange.fetch_ticker(Trading_Market)).astype(str)
Hedging_Market_Data = pd.DataFrame(exchange.fetch_ticker(Hedging_Market)).astype(str)
Trading_Market_order_book = (exchange.fetchOrderBook(Trading_Market)) 
Hedging_Market_order_book = (exchange.fetchOrderBook(Hedging_Market)) 

st.write(Trading_order_book)
st.write(Hedging_order_book)
st.write(Trading_Market_Data)
st.write(Hedging_Market_Data)

#     # don't forget to free the used resources, when you don't need them anymore
# exchange.close()
# st.write(ticker)

    #product_list = ccxt.bitmex.




   