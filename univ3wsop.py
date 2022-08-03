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
    async with connect("wss://ws-mainnet.optimism.io") as ws:
        global df
        await ws.send(json.dumps(
        {"id": 1, "method": "eth_subscribe", "params": 
        ["logs", 
       
  {
    "address": "0x85149247691df622eaF1a8Bd0CaFd40BC45154a9",
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
            message = await asyncio.wait_for(ws.recv(), timeout=60000)
            lord_jesus = json.loads(message)
            lord_jesus = json.dumps(lord_jesus)
            lord_jesus = json.loads(lord_jesus)
            now = datetime.now()
            lord_jesus = lord_jesus["params"]["result"]
            number = lord_jesus["data"][2:]

            number = decode_single('(int256,int256,uint160,uint128,int24)',bytearray.fromhex(number))
            prinnt = (number[1]*math.pow(10,12)* -1)/number[0]

            if number[0] > 0:
                side = "Sell"
            else:
                side = "Buy"
            usdc = abs(number[1]/math.pow(10,6))
            usdc_net = (number[1]/math.pow(10,6))
            weth = abs(number[0]/math.pow(10,18))
            liq = number[3]
            tick = number[4]
            d = {'price': prinnt, 'timestamp': now, 'WETH': weth, 'USDC': usdc, 'side': side, 'USDC_net': usdc_net, 'tick': tick, 'liq': liq}
            fixed_df = pd.DataFrame(d, index=[0])
            df = df.append(fixed_df, ignore_index=True)
            df['cumsum'] = df['USDC_net'].cumsum()
            df['price_impact'] = df['price'].diff(periods=1)
            df['price_impact_w_size'] = df['price_impact']/df['USDC']
            df['taken_liquidity'] = df['liq'].diff(periods=1)
            df['current_price'] = 1/(1/(((1.0001) ** (df['tick'])))/math.pow(10,12))
            df['price_deviation'] = abs(df['current_price'] - df['price'])
            df['price_deviation_w_size'] = df['price_deviation']/df['USDC']
            df['tick_change'] = df['tick'].diff(periods=1)
            bollinger_strat(df=df,window=5,no_of_std=1)
            bollinger_strat2(df=df,window=5,no_of_std=1)
            with placeholder2:
                st.write(df, use_container_width=True)
            # with placeholder3:
            #     st.plotly_chart(px.line(df, x="timestamp", y="price", color="side"), use_container_width=True)

            with placeholder4:
                st.plotly_chart(px.scatter(df, x="timestamp", y="price", size="USDC", color='side'), use_container_width=True)
            with placeholder5:
                st.plotly_chart(px.bar(df, x="timestamp", y="USDC", title="USDC") , use_container_width=True)
            # with placeholder6:
            #     st.plotly_chart(px.scatter(df, x="WETH", y="price", size="USDC", color='WETH') , use_container_width=True)
            # with placeholder7:
            #     st.plotly_chart(px.scatter(df, x='timestamp', y='cumsum', size='USDC',marginal_y="violin", marginal_x="rug"),use_container_width=True)
            # with placeholder8:
            #     st.plotly_chart(px.scatter(df, x='timestamp', y=['Bollinger High_cumsum','Bollinger Low_cumsum','rolling_mean_cumsum','cumsum'], size = 'USDC',marginal_y="violin", marginal_x="rug"),use_container_width=True)
            # with placeholder9:
            #     st.plotly_chart(px.bar(df, x="timestamp", y="price"), use_container_width=True)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
while True:
    loop.run_until_complete(get_event())


