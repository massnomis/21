import asyncio
from glob import glob
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

df = pd.DataFrame(columns = ['id', 'price', 'size', 'side', 'liquidation', 'time'])
placeholder1 = st.empty()

# for seconds in range(200):
# while True: 

 

async def consumer() -> None:
    async with websockets.connect("wss://ftx.com/ws/", ping_interval=20, ping_timeout=2000) as websocket:
        await websocket.send(
            json.dumps(
                {"op": "subscribe", "channel": "trades", "market": "BTC-PERP"}
            )
        )

        async for message in websocket:
            message = json.loads(message)
            if message["type"] == "update":
                result = message["data"]
                # for record in result:
                #     totalVol += record["size"] * record["price"]
                global df
                df1 = pd.DataFrame(result)
                df1['size_new'] = df1["size"][0]
                # df1['size_new'] = size
            
                df = df.append(df1, ignore_index=True)
                # df = df.append(size, ignore_index=True)
                # st.write(size)
                with placeholder1.container():
                    # st.write(df)
              
                    # global df
                    # st.write(size)
                    # size = df["size"][0]
                    # df['size_new'] = size

                    st.plotly_chart(px.scatter(df, y="time", x="price", color="side", size='size_new'),use_container_width=True)
                    # st.write(size)
                        # st.write(df)
    # await asyncio.sleep(30)

asyncio.run(consumer())
