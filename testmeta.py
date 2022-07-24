import asyncio
import json
from numpy import place
# import streamlit as st
from web3 import Web3
# import plotly.express as px
# from web3.middleware import geth_poa_middleware # only needed for PoA networks like BSC
import requests
from websockets import connect
from eth_abi import decode_single, decode_abi
import math
from datetime import datetime
import pandas as pd
# df = pd.DataFrame(columns=['from', 'to', 'value'])
# fixed_df = pd.DataFrame()
# fixed_df = pd.DataFrame(columns=['m'], dtype=str)



# st.set_page_config(layout="wide")
# def bollinger_strat(df, window, no_of_std):
#     rolling_mean = df['value'].rolling(window).mean()
#     rolling_std = df['value'].rolling(window).std()
#     df['rolling_mean_value'] = rolling_mean

#     df['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
#     df['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
#     return df['Bollinger High'] , df['Bollinger Low'], df['rolling_mean_value'] 
# def bollinger_strat2(df, window, no_of_std):
#     rolling_mean = df['cumsum'].rolling(window).mean()
#     rolling_std = df['cumsum'].rolling(window).std()
#     df['rolling_mean_cumsum'] = rolling_mean

#     df['Bollinger High_cumsum'] = rolling_mean + (rolling_std * no_of_std)
#     df['Bollinger Low_cumsum'] = rolling_mean - (rolling_std * no_of_std)     
#     return df['Bollinger High_cumsum'] , df['Bollinger Low_cumsum'], df['rolling_mean_cumsum'] 

# placeholder1 = st.empty()
# placeholder2 = st.empty()
# placeholder3 = st.empty()
# placeholder4 = st.empty()
# placeholder5 = st.empty()
# placeholder6 = st.empty()
# placeholder7 = st.empty()
# placeholder8 = st.empty()
# placeholder9 = st.empty()
# placeholder10 = st.empty()
# placeholder11 = st.empty()
# placeholder12 = st.empty()

# adapter = requests.sessions.HTTPAdapter(pool_connections=50000, pool_maxsize=50000) # pool connections and max size are for HTTP calls only, since we are using WS they are not needed. 
session = requests.Session()
w3 = Web3(Web3.WebsocketProvider("wss://mainnet.infura.io/ws/v3/43b2d6f15d164cb4bbe4d4789831f242"))
# w3.middleware_onion.inject(geth_poa_middleware, layer=0) # only needed for PoA networks like BSC
# df = pd.DataFrame(columns=['from', 'to', 'value'])
false = False
async def get_event():
    # global df
    global df
    global fixed_df
    async with connect("wss://mainnet.infura.io/ws/v3/43b2d6f15d164cb4bbe4d4789831f242") as ws:
        global df
        # global fixed_df
        await ws.send(json.dumps(
        {"id": 1, "method": "eth_subscribe", "params": 
        ["logs", 
        {"address": "0x881d40237659c251811cec9c364ef91dc08d300c",
        "topics":["0xbeee1e6e7fe307ddcf84b0a16137a4430ad5e2480fc4f4a8e250ab56ccd7630d"]
        }
        ]
        }
        )
        )
        subscription_response = await ws.recv()
        # with placeholder1:
        print(subscription_response)
        while True:
            # global df
            # global fixed_df
            message = await asyncio.wait_for(ws.recv(), timeout=600)
            lord_jesus = json.loads(message)
            lord_jesus = json.dumps(lord_jesus)
            lord_jesus = json.loads(lord_jesus)
            print(lord_jesus)
#             lord_jesus = lord_jesus["params"]["result"]
#             number = lord_jesus["data"][2:]
#             addy1 = lord_jesus["topics"][1][2:]
#             addy2 = lord_jesus["topics"][2][2:]
#             number = decode_single('(uint256)',bytearray.fromhex(number))
#             addy1 = decode_single('(address)',bytearray.fromhex(addy1))
#             addy2 = decode_single('(address)',bytearray.fromhex(addy2))
#             number = number[0]
#             number = number / math.pow(10,6)
#             addy1 = addy1[0]
#             addy2 = addy2[0]
#             # st.write(number)
#             # st.write(addy1)
#             # st.write(addy2)
#             now = datetime.now()
#             d = {'from': addy1, 'to': addy2, 'value': number, 'time': now}
#             fixed_df = pd.DataFrame(d, index=[0])
#             df = df.append(fixed_df, ignore_index=True)
#             df['cumsum'] = df['value'].cumsum()
#             bollinger_strat(df=df,window=10,no_of_std=2)
#             bollinger_strat2(df=df,window=10,no_of_std=2)

#             # df['from'].append = addy1
#             # df['to'].append = addy2
#             # df['value'].append = number     
#             with placeholder2:
#                 # global df
#                 # df = df.append(([addy1,addy2,number]),ignore_index=True)
              
#             # df = df.append(([addy1,addy2,number]),ignore_index=True)  
#                 st.write(df,use_container_width=True)
#             with placeholder3:
#                 st.plotly_chart(px.bar(df, x='cumsum', y='value'),use_container_width=True)
#             with placeholder4:
#                 st.plotly_chart(px.scatter(df, x='cumsum', y='rolling_mean_value',marginal_y="violin", marginal_x="rug"),use_container_width=True)
#             with placeholder5:
#                 st.plotly_chart(px.line(df, x='time', y='rolling_mean_cumsum'),use_container_width=True)
#             with placeholder6:
#                 st.plotly_chart(px.scatter(df, x='time', y=['value','rolling_mean_value','Bollinger High','Bollinger Low'],marginal_y="violin", marginal_x="rug"),use_container_width=True)
#             with placeholder7:
#                 st.plotly_chart(px.scatter(df, x='time', y='cumsum', size='value',marginal_y="violin", marginal_x="rug"),use_container_width=True)
#             with placeholder8:
#                 st.plotly_chart(px.scatter(df, x='time', y=['Bollinger High_cumsum','Bollinger Low_cumsum','rolling_mean_cumsum','cumsum'], size = 'value',marginal_y="violin", marginal_x="rug"),use_container_width=True)
# # if _name_ == "_main_":
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
while True:
    loop.run_until_complete(get_event())

# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)