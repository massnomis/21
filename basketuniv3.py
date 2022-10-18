from cProfile import label
import json
import asyncio
from unicodedata import decimal
from numpy import place
from concurrent.futures import ProcessPoolExecutor

import streamlit as st
from web3 import Web3
import plotly.express as px
from websockets import connect
from eth_abi import decode_single, decode_abi
import math
import requests
from websockets import connect
import math
from datetime import datetime
import pandas as pd


st.set_page_config(layout="wide")   

                                                                                                                                  #  0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45
api = 'https://node-api.flipsidecrypto.com/api/v2/queries/f7a3fd01-4651-4898-846e-f01109f7265c/data/latest'
labels = pd.read_json(api,
convert_dates=["TIMESTAMP_NTZ"],
)
labels = labels.set_index('ADDRESS')

# st.write(labels)


# session = requests.Session()
# w3 = Web3(Web3.WebsocketProvider("wss://mainnet.infura.io/ws/v3/43b2d6f15d164cb4bbe4d4789831f242"))
df_main_tri = pd.DataFrame(columns=['sold_id', 'tokens_sold','sold_name','sold_decimal','tokens_bought','bought_name','bought_decimal','bought_id','timestamp'])
false = False
placeholder1 = st.empty()
placeholder2 = st.empty()
placeholder3 = st.empty()
placeholder4 = st.empty()
placeholder5 = st.empty()
placeholder6 = st.empty()

placeholder000 = st.empty()

placeholder100 = st.empty()
placeholder200 = st.empty()
placeholder300 = st.empty()
placeholder400 = st.empty()
placeholder500 = st.empty()
placeholder600 = st.empty()
placeholder700 = st.empty()
placeholder800 = st.empty()
placeholder900 = st.empty()
placeholder1000 = st.empty()
placeholder1100 = st.empty()
placeholder1200 = st.empty()

df_main_uni = pd.DataFrame(columns=['price', 'timestamp','WETH','USDC', 'side'])
false = False
placeholder00 = st.empty()
placeholder01 = st.empty()
placeholder02 = st.empty()
placeholder03 = st.empty()
placeholder04 = st.empty()
placeholder05 = st.empty()
placeholder06 = st.empty()
placeholder07 = st.empty()
placeholder08 = st.empty()
placeholder09 = st.empty()
placeholder010 = st.empty()
placeholder011 = st.empty()
placeholder012 = st.empty()





df_arbi = pd.DataFrame(columns=['sold_id', 'tokens_sold','sold_name','sold_decimal','tokens_bought','bought_name','bought_decimal','bought_id','timestamp'])
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
laceholder17 = st.empty()
laceholder18 = st.empty()
laceholder19 = st.empty()


def get_event_op_uni(message):
    lord_jesus = json.loads(message)
    lord_jesus = json.dumps(lord_jesus)
    lord_jesus = json.loads(lord_jesus)
    # with placeholder1:
    #     st.write(lord_jesus, use_container_width=True)
    now = datetime.now()
    lord_jesus = lord_jesus["params"]["result"]
    fromm = lord_jesus["topics"][1]
    fromm = decode_single('address', bytes.fromhex(fromm[2:]))
    fromm = str(fromm)
    too = lord_jesus["topics"][2]
    too = decode_single('address', bytes.fromhex(too[2:]))
    too = str(too)

    number = lord_jesus["data"][2:]

    number = decode_single('(int256,int256,uint160,uint128,int24)',bytearray.fromhex(number))
    # with placeholder2:
    #     st.write(number, use_container_width=True)
    liq = number[3]
    # liq = str(liq)
    tick = number[4]
    # tick = str(tick)
    prinnt = (number[0]*math.pow(10,12)* -1)/number[1]

    if number[0] > 0:
        side = "BUY"
    else:
        side = "SELL"
    usdc = abs(number[0]/math.pow(10,6))
    usdc_net = (number[0]/math.pow(10,6))
    weth = abs(number[1]/math.pow(10,18))
    try:
        labelz_fromm = labels.loc[fromm]["label"]
    except:
        labelz_fromm = fromm
    try:
        labelz_too = labels.loc[too]["label"]
    except:
        labelz_too = too
    d = {'too': too, 'fromm':fromm, 'price': prinnt, 'timestamp': now, 'WETH': weth, 'USDC': usdc, 'side': side, 'USDC_net': usdc_net, 'labelz_fromm': labelz_fromm, 'labelz_too': labelz_too}   
    fixed_df = pd.DataFrame(d, index=[0])
    df = df.append(fixed_df, ignore_index=True)
    df['cumsum'] = df['USDC_net'].cumsum()
    df['price_impact'] = df['price'].diff(periods=1)
    df['price_impact_w_size'] = df['price_impact']/df['USDC']
    df['taken_liquidity'] = df['Liq'].diff(periods=1)
    df['current_price'] = 1/(((((1.0001) ** (df['Tick'])))/math.pow(10,12)))
    df['price_deviation'] = (df['current_price'] - df['price'])
    df['price_deviation_w_size'] = df['price_deviation']/df['USDC']
    df['tick_change'] = df['Tick'].diff(periods=1)
    return df
