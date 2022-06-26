import asyncio
from glob import glob
from numpy import full_like
from rx import empty
import websockets
import json
import streamlit as st
import pandas as pd
import time
import plotly.express as px
from itertools import accumulate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
st.set_page_config(layout="wide")
placeholder1 = st.empty()

# df = pd.DataFrame(columns = ['id', 'price', 'size', 'side', 'liquidation', 'time'])

# # for seconds in range(200):
# # while True: 
# dict_dumps = {
#   "op": "subscribe",
#   "channel": "trades",
#   "market": "BTC-PERP"
# }

# name = st.text_input("market name", "BTC-PERP")
# dict_dumps["market"] = name
# dumps =  '''{"op": "subscribe", "channel": "trades", "market": ''' 
# rest = f'''"{name}"'''
# last = "}"
# full_dump = dumps + rest + last
# full_dump.astype(dict)
# st.write(dict_dumps)

async def consumer() -> None:

    async with websockets.connect("wss://ftx.com/ws/", ping_interval=20, ping_timeout=2000) as websocket:
        await websocket.send(
            json.dumps(
                {"op": "subscribe", "channel": "markets"}
            #   full_dump
            # 
            # dict_dumps
            )
        )

        async for message in websocket:
            message = json.loads(message)
            # with placeholder1.container():

            if message["type"] == "subscribed":
                st.write("subbed, data coming")
            if message["type"] == "partial":
                data_init = message['data']
                data = data_init['data']
                name = pd.DataFrame.from_dict(data)
                # name = data[0]['name']
            # """"get the data from the message, its a dict, we need the name of each """


                # data = data[0]
                # data = pd.DataFrame(data)
                print(name)
                # global name
            # list = pd.DataFrame(message, index=0)
            # st.dataframe(list)
            # if message["type"] == "update":
            #     result = message["data"]
            #     st.write(result)
                # for record in result:
                #     totalVol += record["size"] * record["price"]
    #             global df
    #             df1 = pd.DataFrame(result)
    #             df1['size_new'] = df1["size"][0]
    #             # df1['size_new'] = size
            
    #             df = df.append(df1, ignore_index=True)
    #             # df = df.append(size, ignore_index=True)
    #             # st.write(size)
    #             with placeholder1.container():
    #                 # st.write(df)
              
    #                 # global df
    #                 # st.write(size)
    #                 # size = df["size"][0]
    #                 # df['size_new'] = size

    #                 st.plotly_chart(px.scatter(df, x="time", y="price", color="side", size='size_new'),use_container_width=True)
    #                 # st.write(size)
    #                     # st.write(df)
    # # await asyncio.sleep(30)

asyncio.run(consumer())
st.write(name)