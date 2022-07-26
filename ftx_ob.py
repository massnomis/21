import asyncio
import websockets
import json
from datetime import datetime
import streamlit as st
import time
import plotly.express as px
import pandas as pd
from itertools import accumulate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# st.set_page_config(layout="wide")

# import plotly.express as px

# df = pd.DataFrame(columns = ['id', 'price', 'size', 'side', 'liquidation', 'time'])
# placeholder1 = st.empty()
# for seconds in range(200):
# while True: 

import ccxt
import streamlit as st
import pandas as pd
from itertools import accumulate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import chain
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import math
st.set_page_config(layout="wide")
exchange = ccxt.ftx({
    'apiKey': '6lPPRFX1r4x_6ENY6GnhgYr3AdPv34x8Bc-MRH_V',
    'secret': 'OnQqs_nox4NS2OYm5z8ulXJ9rMkbOo5_nNwGe53V',
})
# if 'test' in exchange.urls:
#     exchange.urls['api'] = exchange.urls['test'] # ←----- switch the base URL to testnet
# # st.write(exchange.fetchOpenOrders())

placeholder = st.empty()
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
placeholder13 = st.empty()
placeholder14 = st.empty()
placeholder15 = st.empty()
# orders_hist = exchange.fetchOpenOrders()
# st.write(orders_hist)


orders_to_place_a_side_bid = st.number_input('Orders to place bid',0,10, value= 4)
orders_to_place_a_side_ask = st.number_input('Orders to place ask',0,10,value= 4)

stink_save_bid_drawdown = st.number_input('Bid drawdown',0.5,1.0,value= 0.8)
stink_save_ask_drawup = st.number_input('Ask drawup',1.0,2.0,value= 1.2)
# perp = st.checkbox('Perp', value= False)
#  1.05



        # st.write(order_cancel_df)




a = "Subscribed to orderbook"

b = "fat d8ta"

dict_dumps = {
  "op": "subscribe",
  "channel": "orderbook",
  "market": "BTC-PERP"
}
# market_name = st.text_input('Market name', value='BTC-PERP')
# name = st.text_input("market name", "BTC/USD")
# dict_dumps["market"] = market_name

placeholder1 = st.empty()


