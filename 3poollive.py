# from websockets import connect
# from eth_abi import decode_single, decode_abi
import pandas as pd
import streamlit as st
from web3 import Web3
import plotly.express as px
from websockets import connect
from eth_abi import decode_single, decode_abi

import requests
import json
import asyncio

# threepool = '0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7'
# topic = '0x8b3e96f2b889fa771c53c981b40daf005f63f637f1869f707052d15a3dd97140'

# sold_id = decode_single('(int128)',bytearray.fromhex(["topics"][1][2:]))
# tokens_sold = decode_single('(uint256)',bytearray.fromhex(["topics"][2][2:]))
# bought_id = decode_single('(int128)',bytearray.fromhex(["topics"][3][2:]))
# tokens_bought = decode_single('(uint256)',bytearray.fromhex(["topics"][4][2:]))


# simmilarly to usdt_live.py, we need to connect to ws://mainnet.infura.io/ws/v3/43b2d6f15d164cb4bbe4d4789831f242
placeholder = st.empty()
placeholder2 = st.empty()
placeholder3 = st.empty()
placeholder4 = st.empty()

df = pd.DataFrame(columns=['sold_id','tokens_sold','bought_id','tokens_bought', 'timdstamp'])

false = False
session = requests.Session()
w3 = Web3(Web3.WebsocketProvider("wss://mainnet.infura.io/ws/v3/43b2d6f15d164cb4bbe4d4789831f242"))
async def get_events():
    global df
    async with connect("wss://mainnet.infura.io/ws/v3/43b2d6f15d164cb4bbe4d4789831f242") as ws:

        await ws.send(json.dumps(
         
                 {"id": 1, "method": "eth_subscribe", "params":
                 ["logs", 
                 {"address": "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7", 
                 "topics": ["0x8b3e96f2b889fa771c53c981b40daf005f63f637f1869f707052d15a3dd97140"]
                 }
                 ]
                 }
                 )
                 )
        subscription_response = await ws.recv()
        with placeholder:
            placeholder.json(subscription_response)

        while True:
            message = await asyncio.wait_for(ws.recv(), timeout=1000)
            message = json.loads(message)
            message = json.dumps(message)
            message = json.loads(message)
            message = message['params']['result']
            # sold_id = decode_single('(int128)',bytearray.fromhex(message["topics"][1][2:]))
            # tokens_sold = decode_single('(uint256)',bytearray.fromhex(message["topics"][2][2:]))
            # bought_id = decode_single('(int128)',bytearray.fromhex(message["topics"][3][2:]))
            # tokens_bought = decode_single('(uint256)',bytearray.fromhex(message["topics"][4][2:]))
            # if message['method'] == 'eth_subscription':
            with placeholder2:
                placeholder2.json(message)
            # df = df.append({'sold_id': sold_id, 'tokens_sold': tokens_sold, 'bought_id': bought_id, 'tokens_bought': tokens_bought, 'timestamp': message['timestamp']}, ignore_index=True)
            # with placeholder3:
            #     placeholder3.write(df)
            # st.write(message['params']['result'])
        # st.json(subscription_response)
        # print(subscription_response)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
while True:
    loop.run_until_complete(get_events())
# loop.run_until_complete(get_events())
