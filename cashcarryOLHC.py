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
premiums = requests.get('https://ftxpremiums.com/assets/data/premiums.json')
premiums = json.loads(premiums.text)
premiums = pd.DataFrame(premiums)
# print(premiums)
# st.write("cash and carry premiums")
# st.write(premiums)
lending = requests.get('https://ftxpremiums.com/assets/data/lending.json')
lending = json.loads(lending.text)
lending = pd.DataFrame(lending)
# print(lending)    
# st.write("lending rates")

# st.write(lending)
funding = requests.get('https://ftxpremiums.com/assets/data/funding.json')
funding = json.loads(funding.text)
funding = pd.DataFrame(funding)
# print(funding)
# st.write("funding rates")

# st.write(funding)
premiums_names = premiums['name']
# st.write(premiums_names)


lending_names = lending['name']
# st.write(lending_names)

perp_names = funding['name']
# st.write(perp_names)

# names_premeiums = 'BTC/USD'
# @st.cache
# st.title("HERE CREAMY D CLIUVK HERE")
# st.write(names_premeiums)

names_premeiums = st.selectbox("premiums", premiums_names

, index = 8
)
st.write(names_premeiums)
names_lending = st.selectbox("lending", lending_names

# , index = random.randint(0, 100)
)
st.write(names_lending)
name_perp = st.selectbox("nperp", perp_names

# , index = random.randint(0, 10)
)
st.write(name_perp)
# st.write(names_premeiums)
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

# st.write(names_premeiums)
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
bids['accumulated']  = (list(accumulate(bids['size'])))


column = bids["price"]
max_value = column.max()
st.write(max_value)


column = asks["price"]
min_value = column.min()
st.write(min_value)

spred = min_value - max_value
st.write(spred)

spred_pct = spred/min_value*1000
st.write(spred_pct , "bps")
# asks['price'] = asks[0]
# asks['size'] = asks[1]
for i in range(1, 2):
    cols = st.columns(2)
    cols[0].write(bids)
    
    cols[1].write(asks)


aaa = px.line(asks,x='price',y='accumulated')
bbb = px.line(bids,x='price',y='accumulated')
ccc = px.bar(asks,x='price',y='size')
ddd = px.bar(bids,x='price',y='size')

for i in range(1, 2):
    colz = st.columns(2)
    colz[1].plotly_chart(aaa)    
    
    colz[0].plotly_chart(bbb)    
    
for i in range(1, 2):
    colx = st.columns(2)
    colx[1].plotly_chart(ccc)    
    
    colx[0].plotly_chart(ddd)    

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=asks['price'], y=asks['accumulated'], name="asks"),
    secondary_y=False,
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

# from plotly.graph_objs import *
# trace1 = {
#   "mode": "lines+markers", 
#   "name": "bid", 
#   "type": "scatter", 
#   "x": bid['price'], 
#   "y": bid['size']
# }
# trace2 = {
#   "mode": "lines+markers", 
#   "name": "ask", 
#   "type": "scatter", 
#   "x": ask['price'], 
#   "y": ask['size']
# }
# data = Data([trace1, trace2])
# layout = {
#   "title": "Limited Order Book", 
#   "xaxis": {"title": "price"}, 
#   "yaxis": {"title": "amount"}
# }
# fig = Figure(data=data, layout=layout)
# st.plotly_chart(fig)

# st.bar_chart(bids)

# st.write(asks)
# # st.write(asks.columns)
# # asks.rename(index=str).index
# # st.write(asks.index)
# st.write(bids)
# st.write(bids.columns)














st.write(names_lending)

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
bids['accumulated']  = (list(accumulate(bids['size'])))


column = bids["price"]
max_value = column.max()
st.write(max_value)


column = asks["price"]
min_value = column.min()
st.write(min_value)

spred = min_value - max_value
st.write(spred)

spred_pct = spred/min_value*1000
st.write(spred_pct , "bps")
# asks['price'] = asks[0]
# asks['size'] = asks[1]
for i in range(1, 2):
    cols = st.columns(2)
    cols[0].write(bids)
    
    cols[1].write(asks)

    
aaa = px.line(asks,x='price',y='accumulated')
bbb = px.line(bids,x='price',y='accumulated')
ccc = px.bar(asks,x='price',y='size')
ddd = px.bar(bids,x='price',y='size')

for i in range(1, 2):
    colz = st.columns(2)
    colz[1].plotly_chart(aaa)    
    
    colz[0].plotly_chart(bbb)    
    
for i in range(1, 2):
    colx = st.columns(2)
    colx[1].plotly_chart(ccc)    
    
    colx[0].plotly_chart(ddd)    

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=asks['price'], y=asks['accumulated'], name="asks"),
    secondary_y=False,
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
bids['accumulated']  = (list(accumulate(bids['size'])))


column = bids["price"]
max_value = column.max()
st.write(max_value)


column = asks["price"]
min_value = column.min()
st.write(min_value)

spred = min_value - max_value
st.write(spred)

spred_pct = spred/min_value*1000
st.write(spred_pct , "bps")
# asks['price'] = asks[0]
# asks['size'] = asks[1]
for i in range(1, 2):
    cols = st.columns(2)
    cols[0].write(bids)
    
    cols[1].write(asks)

    
aaa = px.line(asks,x='price',y='accumulated')
bbb = px.line(bids,x='price',y='accumulated')
ccc = px.bar(asks,x='price',y='size')
ddd = px.bar(bids,x='price',y='size')

