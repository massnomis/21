import requests
import json
import streamlit as st
import pandas as pd
names_lending = 'BTC/USD'
df2 = requests.get(f"https://ftx.com/api/markets/{names_lending}/orderbook?depth=100").json()
# st.write(df2)
df2 = pd.DataFrame(df2)
df2 = df2['result']
asks = df2['asks']
bids = df2['bids']
asks = pd.DataFrame(asks)
bids = pd.DataFrame(bids)
asks = asks.rename(columns={0: "price", 1: "size"})
bids = bids.rename(columns={0: "price", 1: "size"})
st.write(bids, asks)