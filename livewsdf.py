import asyncio
import websockets
import json
import streamlit as st
import time
import plotly.express as px
import pandas as pd
from itertools import accumulate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# import plotly.express as px

# df = pd.DataFrame(columns = ['id', 'price', 'size', 'side', 'liquidation', 'time'])
# placeholder1 = st.empty()
# for seconds in range(200):
# while True: 
a = "Subscribed to orderbook"

b = "fat d8ta"
placeholder1 = st.empty()


async def consumer() -> None:
    async with websockets.connect("wss://ftx.com/ws/") as websocket:
        await websocket.send(
            json.dumps(
                {"op": "subscribe", "channel": "orderbook", "market": "BTC-PERP"}
            )
        )
        async for message in websocket:
            global a
            global b

            message = json.loads(message)
            with placeholder1.container():

                if message["type"] == "subscribed":
                    st.write(a)

                if message["type"] == "partial":
                    market = message["market"]
                    type = message["type"]
                    channel = message["channel"]
                    data = message["data"]
                    time  = data["time"]
                    checksum = data["checksum"]
                    bids = data["bids"]
                    bids = pd.DataFrame(bids)
                    bids = bids.rename(columns={0: "price_bid", 1: "size_bid"})

                    asks = data["asks"]
                    asks = pd.DataFrame(asks)
                    asks = asks.rename(columns={0: "price_ask", 1: "size_ask"})
                    action = data["action"]
                    # st.write('2', bids, asks, action)

                    # return bids, asks, action, time, checksum
                if message["type"] == "update":
                    # global asks
                    # global bids
                    st.write(b)
                    type_update = message["type"]
                    channel_update = message["channel"]
                    data_update = message["data"]
                    time_update  = data_update["time"]
                    checksum = data_update["checksum"]
                    bids_update = pd.DataFrame(data_update["bids"])
                    # bids_update = pd.DataFrame(bids)
                    bids_update = bids_update.rename(columns={0: "price_bid", 1: "size_bid"})
                    # bids_update = bids_update.append(bids_update)

                    asks_update = pd.DataFrame(data_update["asks"])
                    # asks_update = pd.DataFrame(asks)
                    asks_update = asks_update.rename(columns={0: "price_ask", 1: "size_ask"})
                    action = data_update["action"]

                    # st.write(bids_update, asks_update)
                    

                    # def update_asks(asks_update, asks):
                    # """replace new data points in asks with data in asks_update"""
                    for i in range(len(asks_update)):
                        asks.loc[asks["price_ask"] == asks_update.iloc[i]["price_ask"], "size_ask"] = asks_update.iloc[i]["size_ask"]
                        # return asks, asks_update
                    # def update_bids(bids_update, bids):
                    # """replace new data points in bids with data in bids_update"""
                    for i in range(len(bids_update)):
                        bids.loc[bids["price_bid"] == bids_update.iloc[i]["price_bid"], "size_bid"] = bids_update.iloc[i]["size_bid"]
                        # return bids, bids_update

                    # asks = update_asks(asks_update, asks)
                    # bids = update_bids(bids_update, bids)
                    asks = pd.DataFrame(asks)
                    bids = pd.DataFrame(bids)
                    st.write(asks,bids)
                    # # return bids, asks, action, time, checksum
  
                    asks['accumulated']  = (list(accumulate(asks['size_ask'])))
                    asks['accumulated_price']  = (asks['price_ask']) * asks['size_ask']
                    asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
                    asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']


                    bids['accumulated']  = (list(accumulate(bids['size_bid'])))
                    bids['accumulated_price']  = (bids['price_bid']) * bids['size_bid']
                    bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
                    bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']
                    
                    fig = make_subplots(specs=[[{"secondary_y": True}]])

                    # Add traces
                    fig.add_trace(

                        go.Scatter(x=asks['price_ask'], y=asks['accumulated'], name="asks"),
                        secondary_y=True,
                    )

                    fig.add_trace(
                        go.Scatter(x=bids['price_bid'], y=bids['accumulated'], name="bids"),
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
                        go.Bar(x=asks['price_ask'], y=asks['size_ask'], name="asks"),
                        secondary_y=False,
                    )

                    fig.add_trace(
                        go.Bar(x=bids['price_bid'], y=bids['size_bid'], name="bids"),
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
                    # # asks_update = asks.append(asks_update)

                    # st.write(asks, bids)

                    # def update_df(bids_update, asks_update):
                    #     df = df.append(new_df)
                    #     return df

                    # def update_df_ask(asks_update):
                    #     global asks
                    #     asks = asks.append(asks_update)
                    #     return asks_update
                    # def update_df_bid(bids_update):
                    #     global bids
                    #     bids = bids.append(bids_update)
                    # #     return bids_update
                    # update_df_ask(asks_update)
                    # # update_df_bid(bids_update)
                    # st.write(bids)
                    # st.write(asks)
                    # """
                    # update the dataframe with the new data

                    # """



                    # st.write('3',b, message, market, type, channel, data, time, checksum, bids, asks, action)
                    # break

                    # for record in result:
                    # totalVol += record["size"] * record["price"]
            #     global df
                            #    result = message["data"]

            #     df = df.append(result, ignore_index=True)
            #     with placeholder1.container():
            # st.write(message)
                    # st.plotly_chart(px.scatter(df, x="time", y="price", color="side",  size='size'))

                        # st.write(df)

asyncio.run(consumer())









# df2 = pd.DataFrame(columns = ['action', 'bids', 'asks', 'checksum', 'time'])
# placeholder2 = st.empty()
# # for seconds in range(200):
# # while True: 

 

# async def consumer() -> None:
#     async with websockets.connect("wss://ftx.com/ws/") as websocket:
#         await websocket.send(
#             json.dumps(
#                 {"op": "subscribe", "channel": "orderbook", "market": "BTC-PERP"}
#             )
#         )
#         totalVol = 0
#         async for message in websocket:
#             message = json.loads(message)
#             if message["type"] == "update":
#                 result = message["data"]

#                 global df2
           
#                 df2 = df2.append(result, ignore_index=True)
#                 with placeholder2.container():
#                     st.write(df2)

#                         # st.write(df)

# asyncio.run(consumer())















# import json   


# import pandas as pd
# import websocket

# df = pd.DataFrame(columns=['foreignNotional', 'grossValue', 'homeNotional', 'price', 'side',
#                            'size', 'symbol', 'tickDirection', 'timestamp', 'trdMatchID'])


# def on_message(ws, message):
#     msg = json.loads(message)
#     print(msg)
#     global df
#     # `ignore_index=True` has to be provided, otherwise you'll get
#     # "Can only append a Series if ignore_index=True or if the Series has a name" errors
#     df = df.append(msg, ignore_index=True)


# def on_error(ws, error):
#     print(error)


# def on_close(ws):
#     print("### closed ###")


# def on_open(ws):
#     return


# if __name__ == "__main__":
#     ws = websocket.WebSocketApp("wss://www.bitmex.com/realtime?subscribe=trade:XBTUSD",
#                                 on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
#     ws.run_forever()
