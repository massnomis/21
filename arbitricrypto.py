import asyncio
import json
from pydoc_data.topics import topics
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
laceholder0 = st.empty()
laceholder1 = st.empty()
laceholder2 = st.empty()
laceholder3 = st.empty()
laceholder4 = st.empty()
laceholder5 = st.empty()
laceholder6 = st.empty()
laceholder7 = st.empty()
laceholder8 = st.empty()
laceholder9 = st.empty()
laceholder10 = st.empty()
laceholder11 = st.empty()
laceholder12 = st.empty()
laceholder13 = st.empty()
laceholder14 = st.empty()
laceholder15 = st.empty()
laceholder16 = st.empty()

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
        with laceholder0:
            st.write(subscription_response)
        while True:
            global df_arbi
            message = await asyncio.wait_for(ws.recv(), timeout=600)
            # with laceholder1:
            #     st.json(message)
            lord_jesus = json.loads(message)
            lord_jesus = json.dumps(lord_jesus)
            lord_jesus = json.loads(lord_jesus)
            lord_jesus = lord_jesus["params"]["result"]
            fromm = lord_jesus['topics'][1]
            fromm = decode_single('(address)', bytearray.fromhex(fromm[2:]))
            number = lord_jesus["data"][2:]
            number = decode_single('(uint256,uint256,uint256,uint256)',bytearray.fromhex(number))
            now = datetime.now()
            d = {'sold_id': number[0], 'tokens_sold': number[1], 'bought_id':number[2], 'tokens_bought': number[3], 'timestamp': now, 'from': fromm}
            fixed_df = pd.DataFrame(d, index=[0])
            if d['sold_id'] == 0:
                fixed_df['sold_name'] = 'USDT'
                fixed_df['sold_decimal'] = 6
                fixed_df['tokens_sold'] = fixed_df['tokens_sold'] / 10**6
            elif d['sold_id'] == 1:
                fixed_df['sold_name'] = 'WBTC'
                fixed_df['sold_decimal'] = 8
                fixed_df['tokens_sold'] = fixed_df['tokens_sold'] / 10**8
            elif d['sold_id'] == 2:
                fixed_df['sold_name'] = 'WETH'
                fixed_df['sold_decimal'] = 18
                fixed_df['tokens_sold'] = fixed_df['tokens_sold'] / 10**18
            if d['bought_id'] == 0:
                fixed_df['bought_name'] = 'USDT'
                fixed_df['bought_decimal'] = 6
                fixed_df['tokens_bought'] = fixed_df['tokens_bought'] / 10**6
            elif d['bought_id'] == 1:
                fixed_df['bought_name'] = 'WBTC'
                fixed_df['bought_decimal'] = 8
                fixed_df['tokens_bought'] = fixed_df['tokens_bought'] / 10**8
            elif d['bought_id'] == 2:
                fixed_df['bought_name'] = 'WETH'
                fixed_df['bought_decimal'] = 18
                fixed_df['tokens_bought'] = fixed_df['tokens_bought'] / 10**18
            df_arbi = df_arbi.append(fixed_df, ignore_index=True)
            df_arbi['rate_1_fixed'] = df_arbi['tokens_bought'] / df_arbi['tokens_sold']
            df_arbi['rate_2_fixed'] = df_arbi['tokens_sold'] / df_arbi['tokens_bought']
            df_arbi["max_rate_fixed"] = df_arbi[["rate_1_fixed", "rate_2_fixed"]].max(axis=1)
            df_arbi["min_rate_fixed"] = df_arbi[["rate_1_fixed", "rate_2_fixed"]].min(axis=1)
            df_arbi['max_bought_sold'] = df_arbi[["tokens_bought", "tokens_sold"]].max(axis=1)
            df_arbi['min_bought_sold'] = df_arbi[["tokens_bought", "tokens_sold"]].min(axis=1)
            df_arbi['path'] = df_arbi['sold_name'] + ' to ' + df_arbi['bought_name']
            df_usdt_weth = df_arbi[(df_arbi['sold_name'] == 'USDT') & (df_arbi['bought_name'] == 'WETH')]
            df_weth_wbtc = df_arbi[(df_arbi['sold_name'] == 'WETH') & (df_arbi['bought_name'] == 'WBTC')]
            df_usdt_weth = df_arbi[(df_arbi['sold_name'] == 'WETH') & (df_arbi['bought_name'] == 'USDT')]
            df_usdt_wbtc = df_arbi[(df_arbi['sold_name'] == 'WBTC') & (df_arbi['bought_name'] == 'USDT')]
            df_usdt_wbtc = df_arbi[(df_arbi['sold_name'] == 'USDT') & (df_arbi['bought_name'] == 'WBTC')]
            df_weth_wbtc = df_arbi[(df_arbi['sold_name'] == 'WBTC') & (df_arbi['bought_name'] == 'WETH')]
            with laceholder2:
                st.write(df_arbi,use_container_width=True)
            with laceholder6:
                st.plotly_chart(px.scatter(df_usdt_weth, x='timestamp', y='max_rate_fixed', color='bought_name', size = 'max_bought_sold', title='USDT-WETH',color_discrete_sequence=["green", "red"],), use_container_width=True)
            with laceholder7:
                st.plotly_chart(px.scatter(df_weth_wbtc, x='timestamp', y='max_rate_fixed', color='bought_name', size = 'max_bought_sold', title='WETH-WBTC',color_discrete_sequence=["green", "red"],), use_container_width=True)
            with laceholder8:
                st.plotly_chart(px.scatter(df_usdt_wbtc, x='timestamp', y='max_rate_fixed', color='bought_name', size = 'max_bought_sold', title='USDT-WBTC',color_discrete_sequence=["green", "red"],), use_container_width=True)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
while True:
    loop.run_until_complete(get_event_arbi_tricryp())


