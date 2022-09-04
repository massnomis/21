from operator import index
from turtle import title
import ccxtpro
import asyncio
from numpy import place
import streamlit as st
import json
import pandas as pd
from itertools import accumulate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

import ccxt
import plotly.express as px

st.set_page_config(layout="wide")





placeholder0 = st.empty()
palceholder_market_info = st.empty()
placeholder_open_orders = st.empty()
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


# exchange = ccxtpro.binanceus({
#     'apiKey': "RsNqghLfN0ZG1iP0mNyngzSTYSzdmzTMgWEObBgjhi2GkEUoMYJSUsRJvN9xGrgR",
#     'secret': "G5453sx9t46JRWVNdIDvaSA1EKIqbBmSds8QXQGkaNCiPEqoJ3jkPQ6MLghQXTJl",
# })


# secret = str("G5453sx9t46JRWVNdIDvaSA1EKIqbBmSds8QXQGkaNCiPEqoJ3jkPQ6MLghQXTJl")

# exchange_ccxt = ccxt.binanceus({
#     'apiKey': "RsNqghLfN0ZG1iP0mNyngzSTYSzdmzTMgWEObBgjhi2GkEUoMYJSUsRJvN9xGrgR",
#     'secret': secret,
# })



exchange = ccxt.bitmex({
    'apiKey': 'NOAb2TuyuLgWkYbXOQGH-x9b',
    'secret': '_fAxf57mItdpX-A5KTxXRzJZY3zkeSKdCGlStwa95FAH81Gd',
})
if 'test' in exchange.urls:
    exchange.urls['api'] = exchange.urls['test'] # ←----- switch the base URL to testnet
# st.write(exchange.fetchOpenOrders())


exchange_ccxt = ccxtpro.bitmex({
    'apiKey': 'NOAb2TuyuLgWkYbXOQGH-x9b',
    'secret': '_fAxf57mItdpX-A5KTxXRzJZY3zkeSKdCGlStwa95FAH81Gd',
})
if 'test' in exchange_ccxt.urls:
    exchange_ccxt.urls['api'] = exchange_ccxt.urls['test'] # ←----- switch the base URL to testnet
markets = exchange_ccxt.load_markets()
markets = pd.DataFrame.from_dict(markets)
df1 = pd.DataFrame.from_dict(markets)
df1 = df1.astype(str)
df1 = df1.columns
with placeholder0.container():
    market = st.selectbox("Select Markets", df1)
    # st.write(market)
with palceholder_market_info.container():
    precision_load = pd.DataFrame(exchange_ccxt.load_markets())
    recision_load = precision_load.astype(str)
    # st.write(recision_load)
    min_size = (precision_load[market]['limits']['cost']['min'])
    precision_base = (precision_load[market]['precision']['base'])
    precision_quote = (precision_load[market]['precision']['quote'])
    base = (precision_load[market]['base'])
    quote = (precision_load[market]['quote'])
    st.write(f"Precision: {base} {precision_base} {quote} {precision_quote}")
    st.write(f"Min Size: {min_size}")


orders_hist = exchange_ccxt.fetchOpenOrders(symbol=market)
orders_hist = pd.DataFrame(orders_hist)

if orders_hist.empty:
    st.write('no open orders')
else:
    st.write(orders_hist)
    orders_hist = orders_hist[orders_hist.status != 'canceled']
    orders_hist = orders_hist[orders_hist.status != 'closed']
    orders_hist_id_df = pd.DataFrame(orders_hist['id'])
    # st.write(orders_hist)
    id = orders_hist_id_df
    order_cancel_df = pd.DataFrame()
    cancel_df = pd.DataFrame()

    for index, row in id.iterrows():
        order_cancel = exchange_ccxt.cancelOrder(symbol=market,id=row['id'])
        order_cancel_df = order_cancel_df.append(order_cancel, ignore_index=True).astype(str)
    st.write("canceled, yalla")
# with placeholder_open_orders.container():
#         balance = exchange.watch_balance()
#         st.json(balance)

# with placeholder_open_orders.container():
#     marketz = st.multiselect("Select Markets", df1)
#     st.write(marketz)
    
