import streamlit as st
import requests
import json
import pandas as pd
import math
import time
from itertools import accumulate
# from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import chain

import plotly.express as px
from datetime import datetime
# ts = int('1645598410')

# print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
import json
import requests
import pandas as pd
import random

premiums = requests.get('https://ftxpremiums.com/assets/data/premiums.json')
premiums = json.loads(premiums.text)
premiums = pd.DataFrame(premiums)
# print(premiums)
st.write("cash and carry premiums")
st.write(premiums)
lending = requests.get('https://ftxpremiums.com/assets/data/lending.json')
lending = json.loads(lending.text)
lending = pd.DataFrame(lending)
# print(lending)    
st.write("lending rates")

st.write(lending)
funding = requests.get('https://ftxpremiums.com/assets/data/funding.json')
funding = json.loads(funding.text)
funding = pd.DataFrame(funding)
# print(funding)
st.write("funding rates")

st.write(funding)
premiums_names = premiums['name']
st.write(premiums_names)


lending_names = lending['name']
st.write(lending_names)

perp_names = lending['name']
st.write(perp_names)


# @st.cache
names_premeiums = st.selectbox("premiums", premiums_names)
st.write(names_premeiums)
# page.write(lending_names)

# custom_lending = requests.get(f"https://ftx.com/api/spot_margin/history?coin={NAME_LENDING}&start_time=960368456&end_time=1854597556").json()
# custom_lending = pd.DataFrame(custom_lending['result'])
# st.write(custom_lending)



# df = requests.get(f"https://ftx.com/api/markets/{NAME_LENDING}-PERP/candles?resolution=14400").json()
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
# st.plotly_chart(fig)


# df = requests.get(f"https://ftx.com/api/markets/{NAME_LENDING}/USD/candles?resolution=14400").json()
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
# st.plotly_chart(fig)


df = requests.get(f"https://ftx.com/api/markets/{names_premeiums}/candles?resolution=14400").json()
# st.write(df)
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
st.plotly_chart(fig)

df1 = requests.get(f"https://ftx.com/api/markets/{names_premeiums}/orderbook?depth=100").json()
df1 = pd.DataFrame(df1)
df1 = df1['result']
asks = df1['asks']
bids = df1['bids']

# rename collums
# plot depth
# pick orders
# pragnate orders into ccxt
# exec


# loop later to show postioning
asks = pd.DataFrame(asks)
bids = pd.DataFrame(bids)
# st.write(df1)
st.write(asks)
st.write(bids)

