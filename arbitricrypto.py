# wss://arb-mainnet.g.alchemy.com/v2/0Yoq6lRIOyxmtUc399eoo3__isBlLIt6
import asyncio
import json
from unicodedata import decimal
from numpy import place
import streamlit as st
from web3 import Web3
import plotly.express as px
# from web3.middleware import geth_poa_middleware # only needed for PoA networks like BSC
import requests
from websockets import connect
from eth_abi import decode_single, decode_abi
import math
from datetime import datetime
import pandas as pd


# adapter = requests.sessions.HTTPAdapter(pool_connections=50000, pool_maxsize=50000) # pool connections and max size are for HTTP calls only, since we are using WS they are not needed. 
session = requests.Session()
w3 = Web3(Web3.WebsocketProvider("wss://arb-mainnet.g.alchemy.com/v2/0Yoq6lRIOyxmtUc399eoo3__isBlLIt6"))
# w3.middleware_onion.inject(geth_poa_middleware, layer=0) # only needed for PoA networks like BSC
df = pd.DataFrame(columns=['sold_id', 'tokens_sold','tokens_bought','bought_id','timestamp'])
tokens_list = {'USDT':0, 'WBTC':1, "WETH":2 }
decimal_list = {'USDT':6, 'WBTC':8, "WETH":18 }
false = False

placeholder1 = st.empty()
placeholder2 = st.empty()
placeholder3 = st.empty()
placeholder4 = st.empty()
placeholder5 = st.empty()
placeholder6 = st.empty()
async def get_event():
    global df

    # global df
# ?    global df
#    ?? global fixed_df
    async with connect("wss://arb-mainnet.g.alchemy.com/v2/0Yoq6lRIOyxmtUc399eoo3__isBlLIt6") as ws:
        global df
        # global fixed_df
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
        with placeholder1:
            st.write(subscription_response)
        while True:
            # global df
            # global fixed_df
            message = await asyncio.wait_for(ws.recv(), timeout=600)
            lord_jesus = json.loads(message)
            lord_jesus = json.dumps(lord_jesus)
            lord_jesus = json.loads(lord_jesus)
            st.write(lord_jesus)
            lord_jesus = lord_jesus["params"]["result"]
            number = lord_jesus["data"][2:]
            st.write(number)
            # addy1 = lord_jesus["topics"][1][2:]
            # addy2 = lord_jesus["topics"][2][2:]
            number = decode_single('(uint256,uint256,uint256,uint256)',bytearray.fromhex(number))
            st.write(list(number))

            now = datetime.now()
            # 'sold_id', 'tokens_sold','tokens_bought','bought_id','timestamp']
            d = {'sold_id': number[0], 'tokens_sold': number[1], 'bought_id':number[2], 'tokens_bought': number[3], 'timestamp': now}
            fixed_df = pd.DataFrame(d, index=[0])
            df = df.append(fixed_df, ignore_index=True)
            # df['cumsum'] = df['value'].cumsum()
            with placeholder2:
                st.write(df)
            # addy1 = decode_single('(address)',bytearray.fromhex(addy1))
            # addy2 = decode_single('(address)',bytearray.fromhex(addy2))
            # number = number[0]
            # number = number / math.pow(10,6)
            # addy1 = addy1[0]
            # addy2 = addy2[0]
            # # st.write(number)
            # # st.write(addy1)
            # # st.write(addy2)
            # now = datetime.now()
            # d = {'from': addy1, 'to': addy2, 'value': number, 'time': now}
            # fixed_df = pd.DataFrame(d, index=[0])
            # df = df.append(fixed_df, ignore_index=True)
            # df['cumsum'] = df['value'].cumsum()
            # bollinger_strat(df=df,window=10,no_of_std=2)
            # bollinger_strat2(df=df,window=10,no_of_std=2)

            # df['from'].append = addy1
            # df['to'].append = addy2
            # df['value'].append = number     
            # with placeholder2:
            #     # global df
            #     # df = df.append(([addy1,addy2,number]),ignore_index=True)
              
            # # df = df.append(([addy1,addy2,number]),ignore_index=True)  
            #     st.write(df,use_container_width=True)
            # with placeholder3:
            #     st.plotly_chart(px.bar(df, x='cumsum', y='value'),use_container_width=True)
            # with placeholder4:
            #     st.plotly_chart(px.scatter(df, x='cumsum', y='rolling_mean_value',marginal_y="violin", marginal_x="rug"),use_container_width=True)
            # with placeholder5:
            #     st.plotly_chart(px.line(df, x='time', y='rolling_mean_cumsum'),use_container_width=True)
            # with placeholder6:
            #     st.plotly_chart(px.scatter(df, x='time', y=['value','rolling_mean_value','Bollinger High','Bollinger Low'],marginal_y="violin", marginal_x="rug"),use_container_width=True)
            # with placeholder7:
            #     st.plotly_chart(px.scatter(df, x='time', y='cumsum', size='value',marginal_y="violin", marginal_x="rug"),use_container_width=True)
            # with placeholder8:
            #     st.plotly_chart(px.scatter(df, x='time', y=['Bollinger High_cumsum','Bollinger Low_cumsum','rolling_mean_cumsum','cumsum'], size = 'value',marginal_y="violin", marginal_x="rug"),use_container_width=True)
# if _name_ == "_main_":
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
while True:
    loop.run_until_complete(get_event())

# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)