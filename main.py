import asyncio
# from glob import glob
# from numpy import full_like
# from rx import empty
import websockets
import json
# import streamlit as st
import pandas as pd
# import time
# import plotly.express as px
# from itertools import accumulate
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# st.set_page_config(layout="wide")
# placeholder1 = st.empty()

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
        await websocket.send(json.dumps({"op": "subscribe", "channel": "markets"}))
        async for message in websocket:
            message = json.loads(message)
            if message["type"] == "subscribed":
                print("subbed, data coming")
            if message["type"] == "partial":
                data_init = message['data']
                data = data_init['data']
                namez = pd.DataFrame.from_dict(data)
                # name1 = namez.iloc[1]
                # print(name1)
                name0 = namez.iloc[0]
                print(name0)
asyncio.run(consumer())
# async def consumer() -> None:
#     global websocket
#     async with websockets.connect("wss://ftx.com/ws/", ping_interval=20, ping_timeout=2000) as websocket:
#         await websocket.send(json.dumps({"op": "subscribe", "channel": "markets"}))
#         async for message in websocket:
#             message = json.loads(message)
#             if message["type"] == "subscribed":
#                 print("subbed, data coming")
#             if message["type"] == "partial":
#                 data_init = message['data']
#                 data = data_init['data']
#                 name = pd.DataFrame.from_dict(data)
#                 print(name)
# asyncio.run(consumer())