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
import numpy

df = pd.DataFrame()
fixed_df = pd.DataFrame()
trades_spread = pd.DataFrame()
trades_spread_to_append = pd.DataFrame()
time = pd.DataFrame()
# fixed_df = pd.DataFrame(columns=['m'], dtype=str)
bids = pd.DataFrame()
asks = pd.DataFrame()
best_ask = pd.DataFrame()
best_bid = pd.DataFrame()
st.set_page_config(layout="wide")
placeholder1 = st.empty()
placeholder2 = st.empty()
placeholder3 = st.empty()

def on_open(ws):
    print("open")

def on_message(ws,message):
    json_message = json.loads(message) 
    # st.write(json_message)
    # message = json.loads(message)
    global df
    global fixed_df
    global trades_spread
    global trades_spread_to_append
    global asks
    global bids
    global time
    global best_ask
    global best_bid
    with placeholder1.container():
        # st.write(json_message)
        data = json_message['data']
        data_type = data['e']
        # st.write(data_type)
        if data_type == "trade":
# depthUpdate
# trade
            trade = data
        # if json_message['stream'] == "btcbusd@trade":
    #         st.write(json_message)

    #         trade = json_message['data']
    #         st.write(trade)
            df1 = pd.DataFrame.from_dict([trade])
            df1['Event_time'] = df1['E'].astype(float)

            df1['Event_time'] = pd.to_datetime(df1['E'], unit='ms')
            # st.write(df1)
            df = df.append(df1, ignore_index=False)
            # m = df['m']
            df['m'] = df['m'].astype(str)
            df['Is_the_buyer_the_market_maker'] = df['m']
            df['Ignore'] = df['M'].astype(str)
            
            # df['E'] = df['E'].astype(float)
            df['Symbol'] = df['s'].astype(str)
            df['Price'] = df['p'].astype(float)
            df['Quantity'] = df['q'].astype(float)
            df['Trade_ID'] = df['T'].astype(str)
    
            df['sum'] = df['Quantity'].cumsum()
            # st.write(df)
            st.plotly_chart(px.scatter(df, x="Event_time", y="Price", color="Is_the_buyer_the_market_maker", size='Quantity',marginal_y="histogram", marginal_x="rug"),use_container_width=True)

            st.plotly_chart(px.line(df, x="Event_time", y="sum"),use_container_width=True)

    with placeholder2.container():

        if data_type == "depthUpdate":
# depthUpdate
    # if json_message['stream'] == "btcbusd@depth":
    #     st.write(json_message)

    #     depth = json_message['data']
            # time = data['E']
            depthUpdate = data
            time = pd.to_datetime(data['E'], unit='ms')
            st.write(time)
            bids = depthUpdate["b"]
            bids = pd.DataFrame(bids)
            bids = bids.rename(columns={0: "price_bid", 1: "size_bid"})
            asks = depthUpdate["a"]
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
                # best_ask = (bids['price_ask'].min())

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
                # best_bid = (bids['price_bid'].max())
            for i in range(1, 2):
                cols = st.columns(2)
                cols[0].subheader("bids")
                # cols[0].write(bids['price_bid'].max())
                cols[0].write(bids)
                cols[1].subheader("asks")
                # cols[1].write(asks['price_ask'].min())

                cols[1].write(asks)

            st.write((asks['price_ask'].min())-(bids['price_bid'].max()),((asks['price_ask'].min())-(bids['price_bid'].max()))/(asks['price_ask'].min())*1000)
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=asks['price_ask'], y=asks['accumulated'], name="asks"),secondary_y=True,)
            fig.add_trace(go.Scatter(x=bids['price_bid'], y=bids['accumulated'], name="bids"),secondary_y=True,)
            fig.update_layout(title_text="orderbook")
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

def on_close(ws, close_status_code, close_msg):
    print("closed")
  
SOCK = "wss://stream.binance.com:9443/stream?streams=btcbusd@trade/btcbusd@depth"

ws = websocket.WebSocketApp(SOCK, on_open=on_open,on_close=on_close, on_message=on_message)
ws.run_forever()