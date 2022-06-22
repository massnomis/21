import streamlit as st
import requests
import json
import pandas as pd
import math
import time
from itertools import accumulate
# from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import chain

import plotly.express as px
from datetime import datetime, timedelta
# ts = int('1645598410')

# print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
import json
import requests
import pandas as pd
import random
st.set_page_config(layout="wide")



placeholder1 = st.empty()
for seconds in range(200):
#while True: 

 

    with placeholder1.container():

        df1 = requests.get(f"https://ftx.com/api/markets/BTC-PERP/orderbook?depth=100").json()
        df1 = pd.DataFrame(df1)




        df1 = df1['result']
        asks = df1['asks']
        bids = df1['bids']
        asks = pd.DataFrame(asks)
        bids = pd.DataFrame(bids)
        asks = asks.rename(columns={0: "price", 1: "size"})
        bids = bids.rename(columns={0: "price", 1: "size"})

        asks['accumulated_size']  = (list(accumulate(asks['size'])))
        asks['accumulated_price']  = (asks['price']) * asks['size']
        asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated_size']
        asks['cash_equivelant'] = asks['accumulated_size'] * asks['accumulated_avg_price']


        bids['accumulated_size']  = (list(accumulate(bids['size'])))
        bids['accumulated_price']  = (bids['price']) * bids['size']
        bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated_size']
        bids['cash_equivelant'] = bids['accumulated_size'] * bids['accumulated_avg_price']

 



    # asks['price'] = asks[0]
    # asks['size'] = asks[1]
   
            
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Scatter(x=asks['price'], y=asks['accumulated_size'], name="asks"),
            secondary_y=True,
        )

        fig.add_trace(
            go.Scatter(x=bids['price'], y=bids['accumulated_size'], name="bids"),
            secondary_y=True,
        )

        # Add figure title
        fig.update_layout(
            title_text="orderbook"
        )

        # Set x-axis title


        st.plotly_chart(fig, use_container_width=True)



        # fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Bar(x=asks['price'], y=asks['size'], name="asks"),
            secondary_y=True,
        )

        fig.add_trace(
            go.Bar(x=bids['price'], y=bids['size'], name="bids"),
            secondary_y=True,
        )

        # Add figure title
        fig.update_layout(
            title_text="orderbook"
        )

        # Set x-axis title


        st.plotly_chart(fig, use_container_width=True)
        df2 = requests.get(f"https://ftx.com/api/markets/ETH-PERP/orderbook?depth=100").json()
        df2 = pd.DataFrame(df2)




        df2 = df2['result']
        asks = df2['asks']
        bids = df2['bids']
        asks = pd.DataFrame(asks)
        bids = pd.DataFrame(bids)
        asks = asks.rename(columns={0: "price", 1: "size"})
        bids = bids.rename(columns={0: "price", 1: "size"})

        asks['accumulated_size']  = (list(accumulate(asks['size'])))
        asks['accumulated_price']  = (asks['price']) * asks['size']
        asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated_size']
        asks['cash_equivelant'] = asks['accumulated_size'] * asks['accumulated_avg_price']


        bids['accumulated_size']  = (list(accumulate(bids['size'])))
        bids['accumulated_price']  = (bids['price']) * bids['size']
        bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated_size']
        bids['cash_equivelant'] = bids['accumulated_size'] * bids['accumulated_avg_price']

 



    # asks['price'] = asks[0]
    # asks['size'] = asks[1]
   
            
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Scatter(x=asks['price'], y=asks['accumulated_size'], name="asks"),
            secondary_y=True,
        )

        fig.add_trace(
            go.Scatter(x=bids['price'], y=bids['accumulated_size'], name="bids"),
            secondary_y=True,
        )

        # Add figure title
        fig.update_layout(
            title_text="orderbook"
        )

        # Set x-axis title


        st.plotly_chart(fig, use_container_width=True)



        # fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Bar(x=asks['price'], y=asks['size'], name="asks"),
            secondary_y=True,
        )

        fig.add_trace(
            go.Bar(x=bids['price'], y=bids['size'], name="bids"),
            secondary_y=True,
        )

        # Add figure title
        fig.update_layout(
            title_text="orderbook"
        )

        # Set x-axis title


        st.plotly_chart(fig, use_container_width=True)

        time.sleep(1)


