import websockets
import asyncio
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
df = pd.DataFrame(columns = ['id', 'price', 'size', 'side', 'liquidation', 'time'])
placeholder1 = st.empty()
placeholder2 = st.empty()
placeholder3 = st.empty()

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

                    figz = make_subplots(specs=[[{"secondary_y": True}]])
                    figz.add_trace(go.Bar(x=asks['price_ask'], y=asks['size_ask'], name="asks"),secondary_y=True,)
                    figz.add_trace(go.Bar(x=bids['price_bid'], y=bids['size_bid'], name="bids"),secondary_y=True,)
                    figz.update_layout(title_text="perp")
                    st.plotly_chart(figz, use_container_width=True)

                            
                    now = datetime.datetime.now()
                    next_hour = now + timedelta(hours=1)
                    # st.write(now)
                    # st.write(next_hour)
                    date = datetime.datetime.strptime(str(next_hour), '%Y-%m-%d %H:%M:%S.%f')
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

                    fig = make_subplots(specs=[[{"secondary_y": True}]])
                    fig.add_trace(go.Bar(x=asks['price_ask'], y=asks['size_ask'], name="asks"),secondary_y=True,)
                    fig.add_trace(go.Bar(x=bids['price_bid'], y=bids['size_bid'], name="bids"),secondary_y=True,)
                    fig.update_layout(title_text="Dated")
                    st.plotly_chart(fig, use_container_width=True)
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
                    names_premeiums = 'BTC-0930'

                    expiry = names_premeiums.split('-')[1]
                    expiry = pd.to_datetime(expiry, format='%m%d')
                    # """ year is the same as this year"""
                    expiry = expiry.replace(year=datetime.datetime.now().year)
                    st.write("expiry date", expiry)

                    # expiry = datetime.datetime.strftime(expiry,'%m%d')
                    days_until_expiry = expiry - datetime.datetime.now()
                    # """between now and expiry"""

                    # st.write(int(datetime.now().('%m%d'strftime)))
                    # days_until_expiry = ((expiry).strftime('%m%d')) - (datetime.now().strftime('%m%d'))
                    # st.write("now",datetime.datetime.now())
                    st.write("days until expiry: ", days_until_expiry)
                    # st.write("add the amount of funding events until expiry ")


                    pct_expiry_dated = days_until_expiry.days / 365 * 100
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

                    fig = make_subplots(specs=[[{"secondary_y": True}]])
                    fig.add_trace(go.Bar(x=asks['price_ask'], y=asks['size_ask'], name="asks"),secondary_y=True,)
                    fig.add_trace(go.Bar(x=bids['price_bid'], y=bids['size_bid'], name="bids"),secondary_y=True,)
                    fig.update_layout(title_text="Spot")
                    st.plotly_chart(fig, use_container_width=True)
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

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)   
    coros = []
    coros.append(Perp())
    coros.append(Dated())
    coros.append(Spot())

    loop.run_until_complete(asyncio.gather(*coros))