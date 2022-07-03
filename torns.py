from hashlib import new
import websockets
import asyncio
import requests
import json
import time
import datetime
import pandas as pd
import streamlit as st
import plotly.express as px
from itertools import accumulate
from datetime import timedelta

import plotly.graph_objects as go
from plotly.subplots import make_subplots
st.set_page_config(layout="wide")
dict_dumps = {
  "op": "subscribe",
  "channel": "orderbook",
  "market": "BTC-PERP"
}


# perp = int(perp)
# df = pd.DataFrame(columns = ['id', 'price', 'size', 'side', 'liquidation', 'time'])
placeholder1 = st.empty()
placeholder2 = st.empty()
placeholder3 = st.empty()



now = datetime.datetime.now()
next_hour = now + timedelta(hours=1)
date = datetime.datetime.strptime(str(next_hour), '%Y-%m-%d %H:%M:%S.%f')
newdate = date.replace(minute=0,second=0)
time_till_expiry_perp = newdate - now
pct_expiry_perp = (time_till_expiry_perp.total_seconds() / 3600) / 24 / 365.24 * 100


max_value_perps = 1
min_value_perps = 1
spred_perps = 1
spred_bps_perps = 1

max_value_dated = 1
min_value_dated = 1
spred_dated = 1
spred_bps_dated = 1
pct_expiry_dated = 1

max_value_spot = 1
min_value_spot = 1
spred_spot = 1
spred_bps_spot = 1
















