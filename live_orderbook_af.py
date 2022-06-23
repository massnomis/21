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

result = pd.DataFrame(columns = ['time', 'checksum', 'bids', 'asks', 'update'])
placeholder1 = st.empty()

# for seconds in range(200):
# while True:
bids = pd.DataFrame(result["bids"], columns=['0', '1'])
asks = pd.DataFrame(result["asks"], columns=['0', '1'])

async def consumer() -> None:
    async with websockets.connect("wss://ftx.com/ws/") as websocket:
        await websocket.send(
            json.dumps(
                {"op": "subscribe", "channel": "orderbook", "market": "BTC-PERP"}
            )
        )
        totalVol = 0
        async for message in websocket:
            message = json.loads(message)
            if message["type"] == "update":
                result = message["data"]
                global df
                global bids
                global asks
                # df = df.append(result, ignore_index=True)
                # bids = bids.append(result["bids"], ignore_index=True)
                # asks = asks.append(result["asks"], ignore_index=True)
                bids = pd.DataFrame(result["bids"])
                asks = pd.DataFrame(result["asks"])
                if not bids.empty and not asks.empty:

                    with placeholder1.container():
                        # bids = pd.DataFrame({'0': ["0"]} )
                        # bids = asks.append(result["bids"])
                        # asks = pd.DataFrame({'0': ["0"]} )
                        # asks = asks.append(result["asks"])    
                        if not bids.empty and not asks.empty:
                                        # st.write(df)
                            # st.write(bids)
                            # st.write(asks)
                        # st.plotly_chart(px.imshow(bids.T))
                            
                            asks = asks.rename(columns={0: "price", 1: "size"})
                            bids = bids.rename(columns={0: "price", 1: "size"})
                            asks['accumulated']  = (list(accumulate(asks['size'])))
                            asks['accumulated_price']  = (asks['price']) * asks['size']
                            asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
                            asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']


                            bids['accumulated']  = (list(accumulate(bids['size'])))
                            bids['accumulated_price']  = (bids['price']) * bids['size']
                            bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
                            bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']
                           
                            fig = make_subplots(specs=[[{"secondary_y": True}]])

                            # Add traces
                            fig.add_trace(

                                go.Scatter(x=asks['price'], y=asks['accumulated'], name="asks"),
                                secondary_y=True,
                            )

                            fig.add_trace(
                                go.Scatter(x=bids['price'], y=bids['accumulated'], name="bids"),
                                secondary_y=True,
                            )

                            # Add figure title
                            fig.update_layout(
                                title_text="orderbook"
                            )

                            # Set x-axis title


                            st.plotly_chart(fig, use_container_width=True)




                            fig = make_subplots(specs=[[{"secondary_y": True}]])

                            # Add traces
                            fig.add_trace(
                                go.Bar(x=asks['price'], y=asks['size'], name="asks"),
                                secondary_y=False,
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


                            fig = make_subplots(specs=[[{"secondary_y": True}]])

                            # Add traces
                            fig.add_trace(
                                go.Scatter(x=asks['accumulated_avg_price'], y=asks['cash_equivelant'], name="asks"),
                                secondary_y=True,
                            )

                            fig.add_trace(
                                go.Scatter(x=bids['accumulated_avg_price'], y=bids['cash_equivelant'], name="bids"),
                                secondary_y=True,
                            )

                            # Add figure title
                            fig.update_layout(
                                title_text="cash_equivelant"
                            )

                            # Set x-axis title


                            st.plotly_chart(fig, use_container_width=True)
                                                    # st.write(df)

asyncio.run(consumer())