# async def OLHC():
    # while True:
    #     ohlc = await exchange.watch_ohlcv(market)
    #     ohlc = pd.DataFrame(ohlc)
    #     ohlc.reset_index(drop=True, inplace=False)
    #     ohlc = ohlc.rename(columns={0: "time", 1: "open", 2: "high", 3: "low", 4: "close", 5: "volume"})
    #     ohlc['time'] = pd.to_datetime(ohlc['time'], unit='ms')
    #     with placeholder1:
    #         fig = go.Figure()
    #         fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
    #         vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
    #         row_width=[0.2, 0.7])
    #         fig.add_trace(go.Candlestick(x=ohlc['time'], open=ohlc['open'], high=ohlc['high'], low=ohlc['low'], close=ohlc['close'], name = "OHLC"), row=1, col=1)
    #         fig.add_trace(go.Bar(x=ohlc['time'], y=ohlc['volume'],showlegend=False, name = 'volume'), row=2, col=1)
    #         fig.update(layout_xaxis_rangeslider_visible=False)
    #         fig.update_layout(title_text="OHLC")
    #         st.plotly_chart(fig, use_container_width=True)
async def trades():
    while True:
        trades = await exchange.watch_trades(market)
        tradez = pd.DataFrame.from_dict(trades)

        with placeholder2.container():
            st.plotly_chart(px.scatter(tradez, x="datetime", y="price", color="side", size='amount',color_discrete_sequence=["red", "green"],), use_container_width=True)
        # await exchange.close()

async def books():
    spread_bps_df_2 = pd.DataFrame()
    # bids_h = pd.DataFrame()
    # asks_h = pd.DataFrame()
    while True:
        orderbook = await exchange.watch_order_book(market)


        # orderbook = pd.DataFrame.from_dict(orderbook)
        # orderbook = orderbook.astype(str)
        # orderbook['time'] = datetime.datetime.now()
        # books_heatmap = books_heatmap.append(orderbook)



        bids = orderbook["bids"]
        bids = pd.DataFrame(bids)
        bids = bids.rename(columns={0: "price_bid", 1: "size_bid"})
        asks = orderbook["asks"]
        asks = pd.DataFrame(asks)
        asks.reset_index(drop=True, inplace=False)
        bids.reset_index(drop = True, inplace=False)
        asks = asks.rename(columns={0: "price_ask", 1: "size_ask"})
        asks['accumulated']  = (list(accumulate(asks['size_ask'])))
        asks['accumulated_price']  = (asks['price_ask']) * asks['size_ask']
        asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
        asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']
        bids['accumulated']  = (list(accumulate(bids['size_bid'])))
        bids['accumulated_price']  = (bids['price_bid']) * bids['size_bid']
        bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
        bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']       
        spread_bps_df_add = pd.DataFrame({'time': [datetime.datetime.now()], 'spread_bps': [(((asks['price_ask'][0] - bids['price_bid'][0])/asks['price_ask'][0]) * 10000)]})
        spread_bps_df_2 = spread_bps_df_2.append(spread_bps_df_add)

        with placeholder3:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=asks['price_ask'], y=asks['accumulated'], name="asks", marker_color = 'red'),secondary_y=True,)
            fig.add_trace(go.Scatter(x=bids['price_bid'], y=bids['accumulated'], name="bids", marker_color = 'green'),secondary_y=True,)
            fig.update_layout(title_text="orderbook")
            st.plotly_chart(fig, use_container_width=True)
        with placeholder4:
            st.plotly_chart(px.scatter(spread_bps_df_2, x="time", y="spread_bps"), use_container_width=True)
        with placeholder5:
            bids_max = orderbook['bids'][0][0]
            bids_start = bids_max + (1/precision_quote)
            st.write(bids_start)
        with placeholder6:
            asks_min = orderbook['asks'][0][0]
            asks_start = asks_min - (1/precision_quote)
            st.write(asks_start)
        with placeholder7:
            predicted_spread = (((asks_start - bids_start)/asks_start) * 10000)
            st.write(predicted_spread)
        

        i = 0
        ii = 0
        while i < 1:
            order_init_b = exchange_ccxt.createLimitBuyOrder(symbol=market,price=bids_start,amount=0.01)
            i += 1
        while ii < 1:
            order_init_a = exchange_ccxt.createLimitSellOrder(symbol=market,price=asks_start,amount=0.01)
            ii += 1
        with placeholder8:
            st.write(order_init_b)
        with placeholder9:
            st.write(order_init_a)
        # await exchange.close()


       



async def main():
    # Schedule three calls *concurrently*:
        await asyncio.gather(
        # trades(),
        books(),
        # mm(),




        # await exchange.close()
        # OLHC(),
    )

asyncio.run(main())   