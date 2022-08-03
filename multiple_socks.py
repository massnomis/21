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



async def get_event_mainnet_tricrpto():
    global df_main_tri
    async with connect("wss://mainnet.infura.io/ws/v3/43b2d6f15d164cb4bbe4d4789831f242") as ws:
        global df_main_tri
        await ws.send(json.dumps(
        {"id": 1, "method": "eth_subscribe", "params": 
        ["logs", 
       
  {
    "address": "0xD51a44d3FaE010294C616388b506AcdA1bfAAE46",
    "topics": [
      "0xb2e76ae99761dc136e598d4a629bb347eccb9532a5f8bbd72e18467c3c34cc98"
    ]
  }
        ]
        }
        )
        )
        subscription_response = await ws.recv()
        # with placeholder1:
        #     st.write(subscription_response)
        while True:
            global df_main_tri

            message = await asyncio.wait_for(ws.recv(), timeout=60000)
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
            df_main_tri = df_main_tri.append(fixed_df, ignore_index=True)
            df_main_tri['rate_1_fixed'] = df_main_tri['tokens_bought'] / df_main_tri['tokens_sold']
            df_main_tri['rate_2_fixed'] = df_main_tri['tokens_sold'] / df_main_tri['tokens_bought']
            df_main_tri['path'] = df_main_tri['sold_name'] + ' to ' + df_main_tri['bought_name']
            # df_main_tri = json.loads(df_main_tri)
            # df_main_tri = json.dumps(df_main_tri)
            # df_main_tri = pd.DataFrame(df_main_tri)
            with placeholder2:
                st.write(df_main_tri, use_container_width=True)
            with placeholder3:
                st.plotly_chart(px.line(df_main_tri, x='timestamp', y='rate_1_fixed', color='path'), use_container_width=True)
            with placeholder4:
                st.plotly_chart(px.line(df_main_tri, x='timestamp', y='rate_2_fixed', color='path'), use_container_width=True)
            # with placeholder5:
            #     st.plotly_chart(px.bar(df_main_tri, x='timestamp', y=['tokens_sold','tokens_bought'], color='path'))






# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# while True:
#     loop.run_until_complete(get_event_mainnet_tricrpto())

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
# session = requests.Session()
# w3 = Web3(Web3.WebsocketProvider("wss://mainnet.infura.io/ws/v3/43b2d6f15d164cb4bbe4d4789831f242"))
async def get_event_mainnet_uni():
    global df_main_uni
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
        # with placeholder00:
        #     st.write(subscription_response, use_container_width=True)
        while True:
            # global df
            # global tokens_list
            # global decimal_list
            message = await asyncio.wait_for(ws.recv(), timeout=60000)
            lord_jesus = json.loads(message)
            lord_jesus = json.dumps(lord_jesus)
            lord_jesus = json.loads(lord_jesus)
            # with placeholder01:
            #     st.write(lord_jesus, use_container_width=True)
            # st.write(lord_jesus)
            now = datetime.now()
            lord_jesus = lord_jesus["params"]["result"]
            number = lord_jesus["data"][2:]
            # data = '00000000000000000000000000000000000000000000000000000012c7db4048fffffffffffffffffffffffffffffffffffffffffffffffd76fd5f054400e7a40000000000000000000000000000000000005e12c25ea154ac1ed76c593ce26e000000000000000000000000000000000000000000000000b5050eb63d7592380000000000000000000000000000000000000000000000000000000000031443'
            number = decode_single('(int256,int256,uint160,uint128,int24)',bytearray.fromhex(number))
            print = number[0]/number[1]*math.pow(10,12)*-1

            if number[0] > 0:
                side = "BUY"
            else:
                side = "SELL"



            usdc = abs(number[0]/math.pow(10,6))
            usdc_net = (number[0]/math.pow(10,6))
            weth = abs(number[1]/math.pow(10,18))
            d = {'price': print, 'timestamp': now, 'WETH': weth, 'USDC': usdc, 'side': side, 'USDC_net': usdc_net}
            fixed_df = pd.DataFrame(d, index=[0])
            df_main_uni = df_main_uni.append(fixed_df, ignore_index=True)
            df_main_uni['cumsum'] = df_main_uni['USDC_net'].cumsum()

            bollinger_strat(df=df_main_uni,window=5,no_of_std=1)
            bollinger_strat2(df=df_main_uni,window=5,no_of_std=1)
            with placeholder02:
                st.write(df_main_uni, use_container_width=True)
            with placeholder03:
                st.plotly_chart(px.line(df_main_uni, x="timestamp", y="price", color="side"), use_container_width=True)

            with placeholder04:
                st.plotly_chart(px.scatter(df_main_uni, x="timestamp", y="price", size="USDC", color='side'), use_container_width=True)
            # with placeholder05:
            #     st.plotly_chart(px.bar(df_main_uni, x="timestamp", y="USDC", title="USDC") , use_container_width=True)
            # with placeholder06:
            #     st.plotly_chart(px.scatter(df_main_uni, x="WETH", y="price", size="USDC", color='WETH') , use_container_width=True)
            # with placeholder07:
                # st.plotly_chart(px.scatter(df_main_uni, x='timestamp', y='cumsum', size='USDC',marginal_y="violin", marginal_x="rug"),use_container_width=True)
            # with placeholder08:
            #     st.plotly_chart(px.scatter(df_main_uni, x='timestamp', y=['Bollinger High_cumsum','Bollinger Low_cumsum','rolling_mean_cumsum','cumsum'], size = 'USDC',marginal_y="violin", marginal_x="rug"),use_container_width=True)
            # with placeholder09:
            #     st.plotly_chart(px.bar(df_main_uni, x="timestamp", y="price"), use_container_width=True)

# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# while True:
#     loop.run_until_complete(get_event_mainnet_uni())

 
session = requests.Session()
w3 = Web3(Web3.WebsocketProvider("wss://mainnet.infura.io/ws/v3/43b2d6f15d164cb4bbe4d4789831f242"))
df_op_uni = pd.DataFrame(columns=['price', 'timestamp','WETH','USDC', 'side'])
false = False
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
async def get_event_op_uni():
    global df_op_uni
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
            d = {'too': too, 'fromm':fromm, 'price': price_swap, 'timestamp': now, 'WETH': weth, 'USDC': usdc, 'side': side, 'USDC_net': usdc_net}
            fixed_df = pd.DataFrame(d, index=[0])
            df_op_uni = df_op_uni.append(fixed_df, ignore_index=True)
            df_op_uni['cumsum'] = df_op_uni['USDC_net'].cumsum()
            df_op_uni['price_impact'] = df_op_uni['price'].diff(periods=1)
            df_op_uni['price_impact_w_size'] = df_op_uni['price_impact']/df_op_uni['USDC']
            # df['taken_liquidity'] = df['liq'].diff(periods=1)
            # df['current_price'] = 1/(1/(((1.0001) ** (df['tick'])))/math.pow(10,12))
            # df['price_deviation'] = abs(df['current_price'] - df['price'])
            # df['price_deviation_w_size'] = df['price_deviation']/df['USDC']
            # df['tick_change'] = df['tick'].diff(periods=1)
            bollinger_strat(df=df_op_uni,window=5,no_of_std=1)
            bollinger_strat2(df=df_op_uni,window=5,no_of_std=1)

            with placeholder400:
         
                st.write(df_op_uni, use_container_width=True)
            # df_op_uni = df_op_uni.astype(str)
            # with placeholder700:
            #     st.write(df_op_uni, use_container_width=True)

            # df_op_uni = json.loads(df_op_uni)
            # df_op_uni = json.dumps(df_op_uni)
            # df_op_uni = json.loads(df_op_uni)
            # with placeholder800:
            #     st.write(df_op_uni, use_container_width=True)

            # df_op_uni = pd.DataFrame(df_op_uni)
            # with placeholder900:
            #     st.write(df_op_uni, use_container_width=True)

            # with placeholder200:
            #     st.write(df_op_uni, use_container_width=True)

            with placeholder600:
                st.plotly_chart(px.scatter(df_op_uni, x="timestamp", y="price", size="USDC", color='side'), use_container_width=True)

# session = requests.Session()
# w3 = Web3(Web3.WebsocketProvider("wss://arb-mainnet.g.alchemy.com/v2/0Yoq6lRIOyxmtUc399eoo3__isBlLIt6"))

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
        # with laceholder1:
        #     st.write(subscription_response)
        while True:
            global df_arbi
            # global tokens_list
            # global decimal_list
            message = await asyncio.wait_for(ws.recv(), timeout=60000)
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
            df_arbi['path'] = df_arbi['sold_name'] + ' to ' + df_arbi['bought_name']
            with laceholder2:
                st.write(df_arbi,use_container_width=True)
            with laceholder3:
                st.plotly_chart(px.line(df_arbi, x='timestamp', y='rate_1_fixed', color='path'), use_container_width=True)
            with laceholder4:
                st.plotly_chart(px.line(df_arbi, x='timestamp', y='rate_2_fixed', color='path'), use_container_width=True)
            # with laceholder5:
            #     st.plotly_chart(px.scatter(df_arbi, x='timestamp', y='tokens_bought', color='bought_name', marginal_y = 'violin'), use_container_width=True)
            # with laceholder6:
            #     st.plotly_chart(px.scatter(df_arbi, x='timestamp', y='tokens_sold', color='sold_name', marginal_y = 'violin'), use_container_width=True)

async def main():
    # Schedule three calls *concurrently*:
        await asyncio.gather(
        get_event_mainnet_tricrpto(),
        get_event_op_uni(),
        get_event_arbi_tricryp(),
        get_event_mainnet_uni(),

    )

asyncio.run(main())          

# asyncio.set_event_loop(loop)

# # if __name__ == "__main__":
# executor = ProcessPoolExecutor(4)
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# # while True:    
# if __name__ == '__main__':
    
#     op_uni = loop.run_in_executor(executor, get_event_op_uni)
#     main_tri = loop.run_in_executor(executor, get_event_mainnet_tricrpto)
#     main_uni = loop.run_in_executor(executor, get_event_mainnet_uni)
#     arbi_tri = loop.run_in_executor(executor, get_event_arbi_tricryp)
#     loop.run_until_complete(asyncio.gather(op_uni, main_tri, main_uni, arbi_tri))
