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
from datetime import datetime, timedelta
# ts = int('1645598410')

# print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
import json
import requests
import pandas as pd
import random
st.set_page_config(layout="wide")



# st.text('comments 1')
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
expiry = names_premeiums.split('-')[1]
expiry = pd.to_datetime(expiry, format='%m%d')
# """ year is the same as this year"""
expiry = expiry.replace(year=datetime.now().year)
st.write("expiry date", expiry)

# expiry = datetime.datetime.strftime(expiry,'%m%d')
days_until_expiry = expiry - datetime.now()
# """between now and expiry"""

# st.write(int(datetime.now().('%m%d'strftime)))
# days_until_expiry = ((expiry).strftime('%m%d')) - (datetime.now().strftime('%m%d'))
st.write("now",datetime.now())
st.write("days until expiry: ", days_until_expiry)
st.write("add the amount of funding events until expiry ")


pct_expiry_dated = days_until_expiry.days / 365 * 100
st.write("expiry time - pct of a year: ", pct_expiry_dated, "%")






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
asks['accumulated_size']  = (list(accumulate(asks['size'])))
asks['accumulated_price']  = (asks['price']) * asks['size']
asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated_size']
asks['cash_equivelant'] = asks['accumulated_size'] * asks['accumulated_avg_price']


bids['accumulated_size']  = (list(accumulate(bids['size'])))
bids['accumulated_price']  = (bids['price']) * bids['size']
bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated_size']
bids['cash_equivelant'] = bids['accumulated_size'] * bids['accumulated_avg_price']
column = bids["price"]
max_value_spot = column.max()
st.write("now",datetime.now())
st.write("best bid", max_value_spot)

column = asks["price"]
min_value_spot = column.min()
st.write("best ask", min_value_spot)

spred_spot = min_value_spot - max_value_spot
st.write("spot spread", spred_spot)

spred_bps_spot = spred_spot/min_value_spot*1000
st.write("spred_bps", spred_bps_spot , "bps")
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
custom_lending['rate_bps_hr'] = custom_lending['rate'] * 1000
custom_lending['accumulated']  = (list(accumulate(custom_lending['rate_bps_hr'])))