async def get_event_mainnet_uni():
    global df_main_uni
    global labels

    async with connect("wss://mainnet.infura.io/ws/v3/43b2d6f15d164cb4bbe4d4789831f242") as ws:
        global df_main_uni
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
        while True:
            message = await asyncio.wait_for(ws.recv(), timeout=60000)
            lord_jesus = json.loads(message)
            lord_jesus = json.dumps(lord_jesus)
            lord_jesus = json.loads(lord_jesus)
            now = datetime.now()
            lord_jesus = lord_jesus["params"]["result"]
            fromm = lord_jesus["topics"][1]
            fromm = decode_single('address', bytes.fromhex(fromm[2:]))
            fromm = str(fromm)
            too = lord_jesus["topics"][2]
            too = decode_single('address', bytes.fromhex(too[2:]))
            too = str(too)
            number = lord_jesus["data"][2:]
            number = decode_single('(int256,int256,uint160,uint128,int24)',bytearray.fromhex(number))
            price_swap = number[0]/number[1]*math.pow(10,12)*-1
            if number[0] > 0:
                side = "BUY"
            else:
                side = "SELL"
            usdc = abs(number[0]/math.pow(10,6))
            usdc_net = (number[0]/math.pow(10,6))
            weth = abs(number[1]/math.pow(10,18))
            d = {'too': too, 'fromm':fromm, 'price': price_swap, 'timestamp': now, 'WETH': weth, 'USDC': usdc, 'side': side, 'USDC_net': usdc_net}
            fixed_df = pd.DataFrame(d, index=[0])
            df_main_uni = df_main_uni.append(fixed_df, ignore_index=True)
            df_main_uni['cumsum'] = df_main_uni['USDC_net'].cumsum()
            df_main_uni['price_impact'] = df_main_uni['price'].diff(periods=1)
            df_main_uni['price_impact_w_size'] = df_main_uni['price_impact']/df_main_uni['USDC']
            with placeholder02:
                st.write(df_main_uni, use_container_width=True)
            with placeholder04:
                st.plotly_chart(px.scatter(df_main_uni, x="timestamp", y="price", size="USDC", color='side',color_discrete_sequence=["green", "red"],title='main'), use_container_width=True)
            df1 = df_main_uni.copy()
            return df1
    #         return df_main_uni
    #     return df_main_uni
    # return df_main_uni

session = requests.Session()
w3 = Web3(Web3.WebsocketProvider("wss://mainnet.infura.io/ws/v3/43b2d6f15d164cb4bbe4d4789831f242"))
df_op_uni = pd.DataFrame(columns=['price', 'timestamp','WETH','USDC', 'side'])
false = False

