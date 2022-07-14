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

exchange = ccxt.bitmex({
    'apiKey': 'NOAb2TuyuLgWkYbXOQGH-x9b',
    'secret': '_fAxf57mItdpX-A5KTxXRzJZY3zkeSKdCGlStwa95FAH81Gd',
})
if 'test' in exchange.urls:
    exchange.urls['api'] = exchange.urls['test'] # ←----- switch the base URL to testnet
x = pd.DataFrame(exchange.load_markets())
symbol = "ETH_USDT"

precision_price = (x[symbol]['precision'])
precision_amount = precision_price['amount']
st.write(precision_amount)
st.write(precision_price)



data = (exchange.fetchOrderBook(symbol)) 

pct_expiry_dated = 0.25
latest_rateAPY_spot = 0.0088
latest_rateAPY_quote = 0.0020
alpha = 0
apy_to_beat = (((1+latest_rateAPY_quote)*(1+latest_rateAPY_spot)))+alpha-1
precision_price = 0.05
precision_amount = 1000000
stink_save_bid_drawdown = 0.75
stink_save_ask_drawup = 1.25




bids = data["bids"]
bids = pd.DataFrame(bids)
bids = bids.rename(columns={0: "price_bid", 1: "size_bid"})
asks = data["asks"]
asks = pd.DataFrame(asks)
asks.reset_index(drop=True, inplace=False)
bids.reset_index(drop = True, inplace=False)
asks = asks.rename(columns={0: "price_ask", 1: "size_ask"})
asks['fixed_size_ask'] = asks['size_ask']/precision_amount
bids['fixed_size_bid'] = bids['size_bid']/precision_amount
asks = asks.drop(columns=['size_ask'])
bids = bids.drop(columns=['size_bid'])
asks = pd.DataFrame(asks)
bids = pd.DataFrame(bids)
asks['accumulated']  = (list(accumulate(asks['fixed_size_ask'])))
asks['accumulated_price']  = (asks['price_ask']) * asks['fixed_size_ask']
asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']
bids['accumulated']  = (list(accumulate(bids['fixed_size_bid'])))
bids['accumulated_price']  = (bids['price_bid']) * bids['fixed_size_bid']
bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']                
for i in range(len(asks)):
    x = asks['price_ask'].iloc[i]
    y = asks['fixed_size_ask'].iloc[i]


bid_new = pd.DataFrame(bids)
bid_new['mm_bid_price']  = round(round(bids['price_bid'] * ((1-((1*((1-(latest_rateAPY_spot*pct_expiry_dated))))*apy_to_beat))*(1*((1-(latest_rateAPY_spot*pct_expiry_dated))))) / precision_price) * precision_price, -int(math.floor(math.log10(precision_price))))
bid_new['mm_bid_size'] = bids['fixed_size_bid'] * precision_amount
bid_new = bid_new.drop(columns=['accumulated', 'accumulated_price', 'accumulated_avg_price','cash_equivelant','price_bid','fixed_size_bid'])
stink_save_bid = bid_new['mm_bid_price'].max()*stink_save_bid_drawdown
bid_new = bid_new[bid_new.mm_bid_price > stink_save_bid]
order_df_bid = pd.DataFrame()
for col_name, data in bid_new.iterrows():
    x = (data['mm_bid_price'])
    y =(data['mm_bid_size'])
    order_init = exchange.createLimitBuyOrder(symbol='ETH_USDT',price=x,amount=y)
    order_df_bid = order_df_bid.append(order_init, ignore_index=True)
order_df_bid['ammount_fixed'] = order_df_bid['amount']/precision_amount
order_df_bid['accumulated']  = (list(accumulate(order_df_bid['ammount_fixed'])))
order_df_bid['accumulated_price']  = (order_df_bid['price']) * order_df_bid['ammount_fixed']
order_df_bid['accumulated_avg_price'] = (list(accumulate(order_df_bid['accumulated_price'])))  / order_df_bid['accumulated']
order_df_bid['cash_equivelant'] = order_df_bid['accumulated'] * order_df_bid['accumulated_avg_price']      
st.write(order_df_bid)
st.plotly_chart(px.bar(order_df_bid,y=order_df_bid['ammount_fixed'], x=order_df_bid['price']))
st.plotly_chart(px.line(order_df_bid,y=order_df_bid['accumulated'], x=order_df_bid['price']))
st.plotly_chart(px.line(order_df_bid,y=order_df_bid['cash_equivelant'], x=order_df_bid['price']))





orders_hist = exchange.fetchOrders()
orders_hist = pd.DataFrame(orders_hist)
# st.write(orders_hist)

# st.write(orders_hist['id'])

orders_hist_id_df = pd.DataFrame(orders_hist['id'])
# st.write(orders_hist_id_df)
id = orders_hist_id_df
order_cancel_df = pd.DataFrame()
cancel_df = pd.DataFrame()
for index, row in id.iterrows():
    order_cancel = exchange.cancelOrder(id=row['id'])
    order_cancel_df = order_cancel_df.append(order_cancel, ignore_index=True).astype(str)
st.write(order_cancel_df)











