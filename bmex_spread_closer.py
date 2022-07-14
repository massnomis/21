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
st.set_page_config(layout="wide")

exchange = ccxt.bitmex({
    'apiKey': 'NOAb2TuyuLgWkYbXOQGH-x9b',
    'secret': '_fAxf57mItdpX-A5KTxXRzJZY3zkeSKdCGlStwa95FAH81Gd',
})
if 'test' in exchange.urls:
    exchange.urls['api'] = exchange.urls['test'] # ←----- switch the base URL to testnet



orders_hist = exchange.fetchOpenOrders()
orders_hist = pd.DataFrame(orders_hist)

if orders_hist.empty:
    st.write('no open orders')
else:
    st.write(orders_hist)
    orders_hist = orders_hist[orders_hist.status != 'canceled']
    orders_hist = orders_hist[orders_hist.status != 'closed']
    orders_hist_id_df = pd.DataFrame(orders_hist['id'])
    # st.write(orders_hist)
    id = orders_hist_id_df
    order_cancel_df = pd.DataFrame()
    cancel_df = pd.DataFrame()

    for index, row in id.iterrows():
        order_cancel = exchange.cancelOrder(id=row['id'])
        order_cancel_df = order_cancel_df.append(order_cancel, ignore_index=True).astype(str)
    st.write("canceled, yalla")
    # st.write(order_cancel_df)



load_makets_for_data = pd.DataFrame(exchange.load_markets()).astype(str)
# load_makets_for_data = load_makets_for_data[load_makets_for_data.active != 'False']

# st.write(load_makets_for_data)


symbol = "LINK_USDT"
# st.write(load_makets_for_data.columns)

# pct_expiry_dated = 0.25
# latest_rateAPY_spot = 0.0088
# latest_rateAPY_quote = 0.0020
# alpha = 0
# apy_to_beat = (((1+latest_rateAPY_quote)*(1+latest_rateAPY_spot)))+alpha-1
orders_to_place_a_side = 5 
stink_save_bid_drawdown = 0.98
stink_save_ask_drawup = 1.05

precision_load = pd.DataFrame(exchange.load_markets())
precision = (precision_load[symbol]['precision'])
# st.write(precision)
precision_amount = precision['amount']
precision_price = precision['price']
st.write(precision_amount, precision_price)
data = (exchange.fetchOrderBook(symbol)) 





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
st.write(bids, asks)

bid_new = pd.DataFrame(bids)
bid_new['mm_bid_price']  = bids['price_bid'].max() + precision_price
bid_new['mm_bid_size'] = precision_amount
bid_new = bid_new.drop(columns=['accumulated', 'accumulated_price', 'accumulated_avg_price','cash_equivelant','price_bid','fixed_size_bid'])
# st.write(bid_new)
stink_save_bid = bid_new['mm_bid_price'].max()*stink_save_bid_drawdown
bid_new = bid_new[bid_new.mm_bid_price > stink_save_bid]
# st.write(bid_new)

order_df_bid = pd.DataFrame()
i = 0


testing_bids = pd.DataFrame(columns=['price_bid', 'size_bid'], index=range(0, orders_to_place_a_side))
testing_bids.loc[-1] = [bid_new['mm_bid_price'].max(), precision_amount]  # adding a row
testing_bids.index = testing_bids.index + 1  # shifting index
testing_bids = testing_bids.sort_index() 

st.write(testing_bids)

st.write(bid_new)


for col_name, data in bid_new.iterrows():
    while i < orders_to_place_a_side:

        mm_bid_price = (data['mm_bid_price']) + (precision_price * i)
        mm_bid_size = (data['mm_bid_size'])
        order_init = exchange.createLimitBuyOrder(symbol=symbol,price=mm_bid_price,amount=mm_bid_size)
        order_df_bid = order_df_bid.append(order_init, ignore_index=True)
        i += 1
st.write(order_df_bid)
bid_new['mm_bid_size'] = bid_new['mm_bid_size']/precision_amount
bid_new['accumulated']  = (list(accumulate(bid_new['mm_bid_size'])))
bid_new['accumulated_price']  = (bid_new['mm_bid_price']) * bid_new['mm_bid_size']
bid_new['accumulated_avg_price'] = (list(accumulate(bid_new['accumulated_price'])))  / bid_new['accumulated']
bid_new['cash_equivelant'] = bid_new['accumulated'] * bid_new['accumulated_avg_price']      
# st.write(bid_new)
# st.plotly_chart(px.bar(bid_new,y=bid_new['mm_bid_size'], x=bid_new['mm_bid_price']))
# st.plotly_chart(px.line(bid_new,y=bid_new['accumulated'], x=bid_new['mm_bid_price']))
# st.plotly_chart(px.line(bid_new,y=bid_new['cash_equivelant'], x=bid_new['mm_bid_price']))