async def Perp():
   async with websockets.connect("wss://ftx.com/ws/", ping_interval=20, ping_timeout=2000) as websocket:
        await websocket.send(
            json.dumps(
                dict_dumps
            )
        )
        async for message in websocket:
            # global a
            # global b

            message = json.loads(message)
            global max_value_perps
            global min_value_perps
            global spred_bps_perps
            global spred_perps
            global newdate
            global next_hour
            global time_till_expiry_perp
            global pct_expiry_perp
            with placeholder1.container():

                if message["type"] == "subscribed":
                    st.write(message, use_container_width=True)

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
                    # st.write('2', bids, asks, action)

                    # return bids, asks, action, time, checksum
                if message["type"] == "update":
                    # global asks
                    # global bids
                    # st.write(message, use_container_width=True)
                    # st.write("orderbook incoming", use_container_width=True)
                    type_update = message["type"]
                    channel_update = message["channel"]
                    data_update = message["data"]
                    time_update  = data_update["time"]
                    # time_update = pd.to_datetime(time_update)
                    time_update = datetime.datetime.utcfromtimestamp(time_update)
                    # st.write(time_update)
                    checksum = data_update["checksum"]
                    bids_update = pd.DataFrame(data_update["bids"])
                    bids_update = bids_update.rename(columns={0: "price_bid", 1: "size_bid"})
                    asks_update = pd.DataFrame(data_update["asks"])
                    asks_update = asks_update.rename(columns={0: "price_ask", 1: "size_ask"})
  
                    action = data_update["action"]
                    # st.write(asks)
                    # asks_update['accumulated']  = (list(accumulate(asks_update['size_ask'])))
                    # asks_update['accumulated_price']  = (asks_update['price_ask']) * asks_update['size_ask']
                    # asks_update['accumulated_avg_price'] = (list(accumulate(asks_update['accumulated_price'])))  / asks_update['accumulated']
                    # asks_update['cash_equivelant'] = asks_update['accumulated'] * asks_update['accumulated_avg_price']

                    # bids_update['accumulated']  = (list(accumulate(bids_update['size_bid'])))
                    # bids_update['accumulated_price']  = (bids_update['price_bid']) *bids_update['size_bid']
                    # bids_update['accumulated_avg_price'] = (list(accumulate(bids_update['accumulated_price'])))  / bids_update['accumulated']
                    # bids_update['cash_equivelant'] = bids_update['accumulated'] * bids_update['accumulated_avg_price']


                    # asks.reset_index(drop = True, inplace=True)
                    # bids.reset_index(drop = True, inplace=True)


                    for i in range(len(asks_update)):
                        # global asks_update
                        # if asks_update['price_ask'][i] == bids_update['price_bid'][i]:
                            # global bids_update
                        # asks.append(asks_update.loc[i])

                        # asks.reset_index(drop = True, inplace=True)
                        # asks.dropna(inplace=True)
                        asks['time'] = time_update
                        asks.loc[asks["price_ask"] == asks_update.loc[i]["price_ask"], "size_ask"] = asks_update.loc[i]["size_ask"]
                        asks.dropna(inplace=True)

                        asks = pd.concat([asks, pd.DataFrame.from_records(asks_update)])

                        asks = asks.drop_duplicates(subset=['price_ask'], keep='first')
                        asks.sort_values(by=['price_ask'], inplace=True)
                        asks.reset_index(drop = True, inplace=False)

                        asks.loc[asks["price_ask"] == asks_update.loc[i]["price_ask"], "size_ask"] = asks_update.loc[i]["size_ask"]
                    for i in range(len(bids_update)):
                        bids['time'] = time_update
                        # global bids_update
                        # if bids_update['price_bid'][i] == asks_update['price_ask'][i]:
                            # global asks_update
                        # bids.reset_index(drop = True, inplace=True)

                        # bids.dropna(inplace=True)
                        bids.reset_index(drop=True)

                        # bids.append(bids_update.loc[i])
                        bids.loc[bids["price_bid"] == bids_update.loc[i]["price_bid"], "size_bid"] = bids_update.loc[i]["size_bid"]
                        bids.dropna(inplace=True)
                        bids = pd.concat([bids, pd.DataFrame.from_records(bids_update)])

                        bids = bids.drop_duplicates(subset=['price_bid'], keep='first')
                        bids.sort_values(by=['price_bid'], inplace=True, ascending=False)
                        bids.reset_index(drop=True, inplace=False)
                        bids.loc[bids["price_bid"] == bids_update.loc[i]["price_bid"], "size_bid"] = bids_update.loc[i]["size_bid"]

                    asks = pd.DataFrame(asks)
                    bids = pd.DataFrame(bids)
                    # st.write(asks_update)
                    # st.write(bids_update)
                    asks['accumulated']  = (list(accumulate(asks['size_ask'])))
                    asks['accumulated_price']  = (asks['price_ask']) * asks['size_ask']
                    asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
                    asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']

                    bids['accumulated']  = (list(accumulate(bids['size_bid'])))
                    bids['accumulated_price']  = (bids['price_bid']) * bids['size_bid']
                    bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
                    bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']                
                    # for i in range(1, 2):
                    #     cols = st.columns(2)
                    #     cols[0].subheader("bids")

                    #     cols[0].write(bids)
                    #     cols[1].subheader("asks")


                    #     cols[1].write(asks)
                    # # st.write(asks,bids, use_container_width=True)
                    # st.write(asks_update,bids_update, use_container_width=True)
                    
                    # fig = make_subplots(specs=[[{"secondary_y": True}]])
                    # fig.add_trace(go.Scatter(x=asks['price_ask'], y=asks['accumulated'], name="asks"),secondary_y=True,)
                    # fig.add_trace(go.Scatter(x=bids['price_bid'], y=bids['accumulated'], name="bids"),secondary_y=True,)
                    # fig.update_layout(title_text="orderbook")
                    # st.plotly_chart(fig, use_container_width=True)

                    # figz = make_subplots(specs=[[{"secondary_y": True}]])
                    # figz.add_trace(go.Bar(x=asks['price_ask'], y=asks['size_ask'], name="asks"),secondary_y=True,)
                    # figz.add_trace(go.Bar(x=bids['price_bid'], y=bids['size_bid'], name="bids"),secondary_y=True,)
                    # figz.update_layout(title_text="perp")
                    # st.plotly_chart(figz, use_container_width=True)

                            
                    now = datetime.datetime.now()
                    next_hour = now + timedelta(hours=1)
                    st.write("now", now)
                    # st.write("next_hour", next_hour)
                    date = datetime.datetime.strptime(str(next_hour), '%Y-%m-%d %H:%M:%S.%f')
                    newdate = date.replace(minute=0,second=0)
                    st.write("end", newdate)
        # newdate = date.replace(second=0)

        # st.write(date)
        # st.write(newdate)
                    time_till_expiry_perp = newdate - now
                    st.write("time till expiry", time_till_expiry_perp)

                    pct_expiry_perp = (time_till_expiry_perp.total_seconds() / 3600) / 24 / 365.24 * 100
                    st.write("percentage till expiry", pct_expiry_perp, "%")


                    # st.write(hour)
                    # expiry = pd.to_datetime(hour, format='%m%d')
                    # st.write(expiry)
                    column = bids["price_bid"]
                    max_value_perps = column.max()
                    st.write("best bid perps", max_value_perps)


                    column = asks["price_ask"]
                    min_value_perps = column.min()
                    st.write("best bid asks", min_value_perps)

                    spred_perps = min_value_perps - max_value_perps
                    st.write("perp spread",spred_perps)

                    spred_bps_perps = spred_perps/min_value_perps*1000
                    st.write("perp spread", spred_bps_perps , "bps")


                    # column = bids["price_bid"]
                    # max_value_perp = column.max()
                    # st.write("now",datetime.datetime.now())
                    # st.write("best bid", max_value_perp)

                    # column = asks["price_ask"]
                    # min_value_perp = column.min()
                    # st.write("best ask", min_value_perp)

                    # spred_perp = min_value_perp - max_value_perp
                    # st.write("spot spread", spred_perp)

                    # spred_bps_perp = spred_perp/min_value_perp*1000
                    # st.write("spred_bps", spred_bps_perp , "bps")
                    # st.write(time)
                    # st.write(time_update)
                    # fig = make_subplots(specs=[[{"secondary_y": True}]])
                    # fig.add_trace(go.Scatter(x=asks['time'], y=asks['price_ask'], line=asks['size_ask'], name="asks"),secondary_y=True,)
                    # fig.add_trace(go.Scatter(x=bids['time'], y=bids['price_bid'], line=bids['size_bid'] , name="bids"),secondary_y=True,)
                    # fig.update_layout(title_text="orderbook")
                    # st.plotly_chart(fig, use_container_width=True)
                    # fig = make_subplots(specs=[[{"secondary_y": True}]])
                    # fig.add_trace(go.Scatter(x=asks['accumulated_avg_price'], y=asks['cash_equivelant'], name="asks"),secondary_y=True,)
                    # fig.add_trace(go.Scatter(x=bids['accumulated_avg_price'], y=bids['cash_equivelant'], name="bids"),secondary_y=True,)
                    # fig.update_layout(title_text="cash_equivelant")
                    # st.plotly_chart(fig, use_container_width=True)
