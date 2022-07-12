# import ccxt
# import streamlit as st
# import pandas as pd
# exchange = ccxt.bitmex({
#     'apiKey': 'NOAb2TuyuLgWkYbXOQGH-x9b',
#     'secret': '_fAxf57mItdpX-A5KTxXRzJZY3zkeSKdCGlStwa95FAH81Gd',
# })


# if 'test' in exchange.urls:
#     exchange.urls['api'] = exchange.urls['test'] # ←----- switch the base URL to testnet

# symbol='XBTUSD'


# # Symbol = st.text_input('Symbol', 'XBTUSD')
# def fetchTrades_into_df(symbol):
#     exchange.fetchTrades = exchange.fetchTrades(symbol=symbol)
#     fetchTrades = (exchange.fetchTrades)
#     fetchTrades_df = pd.DataFrame(fetchTrades)
#     trade_info = pd.DataFrame()
#     fixed_df = pd.DataFrame()
#     for index, row in fetchTrades_df.iterrows():
#         trade_info = trade_info.append(row['info'],ignore_index=True)
#     fixed_df = pd.merge(fetchTrades_df, trade_info, left_index=True, right_index=True)
#     fixed_df = fixed_df.drop(columns=['info'])
#     st.write(fixed_df)

# # fetchTrades_into_df(symbol='XBTUSD')






# def fetch_my_Trades_into_df(symbol):
#     exchange.fetchMyTrades = exchange.fetchMyTrades(symbol=symbol)
#     fetchMyTrades = (exchange.fetchMyTrades)
#     fetchMyTrades_df = pd.DataFrame(fetchMyTrades)
#     trade_info = pd.DataFrame()
#     fixed_df = pd.DataFrame()
#     for index, row in fetchMyTrades_df.iterrows():
#         trade_info = trade_info.append(row['info'],ignore_index=True)
#     fixed_df = pd.merge(fetchMyTrades_df, trade_info, left_index=True, right_index=True)
#     fixed_df = fixed_df.drop(columns=['info'])
#     st.write(fixed_df)

# # fetch_my_Trades_into_df(symbol='XBTUSD')



# # sooooooo bad and trash
# # def fetchOrderBook_into_df(symbol):
# #     exchange.fetchOrderBook = exchange.fetchOrderBook(symbol=symbol)
# #     fetchOrderBook = (exchange.fetchOrderBook)
# #     fetchOrderBook_df = pd.DataFrame(fetchOrderBook)
# #     st.write(fetchOrderBook_df)
# # fetchOrderBook_into_df(symbol='XBTUSD')





# from datetime import datetime
# import calendar

# def OHLCV_to_df(symbol):
#     now = datetime.utcnow()
#     unixtime = calendar.timegm(now.utctimetuple())
#     since = (unixtime - 60*60) * 1000 # UTC timestamp in milliseconds
#     ohlcv = exchange.fetch_ohlcv(symbol=symbol, timeframe='5m', since=since, limit=12)
#     start_dt = datetime.fromtimestamp(ohlcv[0][0]/1000)
#     end_dt = datetime.fromtimestamp(ohlcv[-1][0]/1000)
#     df = pd.DataFrame(ohlcv, columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
#     df['Time'] = [datetime.fromtimestamp(float(time)/1000) for time in df['Time']]
#     df.set_index('Time', inplace=True)
#     st.write(df)
# OHLCV_to_df(symbol='XBTUSD')
from re import M
import plotly
import random
import plotly.express as px
import ccxt
import json
# import streamlit as st
import pandas as pd
import streamlit as st
exchange = ccxt.bitmex({
    'apiKey': 'NOAb2TuyuLgWkYbXOQGH-x9b',
    'secret': '_fAxf57mItdpX-A5KTxXRzJZY3zkeSKdCGlStwa95FAH81Gd',
})

if 'test' in exchange.urls:
    exchange.urls['api'] = exchange.urls['test'] # ←----- switch the base URL to testnet



    
symbol = st.text_input('Symbol', 'XBTUSD')
side = st.text_input('Side', 'buy')
amount = st.number_input('Amount', 100)
price = st.number_input('Price', 20000)
order_type = st.selectbox('Order Type', ['createMarketSellOrder', 'createMarketBuyOrder', 'createLimitSellOrder', 'createLimitBuyOrder'])

# tick = 1
# sample_mid_price = 100
# sample_max_bid = 99
# # sample_min_ask = 101
# x = [97, 98, 99, 100, 101]

# y = [1, 1, .5, 0, 0]
# st.plotly_chart(px.bar(x=x, y=y))

# st.write(len(x))
# st.write(len(y))


# list_len = st.number_input("lengeth", 1)
# x = [0] * list_len
# st.write(x)
# carry = len(x)
# fix_len = st.number_input("which to fix", 0)
# x[fix_len] = st.number_input("set input", 0)
# st.write(x)

import streamlit as st
import numpy as np
import pandas as pd

# Randomly fill a dataframe and cache it
# multiple_orders = st.button('Multiple Orders')
# if multiple_orders:
order_number = st.number_input('Order Number', 1)
st.write(order_number)
x = order_number
@st.cache(allow_output_mutation=True)
def get_dataframe():
    return pd.DataFrame(
        np.random.randint(x, size=(2, x)),
        columns=('order %d' % i for i in range(x)),
        index = ["price", "size"]
        
        )


df = get_dataframe()

# Create row, column, and value inputs
# row = st.number_input('row', max_value=df.shape[0])
# col = st.number_input('column', max_value=df.shape[1])

y = st.selectbox('column', df.columns)
x = st.selectbox('row', df.index)

col_num = df.columns.get_loc(y)
# st.write(col_num)
row_num = df.index.get_loc(x)
# st.write(row_num)
# row_num = iloc[x]
# col_num

val_check = st.checkbox("change_value")
if val_check:
    value = st.number_input('value')

# Change the entry at (row, col) to the given value
    df.values[row_num][col_num] = value

# And display the result!
st.dataframe(df)
st.write("price",df[y].tolist()[0],"size",df[y].tolist()[1])
# for row, index in df:
#     st.write()


# def get_x2(y):
#     ticks_to_fill = len(y)
#     x_2 = [((sample_mid_price) ** -1) + ((sample_max_bid + sample_mid_price)/2) * i / ticks_to_fill for i in range(ticks_to_fill)]
#     if len(x_2) == len(y):
    
#         st.plotly_chart(px.bar(x=x_2, y=y))
#     return x_2
# get_x2(y)
# qqq = np.random.randint(1, size=(1, 10))
# st.write(qqq)

accesding = st.button('Accessing')
skewed_orders = st.button('Skewed Orders')


if skewed_orders:
    st.write("bids")
    st.write("asks")










if order_type == 'createMarketSellOrder':
    order_check = st.checkbox('Create Market Sell Order')
    if order_check:
        order_init = exchange.create_market_sell_order(symbol=symbol, amount=amount)
        st.write(order_init)
if order_type == 'createMarketBuyOrder':
    order_check = st.checkbox('Order Check')
    if order_check:
        order_init = exchange.createMarketBuyOrder(symbol=symbol,amount=amount)
        st.write(order_init)
if order_type == 'createLimitSellOrder':
    order_check = st.checkbox('Order Check')
    if order_check:
        order_init = exchange.createLimitSellOrder(symbol=symbol,price=price,amount=amount)
        st.write(order_init)
if order_type == 'createLimitBuyOrder':
    order_check = st.checkbox('Order Check')
    if order_check:
        order_init = exchange.createLimitBuyOrder(symbol=symbol,price=price,amount=amount)
        st.write(order_init)
