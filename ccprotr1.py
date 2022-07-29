import ccxtpro
import asyncio
from numpy import place
import streamlit as st
import pandas as pd
from itertools import accumulate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
st.set_page_config(layout="wide")

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





async def main():
    exchange = ccxtpro.ftx({'enableRateLimit': True})
    exchange2 = ccxtpro.binance({'enableRateLimit': True})
    while True:
        orderbook = await exchange.watch_order_book('ETH/USDT')
        orderbook2 = await exchange2.watch_order_book('ETH/USDT')





        bids2 = orderbook2['bids']
        bids2 = pd.DataFrame(bids2)
        asks2 = orderbook2['asks']
        asks2 = pd.DataFrame(asks2)
        asks2 = asks2.rename(columns={0: "price_ask", 1: "size_ask"})
        bids2 = bids2.rename(columns={0: "price_bid", 1: "size_bid"})
        asks2.reset_index(drop=True, inplace=False)
        bids2.reset_index(drop = True, inplace=False)

        bids = orderbook["bids"]
        bids = pd.DataFrame(bids)
        bids = bids.rename(columns={0: "price_bid", 1: "size_bid"})
        asks = orderbook["asks"]
        asks = pd.DataFrame(asks)
        asks.reset_index(drop=True, inplace=False)
        bids.reset_index(drop = True, inplace=False)
        asks = asks.rename(columns={0: "price_ask", 1: "size_ask"})







        bids3 = bids.merge(bids2, on='price_bid', how='outer')
        bids3['size_bid'] = bids3['size_bid_x'] + bids3['size_bid_y']
        bids3 = bids3.dropna()

        bids3 = bids3.drop(columns=['size_bid_x', 'size_bid_y'])


        asks3 = asks.merge(asks2, on='price_ask', how='outer')
        # asks3['size_ask'] = asks3['size_ask_x'] + asks3['size_ask_y']
        asks3 = asks.dropna()
        # asks3 = asks3.drop(columns=['size_ask_x', 'size_ask_y'])

        

        
        asks2['accumulated']  = (list(accumulate(asks2['size_ask'])))
        asks2['accumulated_price']  = (asks2['price_ask']) * asks2['size_ask']
        asks2['accumulated_avg_price'] = (list(accumulate(asks2['accumulated_price'])))  / asks2['accumulated']
        asks2['cash_equivelant'] = asks2['accumulated'] * asks2['accumulated_avg_price']
        bids2 = bids2.rename(columns={0: "price_bid", 1: "size_bid"})
        bids2['accumulated']  = (list(accumulate(bids2['size_bid'])))
        bids2['accumulated_price']  = (bids2['price_bid']) * bids2['size_bid']
        bids2['accumulated_avg_price'] = (list(accumulate(bids2['accumulated_price'])))  / bids2['accumulated']
        bids2['cash_equivelant'] = bids2['accumulated'] * bids2['accumulated_avg_price']






      
        asks['accumulated']  = (list(accumulate(asks['size_ask'])))
        asks['accumulated_price']  = (asks['price_ask']) * asks['size_ask']
        asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
        asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']
        bids['accumulated']  = (list(accumulate(bids['size_bid'])))
        bids['accumulated_price']  = (bids['price_bid']) * bids['size_bid']
        bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
        bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']       
         



        asks3['accumulated']  = (list(accumulate(asks3['size_ask'])))
        asks3['accumulated_price']  = (asks3['price_ask']) * asks3['size_ask']
        asks3['accumulated_avg_price'] = (list(accumulate(asks3['accumulated_price'])))  / asks3['accumulated']
        asks3['cash_equivelant'] = asks3['accumulated'] * asks3['accumulated_avg_price']
        bids3['accumulated']  = (list(accumulate(bids3['size_bid'])))
        bids3['accumulated_price']  = (bids3['price_bid']) * bids3['size_bid']
        bids3['accumulated_avg_price'] = (list(accumulate(bids3['accumulated_price'])))  / bids3['accumulated']
        bids3['cash_equivelant'] = bids3['accumulated'] * bids3['accumulated_avg_price']

        with placeholder:
            for i in range(1, 2):
                cols = st.columns(2)
                cols[0].subheader("bids")
                cols[0].write(bids)
                cols[1].subheader("asks")
                cols[1].write(asks)
        with placeholder1:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=asks['price_ask'], y=asks['accumulated'], name="asks"),secondary_y=True,)
            fig.add_trace(go.Scatter(x=bids['price_bid'], y=bids['accumulated'], name="bids"),secondary_y=True,)
            fig.update_layout(title_text="orderbook")
            st.plotly_chart(fig, use_container_width=True)
        with placeholder2:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Bar(x=asks['price_ask'], y=asks['size_ask'], name="asks"),secondary_y=True,)
            fig.add_trace(go.Bar(x=bids['price_bid'], y=bids['size_bid'], name="bids"),secondary_y=True,)
            fig.update_layout(title_text="orderbook")
            st.plotly_chart(fig, use_container_width=True)
        with placeholder3:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=asks['accumulated_avg_price'], y=asks['cash_equivelant'], name="asks"),secondary_y=True,)
            fig.add_trace(go.Scatter(x=bids['accumulated_avg_price'], y=bids['cash_equivelant'], name="bids"),secondary_y=True,)
            fig.update_layout(title_text="cash_equivelant")
            st.plotly_chart(fig, use_container_width=True)
        with placeholder4:
            for i in range(1, 2):
                cols = st.columns(2)
                cols[0].subheader("bids")
                cols[0].write(bids2)
                cols[1].subheader("asks")
                cols[1].write(asks2)
        with placeholder5:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=asks2['price_ask'], y=asks2['accumulated'], name="asks"),secondary_y=True,)
            fig.add_trace(go.Scatter(x=bids2['price_bid'], y=bids2['accumulated'], name="bids"),secondary_y=True,)
            fig.update_layout(title_text="orderbook")
            st.plotly_chart(fig, use_container_width=True)
        with placeholder6:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Bar(x=asks2['price_ask'], y=asks2['size_ask'], name="asks"),secondary_y=True,)
            fig.add_trace(go.Bar(x=bids2['price_bid'], y=bids2['size_bid'], name="bids"),secondary_y=True,)
            fig.update_layout(title_text="orderbook")
            st.plotly_chart(fig, use_container_width=True)
        with placeholder7:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=asks2['accumulated_avg_price'], y=asks2['cash_equivelant'], name="asks"),secondary_y=True,)
            fig.add_trace(go.Scatter(x=bids2['accumulated_avg_price'], y=bids2['cash_equivelant'], name="bids"),secondary_y=True,)
            fig.update_layout(title_text="cash_equivelant")
            st.plotly_chart(fig, use_container_width=True)
        with placeholder8:
            # bids3['size_bid2'] = bids3['size_bid2'].fillna(0)

            for i in range(1, 2):
                cols = st.columns(2)
                cols[0].subheader("bids")
                cols[0].write(bids3)
                cols[1].subheader("asks")
                cols[1].write(asks3)
        with placeholder9:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=asks3['price_ask'], y=asks3['accumulated'], name="asks"),secondary_y=True,)
            fig.add_trace(go.Scatter(x=bids3['price_bid'], y=bids3['accumulated'], name="bids"),secondary_y=True,)
            fig.update_layout(title_text="orderbook")
            st.plotly_chart(fig, use_container_width=True)
        with placeholder10:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Bar(x=asks3['price_ask'], y=asks3['size_ask'], name="asks"),secondary_y=True,)
            fig.add_trace(go.Bar(x=bids3['price_bid'], y=bids3['size_bid'], name="bids"),secondary_y=True,)
            fig.update_layout(title_text="orderbook")
            st.plotly_chart(fig, use_container_width=True)
        with placeholder11:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=asks3['accumulated_avg_price'], y=asks3['cash_equivelant'], name="asks"),secondary_y=True,)
            fig.add_trace(go.Scatter(x=bids3['accumulated_avg_price'], y=bids3['cash_equivelant'], name="bids"),secondary_y=True,)
            fig.update_layout(title_text="cash_equivelant")
            st.plotly_chart(fig, use_container_width=True)
        # with placeholder12:

            # st.write(bids3)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
while True:
    loop.run_until_complete(main())