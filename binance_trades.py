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
# fixed_df = pd.DataFrame(columns=['m'], dtype=str)

st.set_page_config(layout="wide")
placeholder1 = st.empty()

# import websocket-client
def on_message(ws, message):
    # print()
    # print(str(datetime.datetime.now()) + ": ")
    message = json.loads(message)
    global df
    global fixed_df
    with placeholder1.container():

        df1 = pd.DataFrame.from_dict([message])
        
        df = df.append(df1, ignore_index=False)
        # m = df['m']
        df['m'] = df['m'].astype(str)
        df['maker'] = df['m']
        df['M'] = df['M'].astype(str)
        df['E'] = df['E'].astype(float)
        df['s'] = df['s'].astype(str)
        df['p'] = df['p'].astype(float)
        df['q'] = df['q'].astype(float)
        df['T']
        st.write(df)
        st.plotly_chart(px.scatter(df, x="E", y="p", color="maker", size='q'),use_container_width=True)

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
streamTrades('btcbusd')
# e    object
# E     int64
# s    object
# t     int64
# p    object
# q    object
# b     int64
# a     int64
# T     int64
# m      bool
# M      bool