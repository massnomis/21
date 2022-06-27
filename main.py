import asyncio
from asyncio import futures
# from glob import glob
# from numpy import full_like
# from rx import empty
import websockets
import json
import streamlit as st
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
            # if message["type"] == "subscribed":
            #     print("subbed, data coming")
            if message["type"] == "partial":
                data_init = message['data']
                data = data_init['data']
                namez = pd.DataFrame.from_dict(data)
                names = namez.iloc[0]
                names = pd.DataFrame(names)
                # st.write(names)
                enabled = namez.iloc[1]
                # st.write(enabled.dropna())
                post_only = namez.iloc[2]
                # st.write(post_only.dropna())
                price_increments = namez.iloc[3]
                # st.write(price_increments.dropna())
                size_increments = namez.iloc[4]
                # st.write(size_increments.dropna())    
                types = namez.iloc[5].dropna()
                # st.write(types)
                types = pd.DataFrame(types)

                merged = names.merge(types, left_index=True, right_index=True)
                # st.write(merged)
                spot = merged.loc[merged["type"] == "spot"]
                # perps_dated.index.rename('name', inplace=True)

                # st.write("spot", spot)
           
            
                merged['expiry'] = merged['name'].str[-4:]
                perpsz = merged.loc[merged["expiry"] == "PERP"]
                
                perpsz['name_shorten_perps'] = perpsz["name"].str[:-5]
                perpsz = perpsz.drop(columns=['type'])
                # perps = merged.loc[merged["name"].str[-4:] == "PERP"]
                # st.write("perpsz", perpsz)
                dated = merged.loc[merged["type"] != "spot"]
                dated = dated.loc[dated["expiry"] != "PERP"]

                dated['name_shorten_dated'] = dated["name"].str[:-5]
                dated = dated.drop(columns=['type'])
                # st.write("dated", dated)

                # st.write(dated["name_shorten_dated"])

                base = namez.iloc[6]
                quote = namez.iloc[7]
                # st.write(base.dropna())  
                base = pd.DataFrame(base)
                quote = pd.DataFrame(quote)
                base = base.dropna()
                quote = quote.dropna()
             
                base_quote = base.merge(quote, left_index=True, right_index=True)
                # st.write(base_quote)
                base_quote_spot = base_quote.merge(spot, left_index=True, right_index=True)
                # st.write("base_quote_spot", base_quote_spot)
                restricted = namez.iloc[8]
                # st.write(restricted.dropna())
                underlyings = namez.iloc[9]
                # st.write(underlyings.dropna())
                name10 = namez.iloc[10]
                # st.write(name10)    
                high_leverage = namez.iloc[11]
                # st.write(high_leverage.dropna())
                large_order_threshholds = namez.iloc[12]
                # st.write(large_order_threshholds)
                futures_descriptions = pd.DataFrame(name10.dropna())
                merge_v1 = base_quote_spot.merge(dated, left_on="baseCurrency",right_on="name_shorten_dated")
                # st.write("merge_v1", merge_v1)
                merge_v2 = merge_v1.merge(perpsz, left_on="baseCurrency",right_on="name_shorten_perps")
                st.write("triangular", merge_v2)
                # st.write(futures_descriptions.dropna())
                # name13 = namez.iloc[13]
                # st.write(name13)
                # name14 = namez.iloc[14]
                # st.write(name14)
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