async def Dated():
 async with websockets.connect("wss://ftx.com/ws/", ping_interval=20, ping_timeout=2000) as websocket:
        await websocket.send(
            json.dumps(
                {
                    "op": "subscribe",
                    "channel": "orderbook",
                    "market": "BTC-0930"
                    }
            )
        )
        async for message in websocket:
            # global a
            # global b

            message = json.loads(message)
            
            global max_value_dated
            global min_value_dated
            global spred_dated
            global spred_bps_dated
            global pct_expiry_dated
            with placeholder2.container():

                if message["type"] == "subscribed":
                    st.write(message, use_container_width=True)

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
                    # st.write('2', bids, asks, action)

                    # return bids, asks, action, time, checksum
                if message["type"] == "update":
                    # global asks
                    # global bids
                    # st.write(message, use_container_width=True)
                    # st.write("orderbook incoming", use_container_width=True)
                    type_update = message["type"]
                    channel_update = message["channel"]
                    data_update = message["data"]
                    time_update  = data_update["time"]
                    # time_update = pd.to_datetime(time_update)
                    time_update = datetime.datetime.utcfromtimestamp(time_update)
                    # st.write(time_update)
                    checksum = data_update["checksum"]
                    bids_update = pd.DataFrame(data_update["bids"])
                    bids_update = bids_update.rename(columns={0: "price_bid", 1: "size_bid"})
                    asks_update = pd.DataFrame(data_update["asks"])
                    asks_update = asks_update.rename(columns={0: "price_ask", 1: "size_ask"})
  
                    action = data_update["action"]
                    # st.write(asks)
                    # asks_update['accumulated']  = (list(accumulate(asks_update['size_ask'])))
                    # asks_update['accumulated_price']  = (asks_update['price_ask']) * asks_update['size_ask']
                    # asks_update['accumulated_avg_price'] = (list(accumulate(asks_update['accumulated_price'])))  / asks_update['accumulated']
                    # asks_update['cash_equivelant'] = asks_update['accumulated'] * asks_update['accumulated_avg_price']

                    # bids_update['accumulated']  = (list(accumulate(bids_update['size_bid'])))
                    # bids_update['accumulated_price']  = (bids_update['price_bid']) *bids_update['size_bid']
                    # bids_update['accumulated_avg_price'] = (list(accumulate(bids_update['accumulated_price'])))  / bids_update['accumulated']
                    # bids_update['cash_equivelant'] = bids_update['accumulated'] * bids_update['accumulated_avg_price']


                    # asks.reset_index(drop = True, inplace=True)
                    # bids.reset_index(drop = True, inplace=True)


                    for i in range(len(asks_update)):
                        # global asks_update
                        # if asks_update['price_ask'][i] == bids_update['price_bid'][i]:
                            # global bids_update
                        # asks.append(asks_update.loc[i])

                        # asks.reset_index(drop = True, inplace=True)
                        # asks.dropna(inplace=True)
                        asks['time'] = time_update
                        asks.loc[asks["price_ask"] == asks_update.loc[i]["price_ask"], "size_ask"] = asks_update.loc[i]["size_ask"]
                        asks.dropna(inplace=True)

                        asks = pd.concat([asks, pd.DataFrame.from_records(asks_update)])

                        asks = asks.drop_duplicates(subset=['price_ask'], keep='first')
                        asks.sort_values(by=['price_ask'], inplace=True)
                        asks.reset_index(drop = True, inplace=False)

                        asks.loc[asks["price_ask"] == asks_update.loc[i]["price_ask"], "size_ask"] = asks_update.loc[i]["size_ask"]
                    for i in range(len(bids_update)):
                        bids['time'] = time_update
                        # global bids_update
                        # if bids_update['price_bid'][i] == asks_update['price_ask'][i]:
                            # global asks_update
                        # bids.reset_index(drop = True, inplace=True)

                        # bids.dropna(inplace=True)
                        bids.reset_index(drop=True)

                        # bids.append(bids_update.loc[i])
                        bids.loc[bids["price_bid"] == bids_update.loc[i]["price_bid"], "size_bid"] = bids_update.loc[i]["size_bid"]
                        bids.dropna(inplace=True)
                        bids = pd.concat([bids, pd.DataFrame.from_records(bids_update)])

                        bids = bids.drop_duplicates(subset=['price_bid'], keep='first')
                        bids.sort_values(by=['price_bid'], inplace=True, ascending=False)
                        bids.reset_index(drop=True, inplace=False)
                        bids.loc[bids["price_bid"] == bids_update.loc[i]["price_bid"], "size_bid"] = bids_update.loc[i]["size_bid"]

                    asks = pd.DataFrame(asks)
                    bids = pd.DataFrame(bids)
                    # st.write(asks_update)
                    # st.write(bids_update)
                    asks['accumulated']  = (list(accumulate(asks['size_ask'])))
                    asks['accumulated_price']  = (asks['price_ask']) * asks['size_ask']
                    asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
                    asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']

                    bids['accumulated']  = (list(accumulate(bids['size_bid'])))
                    bids['accumulated_price']  = (bids['price_bid']) * bids['size_bid']
                    bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
                    bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']                
                    # for i in range(1, 2):
                    #     cols = st.columns(2)
                    #     cols[0].subheader("bids")

                    #     cols[0].write(bids)
                    #     cols[1].subheader("asks")


                    #     cols[1].write(asks)
                    # # st.write(asks,bids, use_container_width=True)
                    # st.write(asks_update,bids_update, use_container_width=True)
                    
                    # fig = make_subplots(specs=[[{"secondary_y": True}]])
                    # fig.add_trace(go.Scatter(x=asks['price_ask'], y=asks['accumulated'], name="asks"),secondary_y=True,)
                    # fig.add_trace(go.Scatter(x=bids['price_bid'], y=bids['accumulated'], name="bids"),secondary_y=True,)
                    # fig.update_layout(title_text="orderbook")
                    # st.plotly_chart(fig, use_container_width=True)

                    # fig = make_subplots(specs=[[{"secondary_y": True}]])
                    # fig.add_trace(go.Bar(x=asks['price_ask'], y=asks['size_ask'], name="asks"),secondary_y=True,)
                    # fig.add_trace(go.Bar(x=bids['price_bid'], y=bids['size_bid'], name="bids"),secondary_y=True,)
                    # fig.update_layout(title_text="Dated")
                    # st.plotly_chart(fig, use_container_width=True)
                    column = bids["price_bid"]
                    max_value_dated = column.max()
                    st.write("now",datetime.datetime.now())
                    st.write("best bid", max_value_dated)

                    column = asks["price_ask"]
                    min_value_dated = column.min()
                    st.write("best ask", min_value_dated)

                    spred_dated = min_value_dated - max_value_dated
                    st.write("spred_dated ", spred_dated)

                    spred_bps_dated = spred_dated/min_value_dated*1000
                    st.write("spred_bps", spred_bps_dated , "bps")
                    names_premeiums = 'BTC-0930'

                    expiry = names_premeiums.split('-')[1]
                    expiry = pd.to_datetime(expiry, format='%m%d')
                    # """ year is the same as this year"""
                    expiry = expiry.replace(year=datetime.datetime.now().year)
                    st.write("expiry date", expiry)

                    # expiry = datetime.datetime.strftime(expiry,'%m%d')
                    days_until_expiry_dated = expiry - datetime.datetime.now()
                    # """between now and expiry"""

                    # st.write(int(datetime.now().('%m%d'strftime)))
                    # days_until_expiry = ((expiry).strftime('%m%d')) - (datetime.now().strftime('%m%d'))
                    # st.write("now",datetime.datetime.now())
                    st.write("days until expiry: ", days_until_expiry_dated)
                    # st.write("add the amount of funding events until expiry ")


                    pct_expiry_dated = days_until_expiry_dated.days / 365 * 100
                    st.write("expiry time - pct of a year: ", pct_expiry_dated, "%")                    # st.write(time)
                    # st.write(time_update)
                    # fig = make_subplots(specs=[[{"secondary_y": True}]])
                    # fig.add_trace(go.Scatter(x=asks['time'], y=asks['price_ask'], line=asks['size_ask'], name="asks"),secondary_y=True,)
                    # fig.add_trace(go.Scatter(x=bids['time'], y=bids['price_bid'], line=bids['size_bid'] , name="bids"),secondary_y=True,)
                    # fig.update_layout(title_text="orderbook")
                    # st.plotly_chart(fig, use_container_width=True)
                    # fig = make_subplots(specs=[[{"secondary_y": True}]])
                    # fig.add_trace(go.Scatter(x=asks['accumulated_avg_price'], y=asks['cash_equivelant'], name="asks"),secondary_y=True,)
                    # fig.add_trace(go.Scatter(x=bids['accumulated_avg_price'], y=bids['cash_equivelant'], name="bids"),secondary_y=True,)
                    # fig.update_layout(title_text="cash_equivelant")
                    # st.plotly_chart(fig, use_container_width=True)
