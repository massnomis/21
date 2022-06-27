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
merge_v2_USD = pd.DataFrame()
# df = pd.DataFrame(columns = ['id', 'price', 'size', 'side', 'liquidation', 'time'])
placeholder = st.empty()
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
            global merge_v2_USD
            with placeholder.container():
                if message["type"] == "partial":
                    data_init = message['data']
                    data = data_init['data']
                    namez = pd.DataFrame.from_dict(data)
                    names = namez.iloc[0]
                    names = pd.DataFrame(names)    
                    types = namez.iloc[5].dropna()
                    types = pd.DataFrame(types)
                    merged = names.merge(types, left_index=True, right_index=True)
                    spot = merged.loc[merged["type"] == "spot"]
                    merged['expiry'] = merged['name'].str[-4:]
                    perpsz = merged.loc[merged["expiry"] == "PERP"]
                    perpsz['name_shorten_perps'] = perpsz["name"].str[:-5]
                    perpsz = perpsz.drop(columns=['type'])
                    dated = merged.loc[merged["type"] != "spot"]
                    dated = dated.loc[dated["expiry"] != "PERP"]
                    dated['name_shorten_dated'] = dated["name"].str[:-5]
                    dated = dated.drop(columns=['type'])
                    base = namez.iloc[6]
                    quote = namez.iloc[7]
                    base = pd.DataFrame(base)
                    quote = pd.DataFrame(quote)
                    base = base.dropna()
                    quote = quote.dropna()
                    base_quote = base.merge(quote, left_index=True, right_index=True)
                    base_quote_spot = base_quote.merge(spot, left_index=True, right_index=True)
                    merge_v1 = base_quote_spot.merge(dated, left_on="baseCurrency",right_on="name_shorten_dated")
                    merge_v2 = merge_v1.merge(perpsz, left_on="baseCurrency",right_on="name_shorten_perps")
                    merge_v2_USD = merge_v2.loc[merge_v2["quoteCurrency"] == "USD"]

            # st.write("triangular", merge_v2_USD)
                    break
                    # break
asyncio.run(consumer())
st.write(merge_v2_USD)

for row in merge_v2_USD:
    st.write(merge_v2_USD[row])
    # st.write(name_x)
