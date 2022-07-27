import asyncio
import websockets
import json
import streamlit as st
import time
import plotly.express as px
import pandas as pd
from itertools import accumulate, chain
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ccxt
import numpy as np
import requests
from datetime import datetime, timedelta
import math
st.set_page_config(layout="wide")
exchange = ccxt.ftx({
    'apiKey': '6lPPRFX1r4x_6ENY6GnhgYr3AdPv34x8Bc-MRH_V',
    'secret': 'OnQqs_nox4NS2OYm5z8ulXJ9rMkbOo5_nNwGe53V',
})

placeholder = st.empty()
placeholder2 = st.empty()
placeholder3 = st.empty()
placeholder4 = st.empty()
placeholder5 = st.empty()
placeholder6 = st.empty()
placeholder7 = st.empty()
placeholder8 = st.empty()
placeholder9 = st.empty()
placeholder10 = st.empty()
placeholder11 = st.empty()
placeholder12 = st.empty()
placeholder13 = st.empty()
placeholder14 = st.empty()
placeholder15 = st.empty()

def ordering_bids(bids, symbol, orders_to_place_a_side_bid, stink_save_bid_drawdown):
    # def precision(symbol):
    precision_load = pd.DataFrame(exchange.load_markets())
    precision = (precision_load[symbol]['precision'])
    precision_amount = precision['amount']
    precision_price = precision['price']
        # return precision_amount, precision_price
    # precision(symbol)

    orders_hist = exchange.fetchOpenOrders()
    orders_hist = pd.DataFrame(orders_hist)
    # with placeholder11:
    if orders_hist.empty:
        # st.write('no open orders')
        pass
    else:
        orders_hist = orders_hist[orders_hist.status != 'canceled']
        orders_hist = orders_hist[orders_hist.status != 'closed']
        if len(orders_hist) > ((orders_to_place_a_side_bid)/2) * 3:
            cancelAllOrders = exchange.cancelAllOrders()
            # st.write("canceled, yalla")
            pass
        else:
            # st.write("no orders to cancel")
            pass
    i = 0
    ii = 0
    bid_new = pd.DataFrame(bids)
    bid_new['mm_bid_price']  = bids['price_bid'].max() + precision_price
    bid_new['mm_bid_size'] = precision_amount
    bid_new = bid_new.drop(columns=['size_bid', 'accumulated', 'accumulated_price', 'accumulated_avg_price','cash_equivelant','price_bid'])

    # st.write(bid_new)
    while i < orders_to_place_a_side_bid:
        for row, data in bid_new.iterrows():
            data['mm_bid_price'] = data['mm_bid_price'] - precision_price * i
            i = i + 1
        # i = i + 1
    # st.write(i)

    yes = requests.get("https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2&toTokenAddress=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&amount=10000000000000000").json()    
    a = int(yes['toTokenAmount'])/int(yes['fromTokenAmount']) * 1000000000000
    # st.write(a)
    bid_new = bid_new[bid_new.mm_bid_price < a]
    bid_new = bid_new.reset_index(drop=True)
    bid_new = bid_new.sort_values(by=['mm_bid_price'], inplace=False)
    bid_new = bid_new.reset_index(drop=True)
    stink_save_bid = bid_new['mm_bid_price'].max()*stink_save_bid_drawdown
    # st.write(stink_save_bid)
    bid_new = bid_new[bid_new.mm_bid_price > stink_save_bid]
    bid_new = bid_new.reset_index(drop=True)

    # st.write(bid_new)
    st.write(bid_new)

    params = {'timeInForce' : 'PO'}
    for row, data in bid_new.iterrows():
        mm_bid_price = (data['mm_bid_price'])
        mm_bid_size = (data['mm_bid_size']) 
        order_init_bid = exchange.createLimitBuyOrder(symbol=symbol,price=mm_bid_price,amount=mm_bid_size, params = params)
    return bid_new

def fix_df(bids, asks):
    asks = pd.DataFrame(asks)
    bids = pd.DataFrame(bids)
    asks['accumulated']  = (list(accumulate(asks['size_ask'])))
    asks['accumulated_price']  = (asks['price_ask']) * asks['size_ask']
    asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
    asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']
    bids['accumulated']  = (list(accumulate(bids['size_bid'])))
    bids['accumulated_price']  = (bids['price_bid']) * bids['size_bid']
    bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
    bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']   
    return bids, asks