async def Spot():
 async with websockets.connect("wss://ftx.com/ws/", ping_interval=20, ping_timeout=2000) as websocket:
        await websocket.send(
            json.dumps(
                {
                    "op": "subscribe",
                    "channel": "orderbook",
                    "market": "BTC/USD"
                    }
            )
        )
        async for message in websocket:
            # global a
            # global b
            global max_value_spot
            global min_value_spot
            global spred_spot
            global spred_bps_spot
            message = json.loads(message)
            with placeholder3.container():

                if message["type"] == "subscribed":
                    st.write(message, use_container_width=True)

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
                    # st.write('2', bids, asks, action)

                    # return bids, asks, action, time, checksum
                if message["type"] == "update":
                    # global asks
                    # global bids
                    # st.write(message, use_container_width=True)
                    # st.write("orderbook incoming", use_container_width=True)
                    type_update = message["type"]
                    channel_update = message["channel"]
                    data_update = message["data"]
                    time_update  = data_update["time"]
                    # time_update = pd.to_datetime(time_update)
                    # time_update = datetime.datetime.utcfromtimestamp(time_update)
                    # st.write(time_update)
                    checksum = data_update["checksum"]
                    bids_update = pd.DataFrame(data_update["bids"])
                    bids_update = bids_update.rename(columns={0: "price_bid", 1: "size_bid"})
                    asks_update = pd.DataFrame(data_update["asks"])
                    asks_update = asks_update.rename(columns={0: "price_ask", 1: "size_ask"})
  
                    action = data_update["action"]
                    # st.write(asks)
                    # asks_update['accumulated']  = (list(accumulate(asks_update['size_ask'])))
                    # asks_update['accumulated_price']  = (asks_update['price_ask']) * asks_update['size_ask']
                    # asks_update['accumulated_avg_price'] = (list(accumulate(asks_update['accumulated_price'])))  / asks_update['accumulated']
                    # asks_update['cash_equivelant'] = asks_update['accumulated'] * asks_update['accumulated_avg_price']

                    # bids_update['accumulated']  = (list(accumulate(bids_update['size_bid'])))
                    # bids_update['accumulated_price']  = (bids_update['price_bid']) *bids_update['size_bid']
                    # bids_update['accumulated_avg_price'] = (list(accumulate(bids_update['accumulated_price'])))  / bids_update['accumulated']
                    # bids_update['cash_equivelant'] = bids_update['accumulated'] * bids_update['accumulated_avg_price']


                    # asks.reset_index(drop = True, inplace=True)
                    # bids.reset_index(drop = True, inplace=True)


                    for i in range(len(asks_update)):
                        # global asks_update
                        # if asks_update['price_ask'][i] == bids_update['price_bid'][i]:
                            # global bids_update
                        # asks.append(asks_update.loc[i])

                        # asks.reset_index(drop = True, inplace=True)
                        # asks.dropna(inplace=True)
                        asks['time'] = time_update
                        asks.loc[asks["price_ask"] == asks_update.loc[i]["price_ask"], "size_ask"] = asks_update.loc[i]["size_ask"]
                        asks.dropna(inplace=True)

                        asks = pd.concat([asks, pd.DataFrame.from_records(asks_update)])

                        asks = asks.drop_duplicates(subset=['price_ask'], keep='first')
                        asks.sort_values(by=['price_ask'], inplace=True)
                        asks.reset_index(drop = True, inplace=False)

                        asks.loc[asks["price_ask"] == asks_update.loc[i]["price_ask"], "size_ask"] = asks_update.loc[i]["size_ask"]
                    for i in range(len(bids_update)):
                        bids['time'] = time_update
                        # global bids_update
                        # if bids_update['price_bid'][i] == asks_update['price_ask'][i]:
                            # global asks_update
                        # bids.reset_index(drop = True, inplace=True)

                        # bids.dropna(inplace=True)
                        bids.reset_index(drop=True)

                        # bids.append(bids_update.loc[i])
                        bids.loc[bids["price_bid"] == bids_update.loc[i]["price_bid"], "size_bid"] = bids_update.loc[i]["size_bid"]
                        bids.dropna(inplace=True)
                        bids = pd.concat([bids, pd.DataFrame.from_records(bids_update)])

                        bids = bids.drop_duplicates(subset=['price_bid'], keep='first')
                        bids.sort_values(by=['price_bid'], inplace=True, ascending=False)
                        bids.reset_index(drop=True, inplace=False)
                        bids.loc[bids["price_bid"] == bids_update.loc[i]["price_bid"], "size_bid"] = bids_update.loc[i]["size_bid"]

                    asks = pd.DataFrame(asks)
                    bids = pd.DataFrame(bids)
                    # st.write(asks_update)
                    # st.write(bids_update)
                    asks['accumulated']  = (list(accumulate(asks['size_ask'])))
                    asks['accumulated_price']  = (asks['price_ask']) * asks['size_ask']
                    asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
                    asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']

                    bids['accumulated']  = (list(accumulate(bids['size_bid'])))
                    bids['accumulated_price']  = (bids['price_bid']) * bids['size_bid']
                    bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
                    bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']                
                    # for i in range(1, 2):
                    #     cols = st.columns(2)
                    #     cols[0].subheader("bids")

                    #     cols[0].write(bids)
                    #     cols[1].subheader("asks")


                    #     cols[1].write(asks)
                    # # st.write(asks,bids, use_container_width=True)
                    # st.write(asks_update,bids_update, use_container_width=True)
                    
                    # fig = make_subplots(specs=[[{"secondary_y": True}]])
                    # fig.add_trace(go.Scatter(x=asks['price_ask'], y=asks['accumulated'], name="asks"),secondary_y=True,)
                    # fig.add_trace(go.Scatter(x=bids['price_bid'], y=bids['accumulated'], name="bids"),secondary_y=True,)
                    # fig.update_layout(title_text="orderbook")
                    # st.plotly_chart(fig, use_container_width=True)

                    # fig = make_subplots(specs=[[{"secondary_y": True}]])
                    # fig.add_trace(go.Bar(x=asks['price_ask'], y=asks['size_ask'], name="asks"),secondary_y=True,)
                    # fig.add_trace(go.Bar(x=bids['price_bid'], y=bids['size_bid'], name="bids"),secondary_y=True,)
                    # fig.update_layout(title_text="Spot")
                    # st.plotly_chart(fig, use_container_width=True)
                    column = bids["price_bid"]
                    max_value_spot = column.max()
                    st.write("now",datetime.datetime.now())
                    st.write("best bid", max_value_spot)

                    column = asks["price_ask"]
                    min_value_spot = column.min()
                    st.write("best ask", min_value_spot)

                    spred_spot = min_value_spot - max_value_spot
                    st.write("spot spread", spred_spot)

                    spred_bps_spot = spred_spot/min_value_spot*1000
                    st.write("spred_bps", spred_bps_spot , "bps")
                    # return *
                    # st.write(time)
                    # st.write(time_update)
                    # fig = make_subplots(specs=[[{"secondary_y": True}]])
                    # fig.add_trace(go.Scatter(x=asks['time'], y=asks['price_ask'], line=asks['size_ask'], name="asks"),secondary_y=True,)
                    # fig.add_trace(go.Scatter(x=bids['time'], y=bids['price_bid'], line=bids['size_bid'] , name="bids"),secondary_y=True,)
                    # fig.update_layout(title_text="orderbook")
                    # st.plotly_chart(fig, use_container_width=True)
                    # fig = make_subplots(specs=[[{"secondary_y": True}]])
                    # fig.add_trace(go.Scatter(x=asks['accumulated_avg_price'], y=asks['cash_equivelant'], name="asks"),secondary_y=True,)
                    # fig.add_trace(go.Scatter(x=bids['accumulated_avg_price'], y=bids['cash_equivelant'], name="bids"),secondary_y=True,)
                    # fig.update_layout(title_text="cash_equivelant")
                    # st.plotly_chart(fig, use_container_width=True)
 
