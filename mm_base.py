from operator import index
import ccxtpro
import asyncio
from numpy import place
import streamlit as st
import json
import pandas as pd
from itertools import accumulate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ccxt
import plotly.express as px

st.set_page_config(layout="wide")




placeh = st.empty()
placeg = st.empty()
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

exchange = ccxtpro.binanceus({'enableRateLimit': True})
ccxtbus = ccxt.binanceus()
markets = ccxtbus.load_markets()
# markets = json.loads(markets)
markets = pd.DataFrame.from_dict(markets)
# markets = markets['0']
df1 = pd.DataFrame.from_dict(markets)
df1 = df1.astype(str)
# df1 = pd.DataFrame.from_dict(markets)
df1 = df1.columns
# st.write(df1)
with placeh.container():
    market = st.selectbox("Select Market", df1)


async def trades():
    while True:
        trades = await exchange.watch_trades(market)
        tradez = pd.DataFrame.from_dict(trades)
        with placeg.container():
            st.plotly_chart(px.scatter(tradez, x="datetime", y="price", color="side", size='amount',color_discrete_sequence=["green", "red"],), use_container_width=True)
        # st.plotly_chart(px.line(tradez, x="datetime", y="sum", color="Is_the_buyer_the_market_maker"),use_container_width=True)

        # with placeholder.container():
        #     st.dataframe(tradez)

async def books():
    while True:
        orderbook = await exchange.watch_order_book(market)
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
         

        with placeholder1:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=asks['price_ask'], y=asks['accumulated'], name="asks"),secondary_y=True,)
            fig.add_trace(go.Scatter(x=bids['price_bid'], y=bids['accumulated'], name="bids"),secondary_y=True,)
            fig.update_layout(title_text="orderbook")
            st.plotly_chart(fig, use_container_width=True)
async def main():
    # Schedule three calls *concurrently*:
        await asyncio.gather(

        trades(),
        books()

    )

asyncio.run(main())   