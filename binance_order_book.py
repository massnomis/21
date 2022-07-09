import websocket
import datetime
import streamlit as st
import time
import json
import plotly.express as px
import pandas as pd
from itertools import accumulate
import plotly.graph_objects as go
from plotly.subplots import make_subplots



st.set_page_config(layout="wide")
placeholder1 = st.empty()

# import websocket-client
def on_message(ws, message):
    # print()
    # print(str(datetime.datetime.now()) + ": ")
    message = json.loads(message)

    with placeholder1.container():
        # message = message.json()
        # st.json(message)
        # message = pd.DataFrame(message)
        # st.write(message)
        bids = message["bids"]
        bids = pd.DataFrame(bids)
        bids = bids.rename(columns={0: "price_bid", 1: "size_bid"})
        asks = message["asks"]
        asks = pd.DataFrame(asks)
  

        asks = asks.rename(columns={0: "price_ask", 1: "size_ask"})

        # st.write(bids, asks)



        # for i in range(len(asks)):

        #     asks.loc[asks["price_ask"] == asks.loc[i]["price_ask"], "size_ask"] = asks.loc[i]["size_ask"]
        #     asks.dropna(inplace=True)

        #     asks = asks.append(asks, ignore_index=True)
        #     asks = asks.drop_duplicates(subset=['price_ask'], keep='first')
        #     asks.sort_values(by=['price_ask'], inplace=True)
        #     asks.reset_index(drop = True, inplace=False)

        #     asks.loc[asks["price_ask"] == asks.loc[i]["price_ask"], "size_ask"] = asks.loc[i]["size_ask"]
        # for i in range(len(bids)):

        # bids.reset_index(drop=True)

        # bids.loc[bids["price_bid"] == bids.loc[i]["price_bid"], "size_bid"] = bids.loc[i]["size_bid"]
        # bids.dropna(inplace=True)
        # bids = bids.append(bids, ignore_index=True)
        # bids = bids.drop_duplicates(subset=['price_bid'], keep='first')
        # bids.sort_values(by=['price_bid'], inplace=True, ascending=False)
        # bids.reset_index(drop=True, inplace=False)
        # bids.loc[bids["price_bid"] == bids.loc[i]["price_bid"], "size_bid"] = bids.loc[i]["size_bid"]

        # asks = pd.DataFrame(asks)
        # bids = pd.DataFrame(bids)
        bids["price_bid"] = bids["price_bid"].astype(float)
        bids["size_bid"] = bids["size_bid"].astype(float)
        asks["price_ask"] = asks["price_ask"].astype(float)
        asks["size_ask"] = asks["size_ask"].astype(float)
        asks['accumulated']  = (list(accumulate(asks['size_ask'])))
        asks['accumulated_price']  = (asks['price_ask']) * asks['size_ask']
        asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
        asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']

        bids['accumulated']  = (list(accumulate(bids['size_bid'])))
        bids['accumulated_price']  = (bids['price_bid']) * bids['size_bid']
        bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
        bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']  

        for i in range(1, 2):
            cols = st.columns(2)
            cols[0].subheader("bids")

            cols[0].write(bids)
            # cols[0].plotly(px.bar(bids, x="price_bid", y="size_bid", title="bids"), use_container_width=True)

            cols[1].subheader("asks")

            cols[1].write(asks)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=asks['price_ask'], y=asks['accumulated'], name="asks"),secondary_y=True,)
        fig.add_trace(go.Scatter(x=bids['price_bid'], y=bids['accumulated'], name="bids"),secondary_y=True,)
        fig.update_layout(title_text="orderbook")
        st.plotly_chart(fig, use_container_width=True)
        st.plotly_chart(px.bar(bids, x="price_bid", y="size_bid", title="bids"), use_container_width=True)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=bids['price_bid'], y=bids['size_bid'], name="bids"),secondary_y=True,)
        fig.add_trace(go.Bar(x=asks['price_ask'], y=asks['size_ask'], name="asks"),secondary_y=True,)
        fig.update_layout(title_text="orderbook")
        st.plotly_chart(fig, use_container_width=True)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=asks['accumulated_avg_price'], y=asks['cash_equivelant'], name="asks"),secondary_y=True,)
        fig.add_trace(go.Scatter(x=bids['accumulated_avg_price'], y=bids['cash_equivelant'], name="bids"),secondary_y=True,)
        fig.update_layout(title_text="cash_equivelant")
        st.plotly_chart(fig, use_container_width=True)

    #     column = bids["price_bid"]
    #     max_value_spot = column.max()
    #     st.write("now",datetime.now())
    #     st.write("best bid", max_value_spot)

    #     column = asks["price_ask"]
    #     min_value_spot = column.min()
    #     st.write("best ask", min_value_spot)

    #     spred_spot = min_value_spot - max_value_spot
    #     st.write("spot spread", spred_spot)

    #     spred_bps_spot = spred_spot/min_value_spot*1000
    #     st.write("spred_bps", spred_bps_spot , "bps")
    # # await asyncio.sleep(30)

def on_error(ws, error):
    print(error)

def on_close(close_msg):
    print("### closed ###" + close_msg)

def streamTrades(currency):
    # websocket.enableTrace(False)
    socket = f'wss://stream.binance.com:9443/ws/{currency}@trade'
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()

def Partial_Book_Depth_Streams(currency):
    # websocket.enableTrace(False)
    socket = f'wss://stream.binance.com:9443/ws/{currency}@depth20'
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()

# streamTrades('btcbusd')
Partial_Book_Depth_Streams('btcbusd')