# async def info():
#     global max_value_spot
#     global min_value_spot
#     global spred_spot
#     global spred_bps_spot# def info():
#     global max_value_dated
#     global min_value_dated
#     global spred_dated
#     global spred_bps_dated
#     global pct_expiry_dated
#     global max_value_perps
#     global min_value_perps
#     global spred_bps_perps
#     global spred_perps
#     global newdate
#     global next_hour
#     global time_till_expiry_perp
#     global pct_expiry_perp
                    name_perp = "BTC-PERP"
                    custom = requests.get(f"https://ftxpremiums.com/assets/data/funding_data/{name_perp}.json").json()
                    custom = pd.DataFrame(custom)
                    custom['rate'] = custom['rate'].astype(float)
                    custom['time'] =  pd.to_datetime(custom['time'], unit='s')
                    custom = custom.sort_values(by="time")

                    custom['rate'] = custom['rate'] * 1000
                    custom['rate_APY'] = custom['rate'] / 10 * 24 * 365.24

                    custom['accumulated']  = (list(accumulate(custom['rate'])))
                    #
                    names_lending = "BTC"
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

                    # window = st.sidebar.slider('window size (periods for rolling average)', 1, 250, 20)
                    # no_of_std = st.sidebar.slider('number of standard deviations', 1, 5, 2)

                    latest_rateAPY = custom['rate_APY'].iloc[-1]
                    st.write("Latest Funding rate APY", latest_rateAPY)
                    st.subheader("""first we look at spot vs dated """)
                    latest_rateAPY_spot = custom_lending['rateAPY'].iloc[-1]

                    long_spot_position_to_expiry = (min_value_spot * (1 - ((latest_rateAPY_spot/1000)*(pct_expiry_dated/100))))
                    short_spot_position_to_expiry = (max_value_spot * (1 - ((latest_rateAPY_spot/1000)*(pct_expiry_dated/100))))

                    PREMIUM_LONG_SPOT_SHORT_DATED_FUTURE = (max_value_dated - long_spot_position_to_expiry) 
                    PREMIUM_SHORT_SPOT_LONG_DATED_FUTURE = (short_spot_position_to_expiry - min_value_dated) 

                    PREMIUM_LONG_SPOT_SHORT_DATED_FUTURE_APY = PREMIUM_LONG_SPOT_SHORT_DATED_FUTURE / (min_value_spot * (pct_expiry_dated/100)) * 100
                    PREMIUM_SHORT_SPOT_LONG_DATED_FUTURE_APY = PREMIUM_SHORT_SPOT_LONG_DATED_FUTURE / (max_value_spot * (pct_expiry_dated/100)) * 100

                    st.write("buy", min_value_spot, "spot", "sell", max_value_dated, "dated_future")
                    st.write("long_spot_position_to_expiry",long_spot_position_to_expiry)
                    st.write("PREMIUM_LONG_SPOT_SHORT_DATED_FUTURE",PREMIUM_LONG_SPOT_SHORT_DATED_FUTURE)
                    st.write(PREMIUM_LONG_SPOT_SHORT_DATED_FUTURE_APY, "% APY")





                    st.write("sell", max_value_spot, "spot", "buy", min_value_dated, "dated_future")
                    st.write("short_spot_position_to_expiry",short_spot_position_to_expiry)
                    st.write("PREMIUM_SHORT_SPOT_LONG_DATED_FUTURE",PREMIUM_SHORT_SPOT_LONG_DATED_FUTURE)
                    st.write(PREMIUM_SHORT_SPOT_LONG_DATED_FUTURE_APY, "% APY")


                    st.subheader("""next we look at spot vs perp""")


                    spot_long_spot_position_to_expiry_perp = (min_value_spot * (1 - ((latest_rateAPY_spot/1000)*(pct_expiry_perp/100))))
                    spot_short_spot_position_to_expiry_perp = (max_value_spot * (1 - ((latest_rateAPY_spot/1000)*(pct_expiry_perp/100))))

                    perp_long_spot_position_to_expiry_perp = (max_value_perps * (1 + ((latest_rateAPY/1000)*(pct_expiry_perp/100))))
                    perp_short_spot_position_to_expiry_perp = (min_value_perps * (1 + ((latest_rateAPY/1000)*(pct_expiry_perp/100))))

                    PREMIUM_LONG_SPOT_SHORT_PERP = (perp_long_spot_position_to_expiry_perp - spot_long_spot_position_to_expiry_perp) 
                    PREMIUM_SHORT_SPOT_LONG_PERP = (spot_short_spot_position_to_expiry_perp - perp_short_spot_position_to_expiry_perp)


                    PREMIUM_LONG_SPOT_SHORT_PERP_APY = PREMIUM_LONG_SPOT_SHORT_PERP / (min_value_spot * (pct_expiry_perp/100)) * 100
                    PREMIUM_SHORT_SPOT_LONG_PERP_APY = PREMIUM_SHORT_SPOT_LONG_PERP / (max_value_spot * (pct_expiry_perp/100)) * 100



                    st.write("sell PERP @ ", max_value_perps, "buy spot @ ", min_value_spot)
                    st.write("long_spot_position_to_expiry",spot_long_spot_position_to_expiry_perp)
                    st.write("perp_long_spot_position_to_expiry_perp",perp_long_spot_position_to_expiry_perp)
                    st.write("PREMIUM_LONG_SPOT_SHORT_PERP",PREMIUM_LONG_SPOT_SHORT_PERP)
                    st.write(PREMIUM_LONG_SPOT_SHORT_PERP_APY, "% APY")

                    st.write("sell spot @ ", max_value_spot, "buy perp @ ", min_value_perps)
                    st.write("short_spot_position_to_expiry",spot_short_spot_position_to_expiry_perp)
                    st.write("perp_short_spot_position_to_expiry_perp",perp_short_spot_position_to_expiry_perp)
                    st.write("PREMIUM_SHORT_SPOT_LONG_PERP",PREMIUM_SHORT_SPOT_LONG_PERP)
                    st.write(PREMIUM_SHORT_SPOT_LONG_PERP_APY, "% APY")

                    st.subheader("now dated_futures vs perps")


                    long_perp_position_to_expiry = (min_value_perps * (1 + ((latest_rateAPY/1000)*(pct_expiry_dated/100))))
                    short_perp_position_to_expiry = (max_value_perps * (1 + ((latest_rateAPY/1000)*(pct_expiry_dated/100))))

                    PREMIUM_LONG_PERP_SHORT_DATED_FUTURE = (max_value_dated - long_perp_position_to_expiry) 
                    PREMIUM_SHORT_PERP_LONG_DATED_FUTURE = (short_perp_position_to_expiry - min_value_dated) 

                    PREMIUM_LONG_PERP_SHORT_DATED_FUTURE_APY = PREMIUM_LONG_PERP_SHORT_DATED_FUTURE / (min_value_perps * (pct_expiry_dated/100)) * 100
                    PREMIUM_SHORT_PERP_LONG_DATED_FUTURE_APY = PREMIUM_SHORT_PERP_LONG_DATED_FUTURE / (max_value_perps * (pct_expiry_dated/100)) * 100




                    st.write("buy", min_value_perps, "perp", "sell", max_value_dated, "dated_future")
                    st.write("long_perp_position_to_expiry",long_perp_position_to_expiry)
                    st.write("PREMIUM_LONG_PERP_SHORT_DATED_FUTURE",PREMIUM_LONG_PERP_SHORT_DATED_FUTURE)
                    st.write(PREMIUM_LONG_PERP_SHORT_DATED_FUTURE_APY, "% APY")





                    st.write("sell", max_value_perps, "perp", "buy", min_value_dated, "dated_future")
                    st.write("short_perp_position_to_expiry",short_perp_position_to_expiry)
                    st.write("PREMIUM_SHORT_PERP_LONG_DATED_FUTURE",PREMIUM_SHORT_PERP_LONG_DATED_FUTURE)
                    st.write(PREMIUM_SHORT_PERP_LONG_DATED_FUTURE_APY, "% APY")
                                    
                                    # st.subheader("dated futures")
                                    # st.write("best bid dated futures", max_value_dated)
                                    # st.write("best ask dated futures", min_value_dated)
                                    # st.write("spread dated futures", spred_dated)
                                    # st.write("spread dated futures", spred_dated_BPS, "bps")
                                    # st.write("expiry date", expiry)
                                    # st.write("now",datetime.datetime.now())
                                    # st.write("days until expiry: ", days_until_expiry)
                                    # st.write("expiry time - pct of a year: ", pct_expiry_dated, "%")


                                    # st.subheader("lending/spot")
                                    # st.write("latest rate APY", latest_rateAPY_spot)
                                    # latest_rate_bps_hr = custom_lending['rate_bps_hr'].iloc[-1]
                                    # st.write("rate_bps_hr", latest_rate_bps_hr)
                                    # st.write("now",datetime.now())
                                    # st.write("best bid", max_value_spot)
                                    # st.write("best ask", min_value_spot)
                                    # st.write("spot spread", spred_spot)
                                    # st.write("spred_bps", spred_bps_spot , "bps")




                    # st.subheader("funding/perpetual")
                    # latest_rateAPY = custom['rate_APY'].iloc[-1]
                    # st.write("Latest Funding rate APY", latest_rateAPY)
                    # latest_rate_bps_hr = custom['rate'].iloc[-1]
                    # st.write("funding_rate_bps_hr", latest_rate_bps_hr)
                # rolling_mean_funding = custom['rolling_mean_rate_APY'].iloc[-1]
                # st.write("rolling_mean_funding", rolling_mean_funding)
                # st.write("time till expiry", time_till_expiry)
                # st.write("percentage till expiry", pct_expiry, "%")
                # st.write("best bid perps", max_value_perps)
                # st.write("best bid asks", min_value_perps)`````
# st.write("perp spread",spred_perps)
# st.write("perp spread", spred_bps_perps , "bps")

# info()
# self._drain_lock = asyncio.Lock(
#     **({"loop": loop} if sys.version_info[:2] < (3, 8) else {})
# )

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)   
    coros = []
    coros.append(Perp())
    coros.append(Dated())
    coros.append(Spot())
    # coros.append(info())

    loop.run_until_complete(asyncio.gather(*coros))
