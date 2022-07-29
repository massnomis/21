import json
import asyncio
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
st.set_page_config(page_title="usdcweth", page_icon="🔐", layout="wide")   
def bollinger_strat(df, window, no_of_std):
    rolling_mean = df['USDC'].rolling(window).mean()
    rolling_std = df['USDC'].rolling(window).std()
    df['rolling_mean_value'] = rolling_mean

    df['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
    df['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
    return df['Bollinger High'] , df['Bollinger Low'], df['rolling_mean_value'] 
def bollinger_strat2(df, window, no_of_std):
    rolling_mean = df['cumsum'].rolling(window).mean()
    rolling_std = df['cumsum'].rolling(window).std()
    df['rolling_mean_cumsum'] = rolling_mean

    df['Bollinger High_cumsum'] = rolling_mean + (rolling_std * no_of_std)
    df['Bollinger Low_cumsum'] = rolling_mean - (rolling_std * no_of_std)     
    return df['Bollinger High_cumsum'] , df['Bollinger Low_cumsum'], df['rolling_mean_cumsum'] 
session = requests.Session()
w3 = Web3(Web3.WebsocketProvider("wss://mainnet.infura.io/ws/v3/43b2d6f15d164cb4bbe4d4789831f242"))
df = pd.DataFrame(columns=['price', 'timestamp','WETH','USDC', 'side'])
false = False
placeholder1 = st.empty()
placeholder2 = st.empty()
placeholder3 = st.empty()
placeholder4 = st.empty()
placeholder5 = st.empty()
placeholder6 = st.empty()
placeholder7 = st.empty()
placeholder8 = st.empty()
placeholder9 = st.empty()
placeholder10 = st.empty()
placeholder11 = st.empty()
placeholder12 = st.empty()
async def get_event():
    global df
    async with connect("wss://mainnet.infura.io/ws/v3/43b2d6f15d164cb4bbe4d4789831f242") as ws:
        global df
        await ws.send(json.dumps(
        {"id": 1, "method": "eth_subscribe", "params": 
        ["logs", 
       
  {
    "address": "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",
    "topics": [
      "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67"
    ]
  }
        ]
        }
        )
        )
        subscription_response = await ws.recv()
        with placeholder1:
            st.write(subscription_response, use_container_width=True)
        while True:
            # global df
            # global tokens_list
            # global decimal_list
            message = await asyncio.wait_for(ws.recv(), timeout=60000)
            lord_jesus = json.loads(message)
            lord_jesus = json.dumps(lord_jesus)
            lord_jesus = json.loads(lord_jesus)
            # st.write(lord_jesus)
            now = datetime.now()
            lord_jesus = lord_jesus["params"]["result"]
            number = lord_jesus["data"][2:]
            # data = '00000000000000000000000000000000000000000000000000000012c7db4048fffffffffffffffffffffffffffffffffffffffffffffffd76fd5f054400e7a40000000000000000000000000000000000005e12c25ea154ac1ed76c593ce26e000000000000000000000000000000000000000000000000b5050eb63d7592380000000000000000000000000000000000000000000000000000000000031443'
            number = decode_single('(int256,int256,uint160,uint128,int24)',bytearray.fromhex(number))
            print = number[0]/number[1]*math.pow(10,12)*-1

            if number[0] > 0:
                side = "SELL"
            else:
                side = "BUY"



            usdc = abs(number[0]/math.pow(10,6))
            usdc_net = (number[0]/math.pow(10,6))
            weth = abs(number[1]/math.pow(10,18))
            d = {'price': print, 'timestamp': now, 'WETH': weth, 'USDC': usdc, 'side': side, 'USDC_net': usdc_net}
            fixed_df = pd.DataFrame(d, index=[0])
            df = df.append(fixed_df, ignore_index=True)
            df['cumsum'] = df['USDC_net'].cumsum()

            bollinger_strat(df=df,window=5,no_of_std=1)
            bollinger_strat2(df=df,window=5,no_of_std=1)
            with placeholder2:
                st.write(df, use_container_width=True)
            with placeholder3:
                st.plotly_chart(px.scatter(df, x="timestamp", y="price", size="USDC"), use_container_width=True)
            with placeholder4:
                st.plotly_chart(px.scatter(df, x="timestamp", y="price", size="USDC", color='side'), use_container_width=True)
            with placeholder5:
                st.plotly_chart(px.bar(df, x="timestamp", y="USDC", title="USDC") , use_container_width=True)
            with placeholder6:
                st.plotly_chart(px.scatter(df, x="WETH", y="price", size="USDC", color='WETH') , use_container_width=True)
            with placeholder7:
                st.plotly_chart(px.scatter(df, x='timestamp', y='cumsum', size='USDC',marginal_y="violin", marginal_x="rug"),use_container_width=True)
            with placeholder8:
                st.plotly_chart(px.scatter(df, x='timestamp', y=['Bollinger High_cumsum','Bollinger Low_cumsum','rolling_mean_cumsum','cumsum'], size = 'USDC',marginal_y="violin", marginal_x="rug"),use_container_width=True)
# if _name_ == "_main_":
            # wi
            # st.write(df)

            # with placeholder6:

            # st.write(df)
            # print(list(number))
            # number = decode_single('(uint256,uint256,uint256,uint256)',bytearray.fromhex(number))
            # now = datetime.now()
            # d = {'sold_id': number[0], 'tokens_sold': number[1], 'bought_id':number[2], 'tokens_bought': number[3], 'timestamp': now}
            # fixed_df = pd.DataFrame(d, index=[0])
            # if d['sold_id'] == 0:
            #     fixed_df['sold_name'] = 'USDT'
            #     fixed_df['sold_decimal'] = 6
            #     fixed_df['tokens_sold_fixed'] = fixed_df['tokens_sold'] / 10**6
            # elif d['sold_id'] == 1:
            #     fixed_df['sold_name'] = 'WBTC'
            #     fixed_df['sold_decimal'] = 8
            #     fixed_df['tokens_sold_fixed'] = fixed_df['tokens_sold'] / 10**8
            # elif d['sold_id'] == 2:
            #     fixed_df['sold_name'] = 'WETH'
            #     fixed_df['sold_decimal'] = 18
            #     fixed_df['tokens_sold_fixed'] = fixed_df['tokens_sold'] / 10**18
            # if d['bought_id'] == 0:
            #     fixed_df['bought_name'] = 'USDT'
            #     fixed_df['bought_decimal'] = 6
            #     fixed_df['tokens_bought_fixed'] = fixed_df['tokens_bought'] / 10**6
            # elif d['bought_id'] == 1:
            #     fixed_df['bought_name'] = 'WBTC'
            #     fixed_df['bought_decimal'] = 8
            #     fixed_df['tokens_bought_fixed'] = fixed_df['tokens_bought'] / 10**8
            # elif d['bought_id'] == 2:
            #     fixed_df['bought_name'] = 'WETH'
            #     fixed_df['bought_decimal'] = 18
            #     fixed_df['tokens_bought_fixed'] = fixed_df['tokens_bought'] / 10**18
            # df = df.append(fixed_df, ignore_index=True)
            # df['rate_1_fixed'] = df['tokens_bought_fixed'] / df['tokens_sold_fixed']
            # df['rate_2_fixed'] = df['tokens_sold_fixed'] / df['tokens_bought_fixed']
            # df['path'] = df['sold_name'] + ' to ' + df['bought_name']
            # with placeholder2:
            #     st.write(df,use_container_width=True)
            # with placeholder3:
            #     st.plotly_chart(px.line(df, x='timestamp', y='rate_1_fixed', color='path'))
            # with placeholder4:
            #     st.plotly_chart(px.line(df, x='timestamp', y='rate_2_fixed', color='path'))
            # with placeholder5:
            #     st.plotly_chart(px.bar(df, x='timestamp', y=['tokens_sold_fixed','tokens_bought_fixed'], color='path'))
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
while True:
    loop.run_until_complete(get_event())


