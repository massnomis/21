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
        df1['E'] = df1['E'].astype(float)

        df1['E'] = pd.to_datetime(df1['E'], unit='ms')
        # st.write(df1)
        df = df.append(df1, ignore_index=False)
        # m = df['m']
        df['m'] = df['m'].astype(str)
        df['buy'] = df['m']
        df['M'] = df['M'].astype(str)
        
        # df['E'] = df['E'].astype(float)
        df['s'] = df['s'].astype(str)
        df['p'] = df['p'].astype(float)
        df['q'] = df['q'].astype(float)
        df['T'] = df['T'].astype(str)
 
        df['sum'] = df['q'].cumsum()
        st.write(df)
        st.plotly_chart(px.scatter(df, x="E", y="p", color="buy", size='q'),use_container_width=True)
        st.plotly_chart(px.line(df, x="E", y="sum", color="buy"),use_container_width=True)

        # st.plotly_chart(px.scatter(df2, x="E", y="q"),use_container_width=True)

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


# import websocket
# import datetime
# import streamlit as st
# import time
# import json
# import plotly.express as px
# import pandas as pd
# from itertools import accumulate
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import numpy

# df = pd.DataFrame()
# fixed_df = pd.DataFrame()
# # fixed_df = pd.DataFrame(columns=['m'], dtype=str)

# st.set_page_config(layout="wide")
# placeholder1 = st.empty()

# # import websocket-client
# def on_message(ws, message):
#     # print()
#     # print(str(datetime.datetime.now()) + ": ")
#     message = json.loads(message)
#     global df
#     global fixed_df
#     with placeholder1.container():

#         df1 = pd.DataFrame.from_dict([message])
        
#         df = df.append(df1, ignore_index=False)
#         # m = df['m']
#         df['m'] = df['m'].astype(str)
#         df['maker'] = df['m']
#         df['M'] = df['M'].astype(str)
#         df['E'] = pd.to_datetime(df['E'], unit='ms')
#         df['s'] = df['s'].astype(str)
#         df['p'] = df['p'].astype(float)
#         df['q'] = df['q'].astype(float)
#         # df['T'] = df['T'].astype(float)
#         # E = df['E'] 
#         # E = pd.to_datetime(E, unit='ms')
#         # df['E'] = E
#         # df['T'] = pd.to_datetime['T']
#         st.write(df)
#         st.plotly_chart(px.scatter(df, x="E", y="p", color="maker", size='q'),use_container_width=True)

# def on_error(ws, error):
#     print(error)

# def on_close(close_msg):
#     print("### closed ###" + close_msg)

# def streamTrades(currency):
#     # websocket.enableTrace(False)
#     socket = f'wss://stream.binance.com:9443/ws/{currency}@trade'
#     ws = websocket.WebSocketApp(socket,
#                                 on_message=on_message,
#                                 on_error=on_error,
#                                 on_close=on_close)
#     ws.run_forever()
# streamTrades('btcbusd')