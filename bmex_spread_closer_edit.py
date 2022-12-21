from http.client import BAD_REQUEST
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
import werkzeug
import ccxt.base.errors
from werkzeug.exceptions import BadRequest
import requests.exceptions
st.set_page_config(layout="wide")

# st.write(exchange.fetchOpenOrders())
# Python




# YA4m6zHsg5oIDLf6Nt3RsLZV
# Q1WgI4sQCSL7onK_N-cZlybEbguToFpP-cSq-TljMYo4taLX



# add api key and secret

# YA4m6zHsg5oIDLf6Nt3RsLZV
# Q1WgI4sQCSL7onK_N-cZlybEbguToFpP-cSq-TljMYo4taLX
exchange = ccxt.bitmex({
    'apiKey' : 'h2r2C5YcbUfVHCIBCyKLyk0h ',
    'secret'  : '5mlXZrL3IQD5NtcttOsApZUOQUmuobjx9I6EZwNS1jRfMjjQ'





})
if 'test' in exchange.urls:
    exchange.urls['api'] = exchange.urls['test'] # ←----- switch the base URL to testnet
# st.write(exchange.fetchOpenOrders())




class BaseError (Exception):
    pass
placeholder = st.empty()
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
placeholder13 = st.empty()
placeholder14 = st.empty()
placeholder15 = st.empty()
# orders_hist = exchange.fetchOpenOrders()
# st.write(orders_hist)
while True:





    # orders_hist_bids = exchange.fetchOpenOrders()
    # orders_hist_asks = exchange.fetchOpenOrders()

    # orders_hist_bids = pd.DataFrame(orders_hist_bids)
    # orders_hist_asks = pd.DataFrame(orders_hist_asks)

    # with placeholder1:
    #     st.write(orders_hist_asks,orders_hist_bids)
    # # with placeholder:
    # #     if orders_hist.empty:
    # #         st.write('no open orders')
    # #     else:
    # #         st.write(orders_hist)
    # orders_hist_bids = orders_hist_bids[orders_hist_bids.side == 'buy']

    orders_hist_bids_id_df = pd.DataFrame()
    # (orders_hist_bids['id'])

    # orders_hist_asks = orders_hist_asks[orders_hist_asks.side == 'sell']
    # orders_hist_asks_id_df = pd.DataFrame(orders_hist_asks['id'])

    #         # st.write(orders_hist)
    #         id = orders_hist_id_df
    #         order_cancel_df = pd.DataFrame()
    #         cancel_df = pd.DataFrame()
    #         cancelAllOrders = exchange.cancelAllOrders()
    #         # st.write(cancelAllOrders)
    #         # for index, row in id.iterrows():
    #         #     order_cancel = exchange.cSancelOrder(id=row['id'])
    #         #     order_cancel_df = order_cancel_df.append(order_cancel, ignore_index=True).astype(str)
    #         st.write("canceled, yalla")
    #         # st.write(order_cancel_df)



    load_makets_for_data = pd.DataFrame(exchange.load_markets()).astype(str)
    # load_makets_for_data = load_makets_for_data[load_makets_for_data.active != 'False']

    # st.write(load_makets_for_data)


    # symbol = st.selectbox('select symbol', 'XBT_USDT')
    symbol = 'XBTUSDT:USDT'
    # load_makets_for_datSa.columns)
    # st.write(load_makets_for_data.columns)

    # pct_expiry_dated = 0.25
    # latest_rateAPY_spot = 0.0088
    # latest_rateAPY_quote = 0.0020
    # alpha = 0
    # apy_to_beat = (((1+latest_rateAPY_quote)*(1+latest_rateAPY_spot)))+alpha-1
    orders_to_place_a_side = 80
    stink_save_bid_drawdown = 0.98
    stink_save_ask_drawup = 1.02

    precision_load = pd.DataFrame(exchange.load_markets())
    precision = (precision_load[symbol]['precision'])

    st.write(precision)
    # symbol = st.selectbox('select symbol', load_makets_for_data.columns)
    precision_amount = precision['amount']
    precision_price = precision['price']
    with placeholder2:
        st.write("precision_amount",precision_amount, "precision_price",precision_price)
    data = (exchange.fetchOrderBook(symbol)) 





    bids = data["bids"]
    bids = pd.DataFrame(bids)
    bids = bids.rename(columns={0: "price_bid", 1: "size_bid"})
    asks = data["asks"]
    asks = pd.DataFrame(asks)
    asks.reset_index(drop=True, inplace=False)
    bids.reset_index(drop = True, inplace=False)
    asks = asks.rename(columns={0: "price_ask", 1: "size_ask"})
    asks['fixed_size_ask'] = asks['size_ask']/precision_amount
    bids['fixed_size_bid'] = bids['size_bid']/precision_amount
    asks = asks.drop(columns=['size_ask'])
    bids = bids.drop(columns=['size_bid'])
    asks = pd.DataFrame(asks)
    bids = pd.DataFrame(bids)
    asks['accumulated']  = (list(accumulate(asks['fixed_size_ask'])))
    asks['accumulated_price']  = (asks['price_ask']) * asks['fixed_size_ask']
    asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
    asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']

    bids['accumulated']  = (list(accumulate(bids['fixed_size_bid'])))
    bids['accumulated_price']  = (bids['price_bid']) * bids['fixed_size_bid']
    bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
    bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']     
    st.write(bids, asks)

    bid_new = pd.DataFrame(bids)
    bid_new['mm_bid_price']  = bids['price_bid'].max() + precision_price
    bid_new['mm_bid_size'] = precision_amount
    bid_new = bid_new.drop(columns=['accumulated', 'accumulated_price', 'accumulated_avg_price','cash_equivelant','price_bid','fixed_size_bid'])
    st.write(bid_new)
    stink_save_bid = bid_new['mm_bid_price'].max()*stink_save_bid_drawdown
    bid_new = bid_new[bid_new.mm_bid_price > stink_save_bid]
    st.write(bid_new)

    i = 0


    # testing_bids = pd.DataFrame(columns=['price_bid', 'size_bid'])
    # while i < orders_to_place_a_side:
    #     testing_bids.loc[-1] = [bid_new['mm_bid_price'].max() + (i * precision_price) , precision_amount]  # adding a row
    #     testing_bids.index = testing_bids.index + 1  # shifting index
    #     testing_bids = testing_bids.sort_index() 
    #     i += 1
    # st.write(testing_bids)

    # st.write(bid_new)
    # order_init = exchange.createLimitBuyOrder(symbol=symbol,price=testing_bids['price_bid'],amount=testing_bids['size_bid'])
    # st.write(order_init)
    order_df_bid = pd.DataFrame()
    with placeholder3:
        st.write(np.random.randint(5))
        if len(orders_hist_bids_id_df) < orders_to_place_a_side/2:
            for col_name, data in bid_new.iterrows():
                while i < orders_to_place_a_side:
                    mm_bid_price = (data['mm_bid_price']) - (precision_price * np.random.randint(3) *i)
                    mm_bid_size = (data['mm_bid_size']) 
                    order_init_bid = exchange.createLimitBuyOrder(symbol=symbol,price=mm_bid_price,amount=mm_bid_size)
                    # add the logs to the dataframe
                    order_df_bid =  order_df_bid.append(order_init_bid, ignore_index=True)
 
                    #  order_df_bid.append(order_init_bid, ignore_index=True)
                    i += 1
        else:
            for col_name, data in orders_hist_bids_id_df.iterrows():
                for col_name, data in bid_new.iterrows():
                    while i < orders_to_place_a_side:
                        orders_hist_bids = orders_hist_bids[orders_hist_bids.status == 'open']
                        orders_hist_bids_id_df = pd.DataFrame(orders_hist_bids['id'])

                        id_bids = orders_hist_bids_id_df
                        id_bids = (orders_hist_bids_id_df['id'])
                        id_bids = id_bids.iloc[0]
                        type = 'limit'
                        side = 'buy'
                        mm_bid_price = bid_new['mm_bid_price']
                        mm_bid_price =  mm_bid_price.iloc[0] - (precision_price * np.random.randint(30) *i)
                        mm_bid_size = bid_new['mm_bid_size']
                        mm_bid_size = mm_bid_size.iloc[0] 
                        try:
                            order_init_bid = exchange.editOrder(id=id_bids,symbol=symbol,type=type,side=side,price=mm_bid_price,amount=mm_bid_size)
                        except Exception:
                            pass
                        # st.write(order_df_bid)
                        order_df_bid = pd.concat([order_df_bid, pd.DataFrame(order_init_bid)], axis=0)
                        # order_df_bid
                        # .append(order_init_bid, ignore_index=True)
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
    # st.write(bid_new)
    # st.plotly_chart(px.bar(bid_new,y=bid_new['mm_bid_size'], x=bid_new['mm_bid_price']))
    # st.plotly_chart(px.line(bid_new,y=bid_new['accumulated'], x=bid_new['mm_bid_price']))
    # st.plotly_chart(px.line(bid_new,y=bid_new['cash_equivelant'], x=bid_new['mm_bid_price']))
    with placeholder4:
        st.write(order_df_bid)









    mid_ish = ((asks['price_ask'].min() + bids['price_bid'].max())) / 2
    steps = round(mid_ish/precision_price)
    with placeholder5:
        st.write("mid_ish", mid_ish, "steps", steps)








    ask_new = pd.DataFrame(asks)
    ask_new['mm_ask_price']  = asks['price_ask'].min() - precision_price
    # + 400
    ask_new['mm_ask_size'] = precision_amount
    ask_new = ask_new.drop(columns=['accumulated', 'accumulated_price', 'accumulated_avg_price','cash_equivelant','price_ask','fixed_size_ask'])
    # st.write(ask_new)
    stink_save_ask = ask_new['mm_ask_price'].min()*stink_save_ask_drawup
    # st.write(stink_save_ask)
    ask_new = ask_new[ask_new.mm_ask_price < stink_save_ask]
    # st.write(ask_new)


    order_df_ask = pd.DataFrame(columns=['price','remaining'])

    ref_ask = asks['price_ask'].min() - precision_price
    ref_ask_size = precision_amount


    ii = 0


    with placeholder6:
        st.write(np.random.randint(5))
        if len(orders_hist_asks_id_df) < orders_to_place_a_side/2 or orders_hist_asks_id_df.empty:
            # st.write("no orders to make")
            for col_name, data in ask_new.iterrows():
                while ii < orders_to_place_a_side:

                    mm_ask_price = (data['mm_ask_price']) + (precision_price * np.random.randint(3)*ii)
                    mm_ask_size = (data['mm_ask_size']) 
                    order_init_ask = exchange.createLimitSellOrder(symbol=symbol,price=mm_ask_price,amount=mm_ask_size)
                    order_df_ask = order_df_ask.append(order_init_ask, ignore_index=True)
                    ii += 1
        else:   
            for col_name, data in orders_hist_asks_id_df.iterrows():
                for col_name, data in ask_new.iterrows():
                    while ii < orders_to_place_a_side:
                        orders_hist_asks = orders_hist_asks[orders_hist_asks.status == 'open']
                        orders_hist_asks_id_df = pd.DataFrame(orders_hist_asks['id'])

                        id_ask = (orders_hist_asks_id_df['id'])
                        id_ask = id_ask.iloc[0]
                        type = 'limit'
                        side = 'sell'
                        mm_ask_price = ask_new['mm_ask_price']
                        mm_ask_price =  mm_ask_price.iloc[0] - (precision_price * np.random.randint(30) *ii)
                        mm_ask_size = ask_new['mm_ask_size']
                        mm_ask_size = mm_ask_size.iloc[0]
                        try:
                            order_init_ask = exchange.editOrder(id=id_ask,symbol=symbol,type=type,side=side,price=mm_ask_price,amount=mm_ask_size)
                        except Exception:
                            pass
               
                        order_df_ask = order_df_ask.append(order_init_ask, ignore_index=True)
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
    with placeholder7:     
        st.write(order_df_ask)




    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=asks['price_ask'], y=asks['accumulated'], name="asks"),secondary_y=True,)
    fig.add_trace(go.Scatter(x=bids['price_bid'], y=bids['accumulated'], name="bids"),secondary_y=True,)
    fig.update_layout(title_text="orderbook")
    with placeholder8:     

        st.plotly_chart(fig, use_container_width=True)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=bids['price_bid'], y=bids['fixed_size_bid'], name="bids"),secondary_y=True,)
    fig.add_trace(go.Bar(x=asks['price_ask'], y=asks['fixed_size_ask'], name="asks"),secondary_y=True,)
    fig.update_layout(title_text="orderbook")
    with placeholder10:
        st.plotly_chart(fig, use_container_width=True)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=asks['accumulated_avg_price'], y=asks['cash_equivelant'], name="asks"),secondary_y=True,)
    fig.add_trace(go.Scatter(x=bids['accumulated_avg_price'], y=bids['cash_equivelant'], name="bids"),secondary_y=True,)
    fig.update_layout(title_text="cash_equivelant")
    with placeholder9:
        st.plotly_chart(fig, use_container_width=True)
    with placeholder11:
        st.write("above is them, below is us")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=order_df_ask['price'], y=order_df_ask['accumulated'], name="asks"),secondary_y=True,)
    fig.add_trace(go.Scatter(x=order_df_bid['price'], y=order_df_bid['accumulated'], name="bids"),secondary_y=True,)
    fig.update_layout(title_text="orderbook")
    with placeholder12:
        st.plotly_chart(fig, use_container_width=True)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=order_df_ask['price'], y=order_df_ask['mm_ask_size'], name="asks"),secondary_y=True,)
    fig.add_trace(go.Bar(x=order_df_bid['price'], y=order_df_bid['mm_bid_size'], name="bids"),secondary_y=True,)
    fig.update_layout(title_text="orderbook")
    with placeholder13:
        st.plotly_chart(fig, use_container_width=True)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=order_df_ask['price'], y=order_df_ask['cash_equivelant'], name="asks"),secondary_y=True,)
    fig.add_trace(go.Scatter(x=order_df_bid['price'], y=order_df_bid['cash_equivelant'], name="bids"),secondary_y=True,)
    fig.update_layout(title_text="orderbook")
    with placeholder14:
        st.plotly_chart(fig, use_container_width=True)




