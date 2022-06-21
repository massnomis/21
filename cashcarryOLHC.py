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
st.set_page_config(layout="wide")



# st.text('Fixed width text')
# st.markdown('_Markdown_') # see *
# st.latex(r''' e^{i\pi} + 1 = 0 ''')
# st.write('Most objects') # df, err, func, keras!
# st.write(['st', 'is <', 3]) # see *
# st.title('My title')
# st.header('My header')
# st.subheader('My sub')
# st.code('for i in range(8): foo()')



# premiums = requests.get('https://ftxpremiums.com/assets/data/premiums.json')
# premiums = json.loads(premiums.text)
# premiums = pd.DataFrame(premiums)
# print(premiums)
# st.write("cash and carry premiums")
# st.write(premiums)
# lending = requests.get('https://ftxpremiums.com/assets/data/lending.json')
# lending = json.loads(lending.text)
# lending = pd.DataFrame(lending)
# # print(lending)    
# # st.write("lending rates")

# # st.write(lending)
# funding = requests.get('https://ftxpremiums.com/assets/data/funding.json')
# funding = json.loads(funding.text)
# funding = pd.DataFrame(funding)
# # print(funding)
# st.write("funding rates")

# st.write(funding)
# premiums_names = premiums['name']
# premiums_names.sort_values(ascending=True)
# 

# lending_names = lending['name']
# # st.write(lending_names)

# perp_names = funding['name']
# # st.write(perp_names)

# names_premeiums = 'BTC/USD'
# @st.cache
# st.title("HERE CREAMY D CLIUVK HERE")
# st.write(names_premeiums)
funding = pd.read_csv('funding.csv')
lending = pd.read_csv('lending.csv')

premiums = pd.read_csv('premiums.csv')
names_premeiums = st.selectbox("premiums", premiums)
# st.write(names_premeiums)
names_lending = st.selectbox("lending", lending

# , index = random.randint(0, 100)
)
# st.write(names_lending)
name_perp = st.selectbox("perp", funding

# , index = random.randint(0, 10)
)

# st.write(names_premeiums)
st.title('dated futures')
df0 = requests.get(f"https://ftx.com/api/markets/{names_premeiums}/candles?resolution=14400").json()
# st.write(df)
df0 = pd.DataFrame(df0['result'])

# st.write(df)
# Create figure with secondary y-axis
fig0 = make_subplots(rows=2, cols=1, shared_xaxes=True, 
            vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
            row_width=[0.2, 0.7])

# include candlestick with rangeselector
fig0.add_trace(go.Candlestick(x=df0['startTime'],open=df0['open'], high=df0['high'],low=df0['low'], close=df0['close'],name="OHLC"), row=1, col=1)

# include a go.Bar trace for volumes
fig0.add_trace(go.Bar(x=df0['startTime'], y=df0['volume'],
            showlegend=False), row=2, col=1)

fig0.update(layout_xaxis_rangeslider_visible=False)
st.plotly_chart(fig0, use_container_width=True)


df1 = requests.get(f"https://ftx.com/api/markets/{names_premeiums}/orderbook?depth=100").json()
df1 = pd.DataFrame(df1)
df1 = df1['result']
asks = df1['asks']
bids = df1['bids']
asks = pd.DataFrame(asks)
bids = pd.DataFrame(bids)
# st.write(df1)
asks = asks.rename(columns={0: "price", 1: "size"})
bids = bids.rename(columns={0: "price", 1: "size"})

asks['accumulated']  = (list(accumulate(asks['size'])))
asks['accumulated_price']  = (asks['price']) * asks['size']
asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']


bids['accumulated']  = (list(accumulate(bids['size'])))
bids['accumulated_price']  = (bids['price']) * bids['size']
bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']



# sum of price*size 
# divided by sum of size


column = bids["price"]
max_value_dated_futures = column.max()
st.write(max_value_dated_futures)


column = asks["price"]
min_value_dated_futures = column.min()
st.write(min_value_dated_futures)

spred_dated = min_value_dated_futures - max_value_dated_futures
st.write(spred_dated)



