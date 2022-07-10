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

df = pd.DataFrame()


st.set_page_config(layout="wide")
placeholder1 = st.empty()

# import websocket-client
def on_message(ws, message):
    # print()
    # print(str(datetime.datetime.now()) + ": ")
    message = json.loads(message)
    global df
    with placeholder1.container():
        # st.dataframe(message)
        df1 = pd.DataFrame.from_dict([message])
        df = df.append(df1, ignore_index=True)
        # st.write(df)
        # st.write(df1)
        if df["m"] == True:
            df["maker/taker"] = "maker"
            st.write(df["m"])

        else:
            df["maker/taker"] = "taker"
            st.write(df["m"])
 

            # maker = df["m"] == True
        # st.bar_chart(df)
        # st.plotly_chart(px.scatter(df, x='E', y='p', size='q'),use_container_width=True)


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
streamTrades('btcbusd')