async def get_event_op_uni():
    global df_op_uni
    global labels
    async with connect("wss://ws-mainnet.optimism.io") as ws:
        global df_op_uni
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
        # with placeholder000:
        #     st.write(subscription_response, use_container_width=True)
        while True:
            global labels
            message = await asyncio.wait_for(ws.recv(), timeout=60000)
            lord_jesus = json.loads(message)
            lord_jesus = json.dumps(lord_jesus)
            lord_jesus = json.loads(lord_jesus)
            # with placeholder1:
            #     st.write(lord_jesus, use_container_width=True)
            now = datetime.now()
            lord_jesus = lord_jesus["params"]["result"]
            fromm = lord_jesus["topics"][1]
            fromm = decode_single('address', bytes.fromhex(fromm[2:]))
            fromm = str(fromm)
            too = lord_jesus["topics"][2]
            too = decode_single('address', bytes.fromhex(too[2:]))
            too = str(too)

            number = lord_jesus["data"][2:]

            number = decode_single('(int256,int256,uint160,uint128,int24)',bytearray.fromhex(number))
            price_swap = (number[1]*math.pow(10,12)* -1)/number[0]

            if number[0] > 0:
                side = "sell"
            else:
                side = "buy"
            usdc = abs(number[1]/math.pow(10,6))
            usdc_net = (number[1]/math.pow(10,6))
            weth = abs(number[0]/math.pow(10,18))
            try:
                labelz_fromm = labels.loc[fromm]["label"]
            except:
                labelz_fromm = 'n/a'
            try:
                labelz_too = labels.loc[too]["label"]
            except:
                labelz_too = 'n/a'
            d = {'too': too, 'fromm':fromm, 'price': price_swap, 'timestamp': now, 'WETH': weth, 'USDC': usdc, 'side': side, 'USDC_net': usdc_net, 'labelz_fromm': labelz_fromm, 'labelz_too': labelz_too}
            fixed_df = pd.DataFrame(d, index=[0])
            df_op_uni = df_op_uni.append(fixed_df, ignore_index=True)
            df_op_uni['cumsum'] = df_op_uni['USDC_net'].cumsum()
            df_op_uni['price_impact'] = df_op_uni['price'].diff(periods=1)
            df_op_uni['price_impact_w_size'] = df_op_uni['price_impact']/df_op_uni['USDC']
            # df_op_uni['labelz_fromm'] = 'n/a'
            # df_op_uni['labelz_fromm'] = labels.loc[fromm]["label"]

            # '''make a new collum in df_op_uni called 'labelz_fromm' and 'labelz_too' and fill it with the fromm and too address we do this by matching the too and fromm address with the labels in the labels list and then'''
            # '''if the label is null, write n/a'''
            # def leblfrom():
            # for i in range(len(df_op_uni)):
            #     try:
            #         df_op_uni['labelz_fromm'] = labels.loc[fromm]["label"]
            #     except:
            #         df_op_uni['labelz_fromm'] = 'n/a'
            # # leblfrom()
            # df_op_uni['labelz_too'] = df_op_uni['too'].apply(lambda x: labels[x] if x in labels else 'n/a')

            # df_op_uni['labelz_fromm'] = df_op_uni['fromm'].map(labels)
            # df_op_uni['labelz_too'] = df_op_uni['too'].map(labels)
            # df_op_uni['labelz_fromm_too'] = df_op_uni['labelz_fromm'] + df_op_uni['labelz_too']





            # df_op_uni['labelz_from'] = label.loc['address']["too"]


            with placeholder400:
         
                st.write(df_op_uni, use_container_width=True)


            with placeholder600:
                st.plotly_chart(px.scatter(df_op_uni, x="timestamp", y="price", size="USDC", color='side',color_discrete_sequence=["green", "red"],title='op'), use_container_width=True)
            df2 = df_op_uni.copy()
            return df2
# wss://polygon-mainnet.g.alchemy.com/v2/uKtRRMD3RVeY5JrQXLzUbyUF05VeHzcP
session = requests.Session()
w3 = Web3(Web3.WebsocketProvider("wss://polygon-mainnet.g.alchemy.com/v2/uKtRRMD3RVeY5JrQXLzUbyUF05VeHzcP"))
df = pd.DataFrame(columns=['price', 'timestamp','WETH','USDC', 'side'])
false = False
placeholder0 = st.empty()

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

