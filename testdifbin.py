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
        bids = message["b"]
        bids = pd.DataFrame(bids)
        bids = bids.rename(columns={0: "price_bid", 1: "size_bid"})
        asks = message["a"]
        asks = pd.DataFrame(asks)
  

        asks = asks.rename(columns={0: "price_ask", 1: "size_ask"})
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
        for i in range(len(asks)):
            asks = asks[asks['size_ask'] != 0]

                        # global asks_update
                        # if asks_update['price_ask'][i] == bids_update['price_bid'][i]:
                            # global bids_update
                        # asks.append(asks_update.loc[i])

                        # asks.reset_index(drop = True, inplace=True)
                        # asks.dropna(inplace=True)
            asks.dropna(inplace=True)

            asks = asks.drop_duplicates(subset=['price_ask'], keep='first')
            asks.sort_values(by=['price_ask'], inplace=True)
            asks.reset_index(drop = True, inplace=False)

        for i in range(len(bids)):
                        # global bids_update
                        # if bids_update['price_bid'][i] == asks_update['price_ask'][i]:
                            # global asks_update
                        # bids.reset_index(drop = True, inplace=True)

                        # bids.dropna(inplace=True)
            bids= bids[bids['size_bid'] != 0]

            bids.reset_index(drop=True)
                        # bids.append(bids_update.loc[i])
            bids.dropna(inplace=True)
            bids = bids.drop_duplicates(subset=['price_bid'], keep='first')
            bids.sort_values(by=['price_bid'], inplace=True, ascending=False)
            bids.reset_index(drop=True, inplace=False)

        for i in range(1, 2):
            cols = st.columns(2)
            cols[0].subheader("bids")

            cols[0].write(bids)

            cols[1].subheader("asks")

            cols[1].write(asks)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=asks['price_ask'], y=asks['accumulated'], name="asks"),secondary_y=True,)
        fig.add_trace(go.Scatter(x=bids['price_bid'], y=bids['accumulated'], name="bids"),secondary_y=True,)
        fig.update_layout(title_text="orderbook")
        st.plotly_chart(fig, use_container_width=True)
        
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
        # st.write(message)

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
    socket = f'wss://stream.binance.com:9443/ws/{currency}@depth'
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()

# streamTrades('btcbusd')
Partial_Book_Depth_Streams('btcbusd')