spred_dated_BPS = spred_dated/min_value_dated_futures*1000
st.write(spred_dated_BPS , "bps")
# asks['price'] = asks[0]
# asks['size'] = asks[1]
for i in range(1, 2):
    cols = st.columns(2)
    cols[0].write(bids)
    
    cols[1].write(asks)

fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=asks['price'], y=asks['accumulated'], name="asks"),
    secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=bids['price'], y=bids['accumulated'], name="bids"),
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

# Add figure title
fig.update_layout(
    title_text="cash_equivelant"
)

# Set x-axis title


st.plotly_chart(fig, use_container_width=True)















st.write(names_lending)
st.title('spot/usd/lending')

dft2 = requests.get(f"https://ftx.com/api/markets/{names_lending}/USD/candles?resolution=14400").json()
# st.write(df)
dft2 = pd.DataFrame(dft2['result'])

# st.write(df)
# Create figure with secondary y-axis
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
            vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
            row_width=[0.2, 0.7])

# include candlestick with rangeselector
fig.add_trace(go.Candlestick(x=dft2['startTime'],open=dft2['open'], high=dft2['high'],low=dft2['low'], close=dft2['close'],name="OHLC"), row=1, col=1)

# include a go.Bar trace for volumes
fig.add_trace(go.Bar(x=dft2['startTime'], y=dft2['volume'],
            showlegend=False), row=2, col=1)

fig.update(layout_xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)









df2 = requests.get(f"https://ftx.com/api/markets/{names_lending}/USD/orderbook?depth=100").json()
df2 = pd.DataFrame(df2)
df2 = df2['result']
asks = df2['asks']
bids = df2['bids']


asks = pd.DataFrame(asks)
bids = pd.DataFrame(bids)
# st.write(df1)

# st.write(asks)
# st.write(bids)

asks = asks.rename(columns={0: "price", 1: "size"})
bids = bids.rename(columns={0: "price", 1: "size"})
asks['accumulated']  = (list(accumulate(asks['size'])))
asks['accumulated_price']  = (asks['price']) * asks['size']
asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']


bids['accumulated']  = (list(accumulate(bids['size'])))
bids['accumulated_price']  = (bids['price']) * bids['size']
bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']
column = bids["price"]
max_value_spot = column.max()
st.write(max_value_spot)

column = asks["price"]
min_value_spot = column.min()
st.write(min_value_spot)

spred_spot = min_value_spot - max_value_spot
st.write(spred_spot)

spred_bps_spot = spred_spot/min_value_spot*1000
st.write(spred_bps_spot , "bps")
# asks['price'] = asks[0]
# asks['size'] = asks[1]
for i in range(1, 2):
    cols = st.columns(2)
    cols[0].write(bids)
    
    cols[1].write(asks)


fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=asks['price'], y=asks['accumulated'], name="asks"),
    secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=bids['price'], y=bids['accumulated'], name="bids"),
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

# Add figure title
fig.update_layout(
    title_text="cash_equivelant"
)

# Set x-axis title


st.plotly_chart(fig, use_container_width=True)



custom_lending = requests.get(f"https://ftx.com/api/spot_margin/history?coin={names_lending}&start_time=960368456&end_time=1854597556").json()

custom_lending = pd.DataFrame(custom_lending['result'])
custom_lending['rate'] = custom_lending['rate'].astype(float)
custom_lending['time'] =  pd.to_datetime(custom_lending['time'])
custom_lending = custom_lending.sort_values(by="time", ascending=True)

# custom_lending['accumulated']  = (list(accumulate(custom_lending['rate'] * custom_lending['size'])))

custom_lending['rateAPY'] = custom_lending['rate'] * 24 * 36500
custom_lending['interest'] = custom_lending['rate'] * custom_lending['size']
# st.write(custom_lending)
# aaa = px.line(custom_lending,x='time',y='rate',render_mode="SVG")
# st.plotly_chart(aaa)
aaa = px.line(custom_lending,x='time',y='rateAPY',render_mode="SVG")
st.plotly_chart(aaa, use_container_width=True)
aa = px.line(custom_lending,x='time',y='size',render_mode="SVG")
st.plotly_chart(aa, use_container_width=True)
a = px.line(custom_lending,x='time',y='interest',render_mode="SVG")
st.plotly_chart(a, use_container_width=True)

