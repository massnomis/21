import asyncio
import ccxt.async_support as ccxta  # noqa: E402
import time
import os
import sys
import ccxtpro
import pandas as pd
import streamlit as st

symbol = 'ETH/USDT'

def sync_client(exchange_id):
    orderbook = None
    exchange = getattr(ccxtpro, exchange_id)()
    try:
        exchange.load_markets()
        market = exchange.market(symbol)
        orderbook = exchange.watch_order_book(market['symbol'])
    except Exception as e:
        print(type(e).__name__, str(e))
    return { 'exchange': exchange.id, 'orderbook': orderbook }
async def async_client(exchange_id):
    orderbook = None
    exchange = getattr(ccxtpro, exchange_id)()
    try:
        await exchange.load_markets()
        market = exchange.market(symbol)  
        orderbook = await exchange.watch_order_book(symbol)
    except Exception as e:
        print(type(e).__name__, str(e))
    await exchange.close()
    return { 'exchange': exchange.id, 'orderbook': orderbook }
async def multi_orderbooks(exchanges):
    input_coroutines = [async_client(exchange) for exchange in exchanges]
    orderbooks = await asyncio.gather(*input_coroutines, return_exceptions=True)


    to_fetch = pd.DataFrame(orderbooks)
    placeholder = st.empty()
    with placeholder:
        st.write(to_fetch)
    # st.write(orderbooks)
    # print(orderbooks)
    return orderbooks
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
while True:
    # global orderbooks
    exchanges = ["ftx", "binance"]
    loop.run_until_complete(multi_orderbooks(exchanges))
    # st.write(orderbooks)





# ftx_holder = st.empty()
# exchange_dump = orderbooks['orderbooks']
# if exchange_dump == 'FTX':
#     orderbooks = ftx_ob
#     ftx_ob = orderbooks

# with ftx_holder:
#     st.write(ftx_ob)