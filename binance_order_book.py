import websocket
import datetime
import streamlit as st
import time
import json
import plotly.express as px
import pandas as pd
from itertools import accumulate
import plotly.graph_objects as go
import requests
from plotly.subplots import make_subplots
# bids = pd.DataFrame()
# asks = pd.DataFrame()
# i = 1
# def og_book():
#     message = requests.get("https://api.binance.com/api/v3/depth?symbol=BTCBUSD&limit=1000").json()
#     # st.write(message)
#     bids = message["bids"]
#     bids = pd.DataFrame(bids)
#     asks = message["asks"]
#     asks = pd.DataFrame(asks)
 
#     bids = bids.rename(columns={0: "price_bid", 1: "size_bid"})




   

    
#     asks = asks.rename(columns={0: "price_ask", 1: "size_ask"})
#     # st.write(bids, asks)
#     return bids, asks

    # bids["price_bid"] = bids["price_bid"].astype(float)
    # bids["size_bid"] = bids["size_bid"].astype(float)
    # asks["price_ask"] = asks["price_ask"].astype(float)
    # asks["size_ask"] = asks["size_ask"].astype(float)
    # asks['accumulated']  = (list(accumulate(asks['size_ask'])))
    # asks['accumulated_price']  = (asks['price_ask']) * asks['size_ask']
    # asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
    # asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']

    # bids['accumulated']  = (list(accumulate(bids['size_bid'])))
    # bids['accumulated_price']  = (bids['price_bid']) * bids['size_bid']
    # bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
    # bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']  
    # st.write(bids,asks)

st.set_page_config(layout="wide")
placeholder1 = st.empty()
# import websocket-client
def on_message(ws, message):
    # print()
    # og_book()
    global i
    # global asks
    # print(str(datetime.datetime.now()) + ": ")
    # st.write(json_message)
    json_message = json.loads(message)
    # st.write(json_message)
    # data = json_message['data']
    data_type = json_message['e']
    # st.write(bids, asks)

    with placeholder1.container():
        # global bids
        # global asks
        # st.write(json_message)
        i = 1
        st.write(i)
        if i == 1:
            message = requests.get("https://api.binance.com/api/v3/depth?symbol=BTCBUSD&limit=1000").json()
            st.write(message)
            bids = message["bids"]
            bids = pd.DataFrame(bids)
            asks = message["asks"]
            asks = pd.DataFrame(asks)
        
            bids = bids.rename(columns={0: "price_bid", 1: "size_bid"})




        

            
            asks = asks.rename(columns={0: "price_ask", 1: "size_ask"})
            i = i+1
            st.write(i)
            st.write(bids, asks)
            # st.write(bids, asks)
            return bids, asks  
    # break   
        # global bids
        # global asks
        else:
# depthUpdate
            # global bids
            # global asks
            # st
    # if json_message['stream'] == "btcbusd@depth":
            # st.write(json_message)

    #     depth = json_message['data']
            # time = data['E']
            # depthUpdate = json_message
            time = pd.to_datetime(json_message['E'], unit='ms')
            st.write(time)
            bids_update = json_message["b"]
            bids_update = pd.DataFrame(bids_update)
            # bids = bids.rename(columns={0: "price_bid", 1: "size_bid"})
            asks_update = json_message["a"]
            asks_update = pd.DataFrame(asks_update)
        # bids = message["bids"]
        # bids = pd.DataFrame(bids)
        # bids = bids.rename(columns={0: "price_bid", 1: "size_bid"})
        # asks = message["asks"]
        # asks = pd.DataFrame(asks)
        # st.write(b, use_container_width=True)
            # type_update = message["type"]
            # channel_update = message["channel"]
            # data_update = message["data"]
            # time_update  = data_update["time"]
            # checksum = data_update["checksum"]
            # bids_update = pd.DataFrame(data_update["bids"])
            bids_update = bids_update.rename(columns={0: "price_bid", 1: "size_bid"})
            # asks_update = pd.DataFrame(data_update["asks"])
            asks_update = asks_update.rename(columns={0: "price_ask", 1: "size_ask"})
            # st.write(bids_update,asks_update)
            # action = data_update["action"]
            # st.write(bids_update,asks_update)
            # global bids
            # global asks
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
                st.write(asks_update)
                st.write(asks)
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
                bids.loc[bids["price_bid"] == bids_update.loc[i]["price_bid"], "size_bid"] = bids_update.loc[i]["size_bid"]

            for i in range(1, 2):
                cols = st.columns(2)
                cols[0].subheader("bids")
                cols[0].write(bids['price_bid'].max())

                cols[0].write(bids)
                cols[1].subheader("asks")
                cols[1].write(asks['price_ask'].min())

                cols[1].write(asks)
            st.write((asks['price_ask'].min())-(bids['price_bid'].max()),((asks['price_ask'].min())-(bids['price_bid'].max()))/(asks['price_ask'].min())*1000)
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=asks['price_ask'], y=asks['accumulated'], name="asks"),secondary_y=True,)
            fig.add_trace(go.Scatter(x=bids['price_bid'], y=bids['accumulated'], name="bids"),secondary_y=True,)
            fig.update_layout(title_text="orderbook")
            st.plotly_chart(fig, use_container_width=True)

            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Bar(x=asks['price_ask'], y=asks['accumulated'], name="asks"),secondary_y=True,)
            fig.add_trace(go.Bar(x=bids['price_bid'], y=bids['accumulated'], name="bids"),secondary_y=True,)
            fig.update_layout(title_text="orderbook")
            # fig.update_traces(width=10)

            st.plotly_chart(fig, use_container_width=True)
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Bar(x=bids['price_bid'], y=bids['size_bid'], name="bids"),secondary_y=True,)
            fig.add_trace(go.Bar(x=asks['price_ask'], y=asks['size_ask'], name="asks"),secondary_y=True,)
            fig.update_layout(title_text="orderbook")
            # fig.update_traces(width=1)
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
    # og_book()
    # websocket.enableTrace(False)
    socket = f'wss://stream.binance.com:9443/ws/{currency}@depth@100ms'
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()

# streamTrades('btcbusd')
Partial_Book_Depth_Streams('btcbusd')