def update_asks(asks_update, asks):
    for i in range(len(asks_update)):
        asks.loc[asks["price_ask"] == asks_update.loc[i]["price_ask"], "size_ask"] = asks_update.loc[i]["size_ask"]
        asks.dropna(inplace=True)
        asks = asks.append(asks_update, ignore_index=True)
        asks = asks.drop_duplicates(subset=['price_ask'], keep='first')
        asks.sort_values(by=['price_ask'], inplace=True)
        asks.reset_index(drop = True, inplace=False)
        asks.loc[asks["price_ask"] == asks_update.loc[i]["price_ask"], "size_ask"] = asks_update.loc[i]["size_ask"]
    return asks, asks_update

def update_bids(bids_update, bids):
    for i in range(len(bids_update)):
        bids.reset_index(drop=True)
        bids.loc[bids["price_bid"] == bids_update.loc[i]["price_bid"], "size_bid"] = bids_update.loc[i]["size_bid"]
        bids.dropna(inplace=True)
        bids = bids.append(bids_update, ignore_index=True)
        bids = bids.drop_duplicates(subset=['price_bid'], keep='first')
        bids.sort_values(by=['price_bid'], inplace=True, ascending=False)
        bids.reset_index(drop=True, inplace=False)
        bids.loc[bids["price_bid"] == bids_update.loc[i]["price_bid"], "size_bid"] = bids_update.loc[i]["size_bid"]
    return bids, bids_update








orders_to_place_a_side_bid = st.number_input('Orders to place bid',0,100, value= 4)
stink_save_bid_drawdown_bps = st.number_input('Bid drawdown',1,10000,value= 5)
stink_save_bid_drawdown = 1 - (stink_save_bid_drawdown_bps/10000)


a = "Subscribed to orderbook"

b = "fat d8ta"

dict_dumps = {
  "op": "subscribe",
  "channel": "orderbook",
  "market": "ETH/USD"
}
symbol = "ETH/USD"

placeholder1 = st.empty()
async def consumer() -> None:
    async with websockets.connect("wss://ftx.com/ws/", ping_interval=20, ping_timeout=2000) as websocket:
        await websocket.send(
            json.dumps(
                dict_dumps
            )
        )
        async for message in websocket:
            global a
            global b
            global name
            global orders_to_place_a_side_bid
            global stink_save_bid_drawdown
            global symbol
            message = json.loads(message)
            with placeholder1.container():
                if message["type"] == "subscribed":
                    st.write(a, use_container_width=True)
                if message["type"] == "partial":
                    market = message["market"]
                    type = message["type"]
                    channel = message["channel"]
                    data = message["data"]
                    time  = data["time"]
                    checksum = data["checksum"]
                    bids = data["bids"]
                    bids = pd.DataFrame(bids)
                    bids = bids.rename(columns={0: "price_bid", 1: "size_bid"})
                    asks = data["asks"]
                    asks = pd.DataFrame(asks)
                    asks.reset_index(drop=True, inplace=False)
                    bids.reset_index(drop = True, inplace=False)
                    asks = asks.rename(columns={0: "price_ask", 1: "size_ask"})
                    action = data["action"]
                if message["type"] == "update":
                    st.write(b, use_container_width=True)
                    type_update = message["type"]
                    channel_update = message["channel"]
                    data_update = message["data"]
                    time_update  = data_update["time"]
                    checksum = data_update["checksum"]
                    bids_update = pd.DataFrame(data_update["bids"])
                    bids_update = bids_update.rename(columns={0: "price_bid", 1: "size_bid"})
                    asks_update = pd.DataFrame(data_update["asks"])
                    asks_update = asks_update.rename(columns={0: "price_ask", 1: "size_ask"})
                    action = data_update["action"]
                    update_asks(asks_update, asks)
                    update_bids(bids_update, bids)




                    # with placeholder10:
                # while True:
                    fix_df(bids, asks)
                    ordering_bids(bids, symbol,orders_to_place_a_side_bid, stink_save_bid_drawdown)



















        


            
asyncio.run(consumer())