steps = (asks['price_ask'].min() - bids['price_bid'].max()) / precision_price
st.write(steps)








ask_new = pd.DataFrame(asks)
ask_new['mm_ask_price']  = asks['price_ask'].min() - precision_price
# + 400
ask_new['mm_ask_size'] = precision_amount
ask_new = ask_new.drop(columns=['accumulated', 'accumulated_price', 'accumulated_avg_price','cash_equivelant','price_ask','fixed_size_ask'])
# st.write(ask_new)
stink_save_ask = ask_new['mm_ask_price'].min()*stink_save_ask_drawup
# st.write(stink_save_ask)
ask_new = ask_new[ask_new.mm_ask_price < stink_save_ask]
st.write(ask_new)


order_df_ask = pd.DataFrame()

ref_ask = asks['price_ask'].min() - precision_price
ref_ask_size = precision_amount

testing_asks = pd.DataFrame(columns=['price_ask', 'size_ask'])
st.write(testing_asks)
ii = 0


for col_name, data in ask_new.iterrows():
    while i < orders_to_place_a_side:

        mm_ask_price = (data['mm_ask_price']) - (precision_price * i)
        mm_ask_size = (data['mm_ask_size'])
        order_init = exchange.createLimitSellOrder(symbol=symbol,price=mm_bid_price,amount=mm_bid_size)
        order_df_ask = order_df_bid.append(order_init, ignore_index=True)
        ii += 1

st.write(order_df_ask)

ask_new['mm_ask_size'] = ask_new['mm_ask_size']/precision_amount
ask_new['accumulated']  = (list(accumulate(ask_new['mm_ask_size'])))
ask_new['accumulated_price']  = (ask_new['mm_ask_price']) * ask_new['mm_ask_size']
ask_new['accumulated_avg_price'] = (list(accumulate(ask_new['accumulated_price'])))  / ask_new['accumulated']
ask_new['cash_equivelant'] = ask_new['accumulated'] * ask_new['accumulated_avg_price']      




fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=asks['price_ask'], y=asks['accumulated'], name="asks"),secondary_y=True,)
fig.add_trace(go.Scatter(x=bids['price_bid'], y=bids['accumulated'], name="bids"),secondary_y=True,)
fig.update_layout(title_text="orderbook")
st.plotly_chart(fig, use_container_width=True)
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(x=bids['price_bid'], y=bids['fixed_size_bid'], name="bids"),secondary_y=True,)
fig.add_trace(go.Bar(x=asks['price_ask'], y=asks['fixed_size_ask'], name="asks"),secondary_y=True,)
fig.update_layout(title_text="orderbook")
st.plotly_chart(fig, use_container_width=True)
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=asks['accumulated_avg_price'], y=asks['cash_equivelant'], name="asks"),secondary_y=True,)
fig.add_trace(go.Scatter(x=bids['accumulated_avg_price'], y=bids['cash_equivelant'], name="bids"),secondary_y=True,)
fig.update_layout(title_text="cash_equivelant")
st.plotly_chart(fig, use_container_width=True)
st.write("above is them, below is us")
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=ask_new['mm_ask_price'], y=ask_new['accumulated'], name="asks"),secondary_y=True,)
fig.add_trace(go.Scatter(x=bid_new['mm_bid_price'], y=bid_new['accumulated'], name="bids"),secondary_y=True,)
fig.update_layout(title_text="orderbook")
st.plotly_chart(fig, use_container_width=True)
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(x=ask_new['mm_ask_price'], y=ask_new['accumulated'], name="asks"),secondary_y=True,)
fig.add_trace(go.Bar(x=bid_new['mm_bid_price'], y=bid_new['accumulated'], name="bids"),secondary_y=True,)
fig.update_layout(title_text="orderbook")
st.plotly_chart(fig, use_container_width=True)
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=ask_new['accumulated_avg_price'], y=ask_new['mm_ask_size'], name="asks"),secondary_y=True,)
fig.add_trace(go.Scatter(x=bid_new['accumulated_avg_price'], y=bid_new['mm_bid_size'], name="bids"),secondary_y=True,)
fig.update_layout(title_text="orderbook")
st.plotly_chart(fig, use_container_width=True)