custom_lending['rate_bps_hr'] = custom_lending['rate'] * 1000
custom_lending['accumulated']  = (list(accumulate(custom_lending['rate_bps_hr'])))
# st.write('hourly funding rate in basis points')
bbbbbb = px.line(custom_lending,x='time',y='rate_bps_hr',render_mode="SVG")
st.plotly_chart(bbbbbb, use_container_width=True)
bbbbbbb = px.line(custom_lending,x='time',y='accumulated',render_mode="SVG")
st.plotly_chart(bbbbbbb, use_container_width=True)






st.write(name_perp)
st.title('perpetual futures')



df = requests.get(f"https://ftx.com/api/markets/{name_perp}/candles?resolution=14400").json()
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
st.plotly_chart(fig, use_container_width=True)















df30 = requests.get(f"https://ftx.com/api/markets/{name_perp}/orderbook?depth=100").json()
df30 = pd.DataFrame(df30)
df30 = df30['result']
asks = df30['asks']
bids = df30['bids']
# rename collums
# plot depth
# pick orders
# pragnate orders into ccxt
# exec


# loop later to show postioning
asks = pd.DataFrame(asks)
bids = pd.DataFrame(bids)
# st.write(df1)


asks = asks.rename(columns={0: "price", 1: "size"})
bids = bids.rename(columns={0: "price", 1: "size"})
asks['accumulated']  = (list(accumulate(asks['size'])))
asks['accumulated_price']  = (asks['price']) * asks['size']
asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']


bids['accumulated']  = (list(accumulate(bids['size'])))
bids['accumulated_price']  = (bids['price']) * bids['size']
bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']

column = bids["price"]
max_value_perps = column.max()
st.write(max_value_perps)


column = asks["price"]
min_value_perps = column.min()
st.write(min_value_perps)

spred_perps = min_value_perps - max_value_perps
st.write(spred_perps)

spred_bps_perps = spred_perps/min_value_perps*1000
st.write(spred_bps_perps , "bps")
# asks['price'] = asks[0]
# asks['size'] = asks[1]
for i in range(1, 2):
    cols = st.columns(2)
    cols[0].write(bids)
    
    cols[1].write(asks)



fig = make_subplots(specs=[[{"secondary_y": True}]])
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=asks['price'], y=asks['accumulated'], name="asks"),
    secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=bids['price'], y=bids['accumulated'], name="bids"),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text="orderbook"
)

# Set x-axis title


st.plotly_chart(fig, use_container_width=True)
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Bar(x=asks['price'], y=asks['size'], name="asks"),
    secondary_y=False,
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

# Add figure title
fig.update_layout(
    title_text="cash_equivelant"
)

# Set x-axis title


st.plotly_chart(fig, use_container_width=True)
st.write("Predicted funding rate. Longs pay shorts if positive, shorts pay longs if negative. 1/24 times the average premium over the hour.")
custom = requests.get(f"https://ftxpremiums.com/assets/data/funding_data/{name_perp}.json").json()

custom = pd.DataFrame(custom)
custom['rate'] = custom['rate'].astype(float)
custom['time'] =  pd.to_datetime(custom['time'], unit='s')
custom = custom.sort_values(by="time")

custom['rate'] = custom['rate'] * 1000
custom['rate_APY'] = custom['rate'] / 10 * 24 * 365.24

custom['accumulated']  = (list(accumulate(custom['rate'])))
# / 10 * 24 * 365.24
st.write('hourly funding rate in basis points')
bbbbbb = px.line(custom,x='time',y='rate',render_mode="SVG")
st.plotly_chart(bbbbbb, use_container_width=True)
bbbbbbx = px.line(custom,x='time',y='rate_APY',render_mode="SVG")
st.plotly_chart(bbbbbbx, use_container_width=True)
bbbbbbb = px.line(custom,x='time',y='accumulated',render_mode="SVG")
st.plotly_chart(bbbbbbb, use_container_width=True)

st.title("misc")
st.write(

max_value_dated_futures,
max_value_perps,
max_value_spot,

min_value_dated_futures,
min_value_perps,
min_value_spot,

spred_dated_BPS,
spred_bps_perps,
spred_bps_spot

)
