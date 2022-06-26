import asyncio
import websockets
import json
import streamlit as st
import time
import plotly.express as px
import pandas as pd
from itertools import accumulate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
st.set_page_config(layout="wide")

# import plotly.express as px

# df = pd.DataFrame(columns = ['id', 'price', 'size', 'side', 'liquidation', 'time'])
# placeholder1 = st.empty()
# for seconds in range(200):
# while True: 
a = "Subscribed to orderbook"

b = "fat d8ta"
placeholder1 = st.empty()


async def consumer() -> None:
    async with websockets.connect("wss://ftx.com/ws/") as websocket:
        await websocket.send(
            json.dumps(
                {"op": "subscribe", "channel": "orderbook", "market": "ETH/USD"}
            )
        )
        async for message in websocket:
            global a
            global b

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
                    # st.write('2', bids, asks, action)

                    # return bids, asks, action, time, checksum
                if message["type"] == "update":
                    # global asks
                    # global bids
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
                        asks.loc[asks["price_ask"] == asks_update.loc[i]["price_ask"], "size_ask"] = asks_update.loc[i]["size_ask"]
                        asks.dropna(inplace=True)

                        asks = asks.append(asks_update, ignore_index=True)
                        asks = asks.drop_duplicates(subset=['price_ask'], keep='first')
                        asks.sort_values(by=['price_ask'], inplace=True)
                        asks.reset_index(drop = True, inplace=False)

                        asks.loc[asks["price_ask"] == asks_update.loc[i]["price_ask"], "size_ask"] = asks_update.loc[i]["size_ask"]
                    for i in range(len(bids_update)):
                        # global bids_update
                        # if bids_update['price_bid'][i] == asks_update['price_ask'][i]:
                            # global asks_update
                        # bids.reset_index(drop = True, inplace=True)

                        # bids.dropna(inplace=True)
                        bids.reset_index(drop=True)

                        # bids.append(bids_update.loc[i])
                        bids.loc[bids["price_bid"] == bids_update.loc[i]["price_bid"], "size_bid"] = bids_update.loc[i]["size_bid"]
                        bids.dropna(inplace=True)
                        bids = bids.append(bids_update, ignore_index=True)
                        bids = bids.drop_duplicates(subset=['price_bid'], keep='first')
                        bids.sort_values(by=['price_bid'], inplace=True, ascending=False)
                        bids.reset_index(drop=True, inplace=False)

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
   
                    st.write(asks,bids, use_container_width=True)
                    # st.write(asks_update,bids_update, use_container_width=True)
                    
                    fig = make_subplots(specs=[[{"secondary_y": True}]])
                    fig.add_trace(go.Scatter(x=asks['price_ask'], y=asks['accumulated'], name="asks"),secondary_y=True,)
                    fig.add_trace(go.Scatter(x=bids['price_bid'], y=bids['accumulated'], name="bids"),secondary_y=True,)
                    fig.update_layout(title_text="orderbook")
                    st.plotly_chart(fig, use_container_width=True)

                    fig = make_subplots(specs=[[{"secondary_y": True}]])
                    fig.add_trace(go.Bar(x=asks['price_ask'], y=asks['size_ask'], name="asks"),secondary_y=True,)
                    fig.add_trace(go.Bar(x=bids['price_bid'], y=bids['size_bid'], name="bids"),secondary_y=True,)
                    fig.update_layout(title_text="orderbook")
                    st.plotly_chart(fig, use_container_width=True)

                    fig = make_subplots(specs=[[{"secondary_y": True}]])
                    fig.add_trace(go.Scatter(x=asks['accumulated_avg_price'], y=asks['cash_equivelant'], name="asks"),secondary_y=True,)
                    fig.add_trace(go.Scatter(x=bids['accumulated_avg_price'], y=bids['cash_equivelant'], name="bids"),secondary_y=True,)
                    fig.update_layout(title_text="cash_equivelant")
                    st.plotly_chart(fig, use_container_width=True)
                    
asyncio.run(consumer())