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

import ccxt
import streamlit as st
apiKey = st.text_input("apiKey")
secret = st.text_input("secret")
ftx = ccxt.ftx()
exchange = ccxt.ftx({
    'apiKey': apiKey,
    'secret': secret
})

a = exchange.fetchBalance()
b = exchange.fetchMyTrades()
c = exchange.fetchMarkets()
d = exchange.fetchCurrencies()
st.write("fetchBalance",a,"fetchMyTrades",b,"fetchMarkets",c,"fetchCurrencies",d)