for i in range(1, 2):
    colz = st.columns(2)
    colz[1].plotly_chart(aaa)    
    
    colz[0].plotly_chart(bbb)    
    
for i in range(1, 2):
    colx = st.columns(2)
    colx[1].plotly_chart(ccc)    
    
    colx[0].plotly_chart(ddd)    

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=asks['price'], y=asks['accumulated'], name="asks"),
    secondary_y=False,
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

st.write("Predicted funding rate. Longs pay shorts if positive, shorts pay longs if negative. 1/24 times the average premium over the hour.")
custom = requests.get(f"https://ftxpremiums.com/assets/data/funding_data/{name_perp}.json").json()

custom = pd.DataFrame(custom)
custom['rate'] = custom['rate'].astype(float)
custom['time'] =  pd.to_datetime(custom['time'], unit='s')
custom = custom.sort_values(by="time")

custom['rate'] = custom['rate'] * 1000
custom['accumulated']  = (list(accumulate(custom['rate'])))
st.write('hourly funding rate in basis points')
bbbbbb = px.line(custom,x='time',y='rate',render_mode="SVG")
st.plotly_chart(bbbbbb, use_container_width=True)
bbbbbbb = px.line(custom,x='time',y='accumulated',render_mode="SVG")
st.plotly_chart(bbbbbbb, use_container_width=True)


# names_premeiums = st.selectbox("premiums", premiums_names

# , index = 1
# # random.randint(0, 100)
# )
# st.write(names_premeiums)
# st.markdown(
#     '''
# import streamlit as st
# import requests
# import json
# import pandas as pd
# import math
# import time
# from itertools import accumulate
# # from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# from itertools import chain

# import plotly.express as px
# from datetime import datetime
# # ts = int('1645598410')

# # print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
# import json
# import requests
# import pandas as pd
# import random

# premiums = requests.get('https://ftxpremiums.com/assets/data/premiums.json')
# premiums = json.loads(premiums.text)
# premiums = pd.DataFrame(premiums)
# # print(premiums)
# st.write("cash and carry premiums")
# st.write(premiums)
# lending = requests.get('https://ftxpremiums.com/assets/data/lending.json')
# lending = json.loads(lending.text)
# lending = pd.DataFrame(lending)
# # print(lending)    
# st.write("lending rates")

# st.write(lending)
# funding = requests.get('https://ftxpremiums.com/assets/data/funding.json')
# funding = json.loads(funding.text)
# funding = pd.DataFrame(funding)
# # print(funding)
# st.write("funding rates")

# st.write(funding)
# premiums_names = premiums['name']
# st.write(premiums_names)


# lending_names = lending['name']
# st.write(lending_names)

# perp_names = lending['name']
# st.write(perp_names)


# # @st.cache
# st.title("HERE CREAMY D CLIUVK HERE")
# names_premeiums = st.selectbox("premiums", premiums_names, format_func=lambda x: 'Select an option' if x == '' else x)
# st.write(names_premeiums)
# # page.write(lending_names)

# # custom_lending = requests.get(f"https://ftx.com/api/spot_margin/history?coin={NAME_LENDING}&start_time=960368456&end_time=1854597556").json()
# # custom_lending = pd.DataFrame(custom_lending['result'])
# # st.write(custom_lending)



# # df = requests.get(f"https://ftx.com/api/markets/{NAME_LENDING}-PERP/candles?resolution=14400").json()
# # df = pd.DataFrame(df['result'])

# # # st.write(df)
# # # Create figure with secondary y-axis
# # fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
# #             vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
# #             row_width=[0.2, 0.7])

# # # include candlestick with rangeselector
# # fig.add_trace(go.Candlestick(x=df['startTime'],open=df['open'], high=df['high'],low=df['low'], close=df['close'],name="OHLC"), row=1, col=1)

# # # include a go.Bar trace for volumes
# # fig.add_trace(go.Bar(x=df['startTime'], y=df['volume'],
# #             showlegend=False), row=2, col=1)

# # fig.update(layout_xaxis_rangeslider_visible=False)
# # st.plotly_chart(fig)


# # df = requests.get(f"https://ftx.com/api/markets/{NAME_LENDING}/USD/candles?resolution=14400").json()
# # df = pd.DataFrame(df['result'])

# # # st.write(df)
# # # Create figure with secondary y-axis
# # fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
# #             vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
# #             row_width=[0.2, 0.7])

# # # include candlestick with rangeselector
# # fig.add_trace(go.Candlestick(x=df['startTime'],open=df['open'], high=df['high'],low=df['low'], close=df['close'],name="OHLC"), row=1, col=1)

# # # include a go.Bar trace for volumes
# # fig.add_trace(go.Bar(x=df['startTime'], y=df['volume'],
# #             showlegend=False), row=2, col=1)

# # fig.update(layout_xaxis_rangeslider_visible=False)
# # st.plotly_chart(fig)


# df = requests.get(f"https://ftx.com/api/markets/{names_premeiums}/candles?resolution=14400").json()
# # st.write(df)
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

# df1 = requests.get(f"https://ftx.com/api/markets/{names_premeiums}/orderbook?depth=100").json()
# df1 = pd.DataFrame(df1)
# df1 = df1['result']
# asks = df1['asks']
# bids = df1['bids']

# # rename collums
# # plot depth
# # pick orders
# # pragnate orders into ccxt
# # exec


# # loop later to show postioning
# asks = pd.DataFrame(asks)
# bids = pd.DataFrame(bids)
# # st.write(df1)
# st.write(asks)
# st.write(bids)



# '''
# )