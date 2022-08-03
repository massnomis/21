import asyncio
import json
from unicodedata import decimal
from numpy import place
import streamlit as st
from web3 import Web3
import plotly.express as px
import requests
from websockets import connect
from eth_abi import decode_single, decode_abi
import math
from datetime import datetime
import pandas as pd
st.set_page_config(page_title="Arbitricrypto", page_icon="🔐", layout="wide")

session = requests.Session()
w3 = Web3(Web3.WebsocketProvider("wss://arb-mainnet.g.alchemy.com/v2/0Yoq6lRIOyxmtUc399eoo3__isBlLIt6"))
df_arbi = pd.DataFrame(columns=['sold_id', 'tokens_sold','sold_name','sold_decimal','tokens_bought','bought_name','bought_decimal','bought_id','timestamp'])
false = False
laceholder1 = st.empty()
laceholder2 = st.empty()
laceholder3 = st.empty()
laceholder4 = st.empty()
laceholder5 = st.empty()
laceholder6 = st.empty()
async def get_event_arbi_tricryp():
    global df_arbi
    async with connect("wss://arb-mainnet.g.alchemy.com/v2/0Yoq6lRIOyxmtUc399eoo3__isBlLIt6") as ws:
        global df_arbi
        await ws.send(json.dumps(
        {"id": 1, "method": "eth_subscribe", "params": 
        ["logs", 
       
  {
    "address": "0x960ea3e3C7FB317332d990873d354E18d7645590",
    "topics": [
      "0xb2e76ae99761dc136e598d4a629bb347eccb9532a5f8bbd72e18467c3c34cc98"
    ]
  }
        ]
        }
        )
        )
        subscription_response = await ws.recv()
        with laceholder1:
            st.write(subscription_response)
        while True:
            global df_arbi
            # global tokens_list
            # global decimal_list
            message = await asyncio.wait_for(ws.recv(), timeout=600)
            lord_jesus = json.loads(message)
            lord_jesus = json.dumps(lord_jesus)
            lord_jesus = json.loads(lord_jesus)
            lord_jesus = lord_jesus["params"]["result"]
            number = lord_jesus["data"][2:]
            number = decode_single('(uint256,uint256,uint256,uint256)',bytearray.fromhex(number))
            now = datetime.now()
            d = {'sold_id': number[0], 'tokens_sold': number[1], 'bought_id':number[2], 'tokens_bought': number[3], 'timestamp': now}
            fixed_df = pd.DataFrame(d, index=[0])
            if d['sold_id'] == 0:
                fixed_df['sold_name'] = 'USDT'
                fixed_df['sold_decimal'] = 6
                fixed_df['tokens_sold_fixed'] = fixed_df['tokens_sold'] / 10**6
            elif d['sold_id'] == 1:
                fixed_df['sold_name'] = 'WBTC'
                fixed_df['sold_decimal'] = 8
                fixed_df['tokens_sold_fixed'] = fixed_df['tokens_sold'] / 10**8
            elif d['sold_id'] == 2:
                fixed_df['sold_name'] = 'WETH'
                fixed_df['sold_decimal'] = 18
                fixed_df['tokens_sold_fixed'] = fixed_df['tokens_sold'] / 10**18
            if d['bought_id'] == 0:
                fixed_df['bought_name'] = 'USDT'
                fixed_df['bought_decimal'] = 6
                fixed_df['tokens_bought_fixed'] = fixed_df['tokens_bought'] / 10**6
            elif d['bought_id'] == 1:
                fixed_df['bought_name'] = 'WBTC'
                fixed_df['bought_decimal'] = 8
                fixed_df['tokens_bought_fixed'] = fixed_df['tokens_bought'] / 10**8
            elif d['bought_id'] == 2:
                fixed_df['bought_name'] = 'WETH'
                fixed_df['bought_decimal'] = 18
                fixed_df['tokens_bought_fixed'] = fixed_df['tokens_bought'] / 10**18
            df = df.append(fixed_df, ignore_index=True)
            df['rate_1_fixed'] = df['tokens_bought_fixed'] / df['tokens_sold_fixed']
            df['rate_2_fixed'] = df['tokens_sold_fixed'] / df['tokens_bought_fixed']
            df['path'] = df['sold_name'] + ' to ' + df['bought_name']
            with laceholder2:
                st.write(df,use_container_width=True)
            with laceholder3:
                st.plotly_chart(px.line(df, x='timestamp', y='rate_1_fixed', color='path'), use_container_width=True)
            with laceholder4:
                st.plotly_chart(px.line(df, x='timestamp', y='rate_2_fixed', color='path'), use_container_width=True)
            with laceholder5:
                st.plotly_chart(px.scatter(df, x='timestamp', y='tokens_bought_fixed', color='bought_name', marginal_y = 'violin'), use_container_width=True)
            with laceholder6:
                st.plotly_chart(px.scatter(df, x='timestamp', y='tokens_sold_fixed', color='sold_name', marginal_y = 'violin'), use_container_width=True)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
while True:
    loop.run_until_complete(get_event_arbi_tricryp())