async def polyuni():
    global df
    global labels

    async with connect("wss://polygon-mainnet.g.alchemy.com/v2/uKtRRMD3RVeY5JrQXLzUbyUF05VeHzcP") as ws:
        global df
        await ws.send(json.dumps(
        {"id": 1, "method": "eth_subscribe", "params": 
        ["logs", 
       
  {
    "address": "0x45dda9cb7c25131df268515131f647d726f50608",
    "topics": [
      "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67"
    ]
  }
        ]
        }
        )
        )
        subscription_response = await ws.recv()
        # with placeholder0:
        #     st.json(subscription_response)
        while True:
            message = await asyncio.wait_for(ws.recv(), timeout=60000)
            lord_jesus = json.loads(message)
            lord_jesus = json.dumps(lord_jesus)
            lord_jesus = json.loads(lord_jesus)
            # with placeholder1:
            #     st.write(lord_jesus, use_container_width=True)
            now = datetime.now()
            lord_jesus = lord_jesus["params"]["result"]
            fromm = lord_jesus["topics"][1]
            fromm = decode_single('address', bytes.fromhex(fromm[2:]))
            fromm = str(fromm)
            too = lord_jesus["topics"][2]
            too = decode_single('address', bytes.fromhex(too[2:]))
            too = str(too)

            number = lord_jesus["data"][2:]

            number = decode_single('(int256,int256,uint160,uint128,int24)',bytearray.fromhex(number))
            # with placeholder2:
            #     st.write(number, use_container_width=True)
            Liq = number[3]
            # liq = str(liq)
            tick = number[4]
            # tick = str(tick)
            prinnt = (number[0]*math.pow(10,12)* -1)/number[1]

            if number[0] > 0:
                side = "BUY"
            else:
                side = "SELL"
            usdc = abs(number[0]/math.pow(10,6))
            usdc_net = (number[0]/math.pow(10,6))
            weth = abs(number[1]/math.pow(10,18))
            try:
                labelz_fromm = labels.loc[fromm]["label"]
            except:
                labelz_fromm = 'n/a'
            try:
                labelz_too = labels.loc[too]["label"]
            except:
                labelz_too = 'n/a'
            d = {'too': too, 'fromm':fromm, 'price': prinnt, 'timestamp': now, 'WETH': weth, 'USDC': usdc, 'side': side, 'USDC_net': usdc_net, 'labelz_fromm': labelz_fromm, 'labelz_too': labelz_too}
            fixed_df = pd.DataFrame(d, index=[0])
            df = df.append(fixed_df, ignore_index=True)
            df['cumsum'] = df['USDC_net'].cumsum()
            df['price_impact'] = df['price'].diff(periods=1)
            df['price_impact_w_size'] = df['price_impact']/df['USDC']
            # df['taken_liquidity'] = df['Liq'].diff(periods=1)
            # df['current_price'] = 1/(((((1.0001) ** (df['Tick'])))/math.pow(10,12)))
            # df['price_deviation'] = (df['current_price'] - df['price'])
            # df['price_deviation_w_size'] = df['price_deviation']/df['USDC']
            # df['tick_change'] = df['Tick'].diff(periods=1)
            with placeholder3:
                st.write(df, use_container_width=True)
            # with placeholder3:
            #     st.plotly_chart(px.line(df, x="timestamp", y="price", color="side"), use_container_width=True)

            with placeholder4:
                st.plotly_chart(px.scatter(df, x="timestamp", y="price", size="USDC", color='side',color_discrete_sequence=["green", "red"],title='poly'), use_container_width=True)
            # with placeholder5:
            #     st.plotly_chart(px.scatter(df, x="timestamp", y="current_price", color = 'price_deviation') , use_container_width=True)
            df3 = df.copy()
            return df3
    #     return df3
    # return df3



async def main():
    # Schedule three calls *concurrently*:
        await asyncio.gather(
        
        get_event_op_uni(),
        get_event_mainnet_uni(),
        polyuni(),
    
    )

asyncio.run(main())          

