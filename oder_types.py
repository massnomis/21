import ccxt
import streamlit as st
import pandas as pd
exchange = ccxt.bitmex({
    'apiKey': 'NOAb2TuyuLgWkYbXOQGH-x9b',
    'secret': '_fAxf57mItdpX-A5KTxXRzJZY3zkeSKdCGlStwa95FAH81Gd',
})
if 'test' in exchange.urls:
    exchange.urls['api'] = exchange.urls['test'] # ←----- switch the base URL to testnet



exchange.fetchTickers = exchange.fetchTickers()
exchange_tickers_check = st.checkbox('Show all tickers')
if exchange_tickers_check:
    st.write(exchange.fetchTickers)



exchange.fetchCurrencies  = exchange.fetchCurrencies()
exchange_currencies_check = st.checkbox('Show all currencies')
if exchange_currencies_check:
    st.write(exchange.fetchCurrencies)



exchange.markets = exchange.load_markets()
exchange_markets_check = st.checkbox('Show exchange markets')
if exchange_markets_check:
    st.write(exchange.markets)


account_info = (exchange.fetch_balance())
account_info = pd.DataFrame(account_info['info'])
account_info_check =st.checkbox('Show account info')
if account_info_check:
    account_info_specific = st.selectbox('Select account', account_info['currency'])
    st.write(account_info)
    st.write(account_info[account_info['currency'] == account_info_specific])











exchange.fetchOrderBook = exchange.fetchOrderBook()
fetch_order_book_check = st.checkbox('Show order book')
if fetch_order_book_check:
    st.write(exchange.fetchOrderBook)


exchange.fetchOHLCV = exchange.fetchOHLCV()
fetch_ohlcv_check = st.checkbox('Show ohlcv')
if fetch_ohlcv_check:
    st.write(exchange.fetchOHLCV)



exchange.fetchStatus = exchange.fetchStatus()
fetch_status_check = st.checkbox('Show status')
if fetch_status_check:
    st.write(exchange.fetchStatus)






# NEEDS SYMBOL POSITIONAL ARG
# exchange.fetchTicker = exchange.fetchTicker()
# exchange_ticker_check = st.checkbox('Show ticker')
# if exchange_ticker_check:
#     st.write(exchange.fetchTicker)



# NEEDS SYMBOL POSITIONAL ARG
# exchange.fetchTrades = exchange.fetchTrades()
# fetch_trades_check = st.checkbox('Show trades')
# if fetch_trades_check:
#     st.write(exchange.fetchTrades)




# NEEDS SYMBOL POSITIONAL ARG
# exchange.fetchMyTrades = exchange.fetchMyTrades()
# fetch_trades_check = st.checkbox('Show my trades')
# if fetch_trades_check:
#     st.write(exchange.fetchMyTrades)


















   # LoadMarkets            .           fetchBalance       |
# |       fetchMarkets           .            createOrder       |
# |       fetchCurrencies        .            cancelOrder       |
# |       fetchTicker            .             fetchOrder       |
# |       fetchTickers           .            fetchOrders       |
# |       fetchOrderBook         .        fetchOpenOrders       |
# |       fetchOHLCV             .      fetchClosedOrders       |
# |       fetchStatus            .          fetchMyTrades       |
# |       fetchTrades            .                deposit       |
# |                              .               withdraw    











#  limit
# limit limit
# limit stop
# limit click
# limit chase
# limit scale

# market
# market market
# market stop
# market swarm
# market TWAP

# reduce

# POST/IOC
# margin