window = st.sidebar.slider('window size (periods for rolling average)', 1, 250, 20)
no_of_std = st.sidebar.slider('number of standard deviations', 1, 5, 2)
def bollinger_strat(custom_lending, window, no_of_std):
    rolling_mean = custom_lending['rateAPY'].rolling(window).mean()
    rolling_std = custom_lending['rateAPY'].rolling(window).std()
    custom_lending['rolling_mean'] = rolling_mean

    custom_lending['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
    custom_lending['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
    return custom_lending['Bollinger High'] , custom_lending['Bollinger Low'], custom_lending['rolling_mean'] 
bollinger_strat(custom_lending,window,no_of_std)
bbbbbbb = px.line(custom_lending,x='time',y=['Bollinger High','Bollinger Low','rateAPY','rolling_mean'],render_mode="SVG")
st.plotly_chart(bbbbbbb, use_container_width=True)





def bollinger_strat(custom_lending, window, no_of_std):
    rolling_mean = custom_lending['size'].rolling(window).mean()
    rolling_std = custom_lending['size'].rolling(window).std()
    custom_lending['rolling_mean'] = rolling_mean

    custom_lending['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
    custom_lending['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
    return custom_lending['Bollinger High'] , custom_lending['Bollinger Low'], custom_lending['rolling_mean'] 
bollinger_strat(custom_lending,window,no_of_std)
bbbbbbb = px.line(custom_lending,x='time',y=['Bollinger High','Bollinger Low','size','rolling_mean'],render_mode="SVG")
st.plotly_chart(bbbbbbb, use_container_width=True)







def bollinger_strat(custom_lending, window, no_of_std):
    rolling_mean = custom_lending['accumulated'].rolling(window).mean()
    rolling_std = custom_lending['accumulated'].rolling(window).std()
    custom_lending['rolling_mean'] = rolling_mean

    custom_lending['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
    custom_lending['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
    return custom_lending['Bollinger High'] , custom_lending['Bollinger Low'], custom_lending['rolling_mean'] 
bollinger_strat(custom_lending,window,no_of_std)
bbbbbbb = px.line(custom_lending,x='time',y=['Bollinger High','Bollinger Low','accumulated','rolling_mean'],render_mode="SVG")
st.plotly_chart(bbbbbbb, use_container_width=True)



# aaa = px.line(custom_lending,x='time',y='rateAPY',render_mode="SVG")
# st.plotly_chart(aaa, use_container_width=True)
# aa = px.line(custom_lending,x='time',y='size',render_mode="SVG")
# st.plotly_chart(aa, use_container_width=True)
# a = px.line(custom_lending,x='time',y='interest',render_mode="SVG")
# st.plotly_chart(a, use_container_width=True)

def bollinger_strat(custom_lending, window, no_of_std):
    rolling_mean = custom_lending['interest'].rolling(window).mean()
    rolling_std = custom_lending['interest'].rolling(window).std()
    custom_lending['rolling_mean'] = rolling_mean

    custom_lending['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
    custom_lending['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
    return custom_lending['Bollinger High'] , custom_lending['Bollinger Low'], custom_lending['rolling_mean'] 
bollinger_strat(custom_lending,window,no_of_std)
bbbbbbb = px.line(custom_lending,x='time',y=['Bollinger High','Bollinger Low','interest','rolling_mean'],render_mode="SVG")
st.plotly_chart(bbbbbbb, use_container_width=True)


def bollinger_strat(custom_lending, window, no_of_std):
    rolling_mean = custom_lending['rate_bps_hr'].rolling(window).mean()
    rolling_std = custom_lending['rate_bps_hr'].rolling(window).std()
    custom_lending['rolling_mean'] = rolling_mean

    custom_lending['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
    custom_lending['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
    return custom_lending['Bollinger High'] , custom_lending['Bollinger Low'], custom_lending['rolling_mean'] 
bollinger_strat(custom_lending,window,no_of_std)
bbbbbbb = px.line(custom_lending,x='time',y=['Bollinger High','Bollinger Low','rate_bps_hr','rolling_mean'],render_mode="SVG")
st.plotly_chart(bbbbbbb, use_container_width=True)






# st.write('hourly funding rate in basis points')
# bbbbbb = px.line(custom_lending,x='time',y='rate_bps_hr',render_mode="SVG")
# st.plotly_chart(bbbbbb, use_container_width=True)
# bbbbbbb = px.line(custom_lending,x='time',y='accumulated',render_mode="SVG")
# st.plotly_chart(bbbbbbb, use_container_width=True)






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

now = datetime.now()
next_hour = now + timedelta(hours=1)
# st.write(now)
# st.write(next_hour)
date = datetime.strptime(str(next_hour), '%Y-%m-%d %H:%M:%S.%f')
newdate = date.replace(minute=0,second=0)
# newdate = date.replace(second=0)

# st.write(date)
# st.write(newdate)
time_till_expiry = newdate - now
st.write("time till expiry", time_till_expiry)

pct_expiry = (time_till_expiry.total_seconds() / 3600) / 24 / 365.24 * 100
st.write("percentage till expiry", pct_expiry, "%")


# st.write(hour)
# expiry = pd.to_datetime(hour, format='%m%d')
# st.write(expiry)
column = bids["price"]
max_value_perps = column.max()
st.write("best bid perps", max_value_perps)


column = asks["price"]
min_value_perps = column.min()
st.write("best bid asks", min_value_perps)

spred_perps = min_value_perps - max_value_perps
st.write("perp spread",spred_perps)

spred_bps_perps = spred_perps/min_value_perps*1000
st.write("perp spread", spred_bps_perps , "bps")
# asks['price'] = asks[0]
# asks['size'] = asks[1]
for i in range(1, 2):
    cols = st.columns(2)
    cols[0].subheader('bids')

    cols[0].write(bids)
    cols[1].subheader('asks')
    
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








def bollinger_strat(custom, window, no_of_std):
    rolling_mean = custom['rate_APY'].rolling(window).mean()
    rolling_std = custom['rate_APY'].rolling(window).std()
    custom['rolling_mean'] = rolling_mean

    custom['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
    custom['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
    return custom['Bollinger High'] , custom['Bollinger Low'], custom['rolling_mean'] 
bollinger_strat(custom,window,no_of_std)
bbbbbbb = px.line(custom,x='time',y=['Bollinger High','Bollinger Low','rate_APY','rolling_mean'],render_mode="SVG")
st.plotly_chart(bbbbbbb, use_container_width=True)




st.write('hourly funding rate in basis points')


def bollinger_strat(custom, window, no_of_std):
    rolling_mean = custom['rate'].rolling(window).mean()
    rolling_std = custom['rate'].rolling(window).std()
    custom['rolling_mean'] = rolling_mean

    custom['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
    custom['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
    return custom['Bollinger High'] , custom['Bollinger Low'], custom['rolling_mean'] 
bollinger_strat(custom,window,no_of_std)
bbbbbbb = px.line(custom,x='time',y=['Bollinger High','Bollinger Low','rate','rolling_mean'],render_mode="SVG")
st.plotly_chart(bbbbbbb, use_container_width=True)


def bollinger_strat(custom, window, no_of_std):
    rolling_mean = custom['accumulated'].rolling(window).mean()
    rolling_std = custom['accumulated'].rolling(window).std()
    custom['rolling_mean'] = rolling_mean

    custom['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
    custom['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
    return custom['Bollinger High'] , custom['Bollinger Low'], custom['rolling_mean'] 
bollinger_strat(custom,window,no_of_std)
bbbbbbb = px.line(custom,x='time',y=['Bollinger High','Bollinger Low','accumulated','rolling_mean'],render_mode="SVG")
st.plotly_chart(bbbbbbb, use_container_width=True)







# try and do rolling average and rolling stddev











st.title("misc")
st.write("dated:",names_premeiums)
st.write("spot:",names_lending)
st.write("perp:", name_perp)
numbers = len(names_lending)
st.write(numbers)
# """verify that names_premiums, names_lending, name_perp are the same asset by looking at the fist 4 letters"""
def spelling(numbers, names_premiums, names_lending, name_perp):
    if names_premiums[:numbers] == names_lending[:numbers] and names_premiums[:numbers] == name_perp[:4]:
        return True
    else:
        return False
a = spelling(numbers, names_premeiums, names_lending, name_perp)
st.write("are the assets the same?",a)
st.subheader("dated futures")
st.write("best bid dated futures", max_value_dated_futures)
st.write("best ask dated futures", min_value_dated_futures)
st.write("spread dated futures", spred_dated)
st.write("spread dated futures", spred_dated_BPS, "bps")
st.write("expiry date", expiry)
st.write("now",datetime.now())
st.write("days until expiry: ", days_until_expiry)
st.write("expiry time - pct of a year: ", pct_expiry_dated, "%")


st.subheader("lending/spot")
latest_rateAPY_spot = custom_lending['rateAPY'].iloc[-1]
st.write("latest rate APY", latest_rateAPY_spot)
latest_rate_bps_hr = custom_lending['rate_bps_hr'].iloc[-1]
st.write("rate_bps_hr", latest_rate_bps_hr)
st.write("now",datetime.now())
st.write("best bid", max_value_spot)
st.write("best ask", min_value_spot)
st.write("spot spread", spred_spot)
st.write("spred_bps", spred_bps_spot , "bps")





st.subheader("funding/perpetual")
latest_rateAPY = custom['rate_APY'].iloc[-1]
st.write("latest rate APY", latest_rateAPY)
latest_rate_bps_hr = custom['rate'].iloc[-1]
st.write("rate_bps_hr", latest_rate_bps_hr)
st.write("time till expiry", time_till_expiry)
st.write("percentage till expiry", pct_expiry, "%")
st.write("best bid perps", max_value_perps)
st.write("best bid asks", min_value_perps)
st.write("perp spread",spred_perps)
st.write("perp spread", spred_bps_perps , "bps")
st.subheader("""first we look at spot vs dated """)
st.write("sell", min_value_dated_futures, "dated_future", "buy", max_value_spot, "spot")

calculated_income_by_lending = (max_value_spot * (1 + ((latest_rateAPY_spot/100)*(pct_expiry_dated/100))))
# st.write(calculated_income_by_lending)
PREMIUM = (min_value_dated_futures - calculated_income_by_lending) 
# * (1 - latest_rateAPY)
PREMIUM_APY = PREMIUM / (max_value_spot * (pct_expiry_dated/100)) * 100

st.write(PREMIUM_APY, "% APY")





# st.write(PREMIUM_APY)
# """previous formula has to be accrued hourly not daily """


# """verify the profitavilty of the cash and carry"""

# """first we look at spot vs dated """


# """next we look at spot vs perp """



# """third we look at dated vs perp """