async def consumer() -> None:
    async with websockets.connect("wss://ftx.com/ws/", ping_interval=20, ping_timeout=2000) as websocket:
        await websocket.send(
            json.dumps(
                dict_dumps
            )
        )
        async for message in websocket:
            global a
            global b
            global name
            global orders_to_place_a_side_bid
            global orders_to_place_a_side_ask
            global stink_save_bid_drawdown
            global stink_save_ask_drawup

            message = json.loads(message)
            with placeholder1.container():

                if message["type"] == "subscribed":
                    st.write(a, use_container_width=True)

                if message["type"] == "partial":
                    market = message["market"]
                    type = message["type"]
                    channel = message["channel"]
                    data = message["data"]
                    time  = data["time"]
                    checksum = data["checksum"]
                    bids = data["bids"]
                    bids = pd.DataFrame(bids)
                    bids = bids.rename(columns={0: "price_bid", 1: "size_bid"})

                    asks = data["asks"]
                    asks = pd.DataFrame(asks)
                    asks.reset_index(drop=True, inplace=False)
                    bids.reset_index(drop = True, inplace=False)

                    asks = asks.rename(columns={0: "price_ask", 1: "size_ask"})
                    action = data["action"]
                    # st.write('2', bids, asks, action)

                    # return bids, asks, action, time, checksum
                if message["type"] == "update":
                    # global asks
                    # global bids
                    st.write(b, use_container_width=True)
                    type_update = message["type"]
                    channel_update = message["channel"]
                    data_update = message["data"]
                    time_update  = data_update["time"]
                    checksum = data_update["checksum"]
                    bids_update = pd.DataFrame(data_update["bids"])
                    bids_update = bids_update.rename(columns={0: "price_bid", 1: "size_bid"})
                    asks_update = pd.DataFrame(data_update["asks"])
                    asks_update = asks_update.rename(columns={0: "price_ask", 1: "size_ask"})
  
                    action = data_update["action"]
                    # st.write(asks)
                    # asks_update['accumulated']  = (list(accumulate(asks_update['size_ask'])))
                    # asks_update['accumulated_price']  = (asks_update['price_ask']) * asks_update['size_ask']
                    # asks_update['accumulated_avg_price'] = (list(accumulate(asks_update['accumulated_price'])))  / asks_update['accumulated']
                    # asks_update['cash_equivelant'] = asks_update['accumulated'] * asks_update['accumulated_avg_price']

                    # bids_update['accumulated']  = (list(accumulate(bids_update['size_bid'])))
                    # bids_update['accumulated_price']  = (bids_update['price_bid']) *bids_update['size_bid']
                    # bids_update['accumulated_avg_price'] = (list(accumulate(bids_update['accumulated_price'])))  / bids_update['accumulated']
                    # bids_update['cash_equivelant'] = bids_update['accumulated'] * bids_update['accumulated_avg_price']


                    # asks.reset_index(drop = True, inplace=True)
                    # bids.reset_index(drop = True, inplace=True)


                    for i in range(len(asks_update)):
                        # global asks_update
                        # if asks_update['price_ask'][i] == bids_update['price_bid'][i]:
                            # global bids_update
                        # asks.append(asks_update.loc[i])

                        # asks.reset_index(drop = True, inplace=True)
                        # asks.dropna(inplace=True)
                        asks.loc[asks["price_ask"] == asks_update.loc[i]["price_ask"], "size_ask"] = asks_update.loc[i]["size_ask"]
                        asks.dropna(inplace=True)

                        asks = asks.append(asks_update, ignore_index=True)
                        asks = asks.drop_duplicates(subset=['price_ask'], keep='first')
                        asks.sort_values(by=['price_ask'], inplace=True)
                        asks.reset_index(drop = True, inplace=False)

                        asks.loc[asks["price_ask"] == asks_update.loc[i]["price_ask"], "size_ask"] = asks_update.loc[i]["size_ask"]
                    for i in range(len(bids_update)):
                        # global bids_update
                        # if bids_update['price_bid'][i] == asks_update['price_ask'][i]:
                            # global asks_update
                        # bids.reset_index(drop = True, inplace=True)

                        # bids.dropna(inplace=True)
                        bids.reset_index(drop=True)

                        # bids.append(bids_update.loc[i])
                        bids.loc[bids["price_bid"] == bids_update.loc[i]["price_bid"], "size_bid"] = bids_update.loc[i]["size_bid"]
                        bids.dropna(inplace=True)
                        bids = bids.append(bids_update, ignore_index=True)
                        bids = bids.drop_duplicates(subset=['price_bid'], keep='first')
                        bids.sort_values(by=['price_bid'], inplace=True, ascending=False)
                        bids.reset_index(drop=True, inplace=False)
                        bids.loc[bids["price_bid"] == bids_update.loc[i]["price_bid"], "size_bid"] = bids_update.loc[i]["size_bid"]














    
                    asks = pd.DataFrame(asks)
                    bids = pd.DataFrame(bids)
                    # st.write(asks_update)
                    # st.write(bids_update)
                    asks['accumulated']  = (list(accumulate(asks['size_ask'])))
                    asks['accumulated_price']  = (asks['price_ask']) * asks['size_ask']
                    asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
                    asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']

                    bids['accumulated']  = (list(accumulate(bids['size_bid'])))
                    bids['accumulated_price']  = (bids['price_bid']) * bids['size_bid']
                    bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
                    bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']                
                    for i in range(1, 2):
                        cols = st.columns(2)
                        cols[0].subheader("bids")

                        cols[0].write(bids)
                        cols[1].subheader("asks")

                        cols[1].write(asks)
                    # st.write(asks,bids, use_container_width=True)
                    # st.write(asks_update,bids_update, use_container_width=True)
                    
                    # while True:




                    # load_makets_for_data = load_makets_for_data[load_makets_for_data.active != 'False']

                    # st.write(load_makets_for_data)

                    # if perp:
                    #     symbol = name + ":USD"
                    # else :
                    #     symbol = name

                    symbol = "BTC/USD:USD"
                    precision_load = pd.DataFrame(exchange.load_markets())
                    # st.write(precision_load.astype(str))
                    precision = (precision_load[symbol]['precision'])
                    # st.write(precision)
                    precision_amount = precision['amount']
                    precision_price = precision['price']
                














                    def ordering():
                        orders_hist = exchange.fetchOpenOrders()
                        orders_hist = pd.DataFrame(orders_hist)
                        with placeholder:
                            if orders_hist.empty:
                                st.write('no open orders')
                            else:
                                orders_hist = orders_hist[orders_hist.status != 'canceled']
                                orders_hist = orders_hist[orders_hist.status != 'closed']
                                # st.write(orders_hist)
                                if len(orders_hist) > ((orders_to_place_a_side_bid + orders_to_place_a_side_ask)/2) * 3:
                                    cancelAllOrders = exchange.cancelAllOrders()
                                # st.write(cancelAllOrders)
                                # for index, row in id.iterrows():
                                #     order_cancel = exchange.cancelOrder(id=row['id'])
                                #     order_cancel_df = order_cancel_df.append(order_cancel, ignore_index=True).astype(str)
                                    st.write("canceled, yalla")
                                else:
                                    st.write("no orders to cancel")


                        i = 0



                        bid_new = pd.DataFrame(bids)
                        bid_new['mm_bid_price']  = bids['price_bid'].max() + precision_price
                        bid_new['mm_bid_size'] = precision_amount
                        bid_new = bid_new.drop(columns=['accumulated', 'accumulated_price', 'accumulated_avg_price','cash_equivelant','price_bid'])
                        # st.write(bid_new)
                        stink_save_bid = bid_new['mm_bid_price'].max()*stink_save_bid_drawdown
                        bid_new = bid_new[bid_new.mm_bid_price > stink_save_bid]
                        # st.write(bid_new)

                        order_df_bid = pd.DataFrame()

                        # with placeholder3:
                        #     st.write(np.random.randint(5))
                        for col_name, data in bid_new.iterrows():
                            while i < orders_to_place_a_side_bid:

                                mm_bid_price = (data['mm_bid_price']) - (precision_price)
                                mm_bid_size = (data['mm_bid_size']) 
                                order_init_bid = exchange.createLimitBuyOrder(symbol=symbol,price=mm_bid_price,amount=mm_bid_size)
                                order_df_bid = order_df_bid.append(order_init_bid, ignore_index=True)
                                i += 1
                            i += 1
                        i += 1

                        order_df_bid = order_df_bid[['price','remaining']]
                        # st.write(order_df_bid)
                        order_df_bid = order_df_bid.sort_values(by=['price'], inplace=False, ascending=False)

                        order_df_bid = order_df_bid.reset_index()

                        order_df_bid['mm_bid_size'] = order_df_bid['remaining']/precision_amount
                        order_df_bid['accumulated']  = (list(accumulate(order_df_bid['mm_bid_size'])))
                        order_df_bid['accumulated_price']  = (order_df_bid['price']) * order_df_bid['mm_bid_size']
                        order_df_bid['accumulated_avg_price'] = (list(accumulate(order_df_bid['accumulated_price'])))  / order_df_bid['accumulated']
                        order_df_bid['cash_equivelant'] = order_df_bid['accumulated'] * order_df_bid['accumulated_avg_price']      








                        mid_ish = ((asks['price_ask'].min() + bids['price_bid'].max())) / 2
                        steps = round(mid_ish/precision_price)
                        # with placeholder5:
                        #     st.write("mid_ish", mid_ish, "steps", steps)








                        ask_new = pd.DataFrame(asks)
                        ask_new['mm_ask_price']  = asks['price_ask'].min() - precision_price
                        # + 400
                        ask_new['mm_ask_size'] = precision_amount
                        ask_new = ask_new.drop(columns=['accumulated', 'accumulated_price', 'accumulated_avg_price','cash_equivelant','price_ask'])
                        # st.write(ask_new)
                        stink_save_ask = ask_new['mm_ask_price'].min()*stink_save_ask_drawup
                        # st.write(stink_save_ask)
                        ask_new = ask_new[ask_new.mm_ask_price < stink_save_ask]
                        # st.write(ask_new)


                        order_df_ask = pd.DataFrame()

                        ref_ask = asks['price_ask'].min() - precision_price
                        ref_ask_size = precision_amount


                        ii = 0


                        for col_name, data in ask_new.iterrows():
                            while ii < orders_to_place_a_side_ask:

                                mm_ask_price = (data['mm_ask_price']) + (precision_price)
                                mm_ask_size = (data['mm_ask_size']) 
                                order_init_ask = exchange.createLimitSellOrder(symbol=symbol,price=mm_ask_price,amount=mm_ask_size)
                                order_df_ask = order_df_ask.append(order_init_ask, ignore_index=True)
                                ii += 1
                            ii += 1
                        ii += 1
                        # st.write(order_df_ask)
                        order_df_ask = order_df_ask[['price','remaining']]
                        # st.write(order_df_ask)
                        order_df_ask = order_df_ask.sort_values(by=['price'], inplace=False)

                        order_df_ask = order_df_ask.reset_index()

                        order_df_ask['mm_ask_size'] = order_df_ask['remaining']/precision_amount
                        order_df_ask['accumulated']  = (list(accumulate(order_df_ask['mm_ask_size'])))
                        order_df_ask['accumulated_price']  = (order_df_ask['price']) * order_df_ask['mm_ask_size']
                        order_df_ask['accumulated_avg_price'] = (list(accumulate(order_df_ask['accumulated_price'])))  / order_df_ask['accumulated']
                        order_df_ask['cash_equivelant'] = order_df_ask['accumulated'] * order_df_ask['accumulated_avg_price'] 

                    ordering()



















        


            
asyncio.run(consumer())