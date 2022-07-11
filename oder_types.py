import ccxt
import streamlit as st
import pandas as pd
exchange = ccxt.bitmex({
    'apiKey': 'NOAb2TuyuLgWkYbXOQGH-x9b',
    'secret': '_fAxf57mItdpX-A5KTxXRzJZY3zkeSKdCGlStwa95FAH81Gd',
})
if 'test' in exchange.urls:
    exchange.urls['api'] = exchange.urls['test'] # ←----- switch the base URL to testnet
x = pd.DataFrame(exchange.load_markets())
symbol = st.selectbox("pair", (pd.DataFrame(exchange.load_markets()).columns), index = 494 )

st.write(x.astype(str))
precision = (x[symbol]['precision'])
precision_amount = precision['amount']
st.write(precision)
st.write(precision_amount)
# info = (x[symbol]['info'])
# info = pd.DataFrame(info)
# st.write(info)
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
# st.write(asks_update)
# st.write(bids_update)
asks['accumulated']  = (list(accumulate(asks['fixed_size_ask'])))
asks['accumulated_price']  = (asks['price_ask']) * asks['fixed_size_ask']
asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']

bids['accumulated']  = (list(accumulate(bids['fixed_size_bid'])))
bids['accumulated_price']  = (bids['price_bid']) * bids['fixed_size_bid']
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

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=asks['price_ask'], y=asks['accumulated'], name="asks"),secondary_y=True,)
fig.add_trace(go.Scatter(x=bids['price_bid'], y=bids['accumulated'], name="bids"),secondary_y=True,)
fig.update_layout(title_text="orderbook")
st.plotly_chart(fig, use_container_width=True)

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(x=asks['price_ask'], y=asks['fixed_size_ask'], name="asks"),secondary_y=True,)
fig.add_trace(go.Bar(x=bids['price_bid'], y=bids['fixed_size_bid'], name="bids"),secondary_y=True,)
fig.update_layout(title_text="orderbook")
st.plotly_chart(fig, use_container_width=True)

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=asks['accumulated_avg_price'], y=asks['cash_equivelant'], name="asks"),secondary_y=True,)
fig.add_trace(go.Scatter(x=bids['accumulated_avg_price'], y=bids['cash_equivelant'], name="bids"),secondary_y=True,)
fig.update_layout(title_text="cash_equivelant")
st.plotly_chart(fig, use_container_width=True)

column = bids["price_bid"]
max_value_spot = column.max()
st.write("now",datetime.now())
st.write("best bid", max_value_spot)

column = asks["price_ask"]
min_value_spot = column.min()
st.write("best ask", min_value_spot)

spred_spot = min_value_spot - max_value_spot
st.write("spot spread", spred_spot)

spred_bps_spot = spred_spot/min_value_spot*1000
st.write("spred_bps", spred_bps_spot , "bps")


a = np.array([1, 2, 3, 4, 5])
st.write(a)
b = np.random.randint(10, size=(2, 10))
st.write(b)
arr = np.array([a, a])
st.write(arr)





for i in range(1, 2):
    colz = st.columns(2)
    # colz[0].write(pd.DataFrame(exchange.fetchCurrencies()).columns)

    colz[1].write(pd.DataFrame(exchange.load_markets()).columns)

    colz[0].write(pd.DataFrame(exchange.fetchCurrencies()).columns)

# st.write(pd.DataFrame(exchange.load_markets()).columns)
# st.write(pd.DataFrame(exchange.fetchCurrencies()).columns)
# st.write(pd.DataFrame(exchange.fetchTickers()).columns)


exchange_tickers_check = st.checkbox('Show all tickers')
if exchange_tickers_check:
    exchange.fetchTickers = exchange.fetchTickers()

    st.write(exchange.fetchTickers)
symbol = st.selectbox("pair", (pd.DataFrame(exchange.load_markets()).columns), index = 494 )

exchange_currencies_check = st.checkbox('Show all currencies')
exchange.fetchCurrencies = exchange.fetchCurrencies()

if exchange_currencies_check:

    st.write(exchange.fetchCurrencies)



exchange_markets_check = st.checkbox('Show exchange markets')
if exchange_markets_check:
    exchange.markets = exchange.load_markets()

    st.write(exchange.markets)



account_info_check =st.checkbox('Show account info')
if account_info_check:
    account_info = (exchange.fetch_balance())
    account_info = pd.DataFrame(account_info['info'])
    account_info_specific = st.selectbox('Select account', account_info['currency'])
    st.write(account_info)
    st.write(account_info[account_info['currency'] == account_info_specific])




fetch_status_check = st.checkbox('Show status')
if fetch_status_check:
    exchange.fetchStatus = exchange.fetchStatus()
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

# NEEDS SYMBOL POSITIONAL ARG
# exchange.fetchOrderBook = exchange.fetchOrderBook()
# fetch_order_book_check = st.checkbox('Show order book')
# if fetch_order_book_check:
#     st.write(exchange.fetchOrderBook)

# # NEEDS SYMBOL POSITIONAL ARG
# exchange.fetchOHLCV = exchange.fetchOHLCV()
# fetch_ohlcv_check = st.checkbox('Show ohlcv')
# if fetch_ohlcv_check:
#     st.write(exchange.fetchOHLCV)












def fetchTrades_into_df(symbol):
    exchange.fetchTrades = exchange.fetchTrades(symbol=symbol)
    fetchTrades = (exchange.fetchTrades)
    fetchTrades_df = pd.DataFrame(fetchTrades)
    trade_info = pd.DataFrame()
    fixed_df = pd.DataFrame()
    for index, row in fetchTrades_df.iterrows():
        trade_info = trade_info.append(row['info'],ignore_index=True)
    fixed_df = pd.merge(fetchTrades_df, trade_info, left_index=True, right_index=True)
    fixed_df = fixed_df.drop(columns=['info'])
    st.write(fixed_df)
fetchTrades_into_df_q = st.checkbox("fetchTrades_into_df_q?")
if fetchTrades_into_df_q:
    fetchTrades_into_df(symbol='XBTUSD')
# fetchTrades_into_df(symbol='XBTUSD')






def fetch_my_Trades_into_df(symbol):
    exchange.fetchMyTrades = exchange.fetchMyTrades(symbol=symbol)
    fetchMyTrades = (exchange.fetchMyTrades)
    fetchMyTrades_df = pd.DataFrame(fetchMyTrades)
    trade_info = pd.DataFrame()
    fixed_df = pd.DataFrame()
    for index, row in fetchMyTrades_df.iterrows():
        trade_info = trade_info.append(row['info'],ignore_index=True)
    fixed_df = pd.merge(fetchMyTrades_df, trade_info, left_index=True, right_index=True)
    fixed_df = fixed_df.drop(columns=['info'])
    st.write(fixed_df)
fetch_my_Trades_into_df_q = st.checkbox("fetch_my_Trades_into_df?")
if fetch_my_Trades_into_df_q:
    fetch_my_Trades_into_df(symbol='XBTUSD')




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





from datetime import datetime
import calendar

def OHLCV_to_df(symbol):
    now = datetime.utcnow()
    unixtime = calendar.timegm(now.utctimetuple())
    since = (unixtime - 60*60) * 1000 # UTC timestamp in milliseconds
    ohlcv = exchange.fetch_ohlcv(symbol=symbol, timeframe='5m', since=since, limit=12)
    start_dt = datetime.fromtimestamp(ohlcv[0][0]/1000)
    end_dt = datetime.fromtimestamp(ohlcv[-1][0]/1000)
    df = pd.DataFrame(ohlcv, columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Time'] = [datetime.fromtimestamp(float(time)/1000) for time in df['Time']]
    df.set_index('Time', inplace=True)
    st.write(df)
OLHC_q = st.checkbox("OLHC?")
if OLHC_q:
    OHLCV_to_df(symbol='XBTUSD')


    
symbol = 'XBTUSD'
type = 'market'
side = 'buy'
amount = 100
# price = null
# params = {}
order_type = st.selectbox("order_ype", ['createMarketSellOrder', 'createMarketBuyOrder', 'createLimitSellOrder', 'createLimitBuyOrder'])

if order_type == 'createMarketSellOrder':
    order_check = st.checkbox('Create Market Sell Order')
    if order_check:
        order_init = exchange.create_market_sell_order(symbol=symbol, amount=amount)
        st.write(order_init)
if order_type == 'createMarketBuyOrder':
    order_check = st.checkbox('Order Check')
    if order_check:
        order_init = exchange.createMarketBuyOrder(symbol=symbol,amount=amount)
        st.write(order_init)
if order_type == 'createLimitSellOrder':
    order_check = st.checkbox('Order Check')
    if order_check:
        order_init = exchange.createLimitSellOrder(symbol=symbol,price=price,amount=amount)
        st.write(order_init)
if order_type == 'createLimitBuyOrder':
    order_check = st.checkbox('Order Check')
    if order_check:
        order_init = exchange.createLimitBuyOrder(symbol=symbol,price=price,amount=amount)
        st.write(order_init)
# CCXT - required Unified CCXT market symbol (e.g. 'BTC/USD')
# type
# market, limit
# side
# buy, sell
# amount
# price



#   // camelCaseNotation
#   exchange.createMarketSellOrder (symbol, amount, params)
#   exchange.createMarketBuyOrder (symbol, amount, params)

#   // underscore_notation
#   exchange.create_market_sell_order (symbol, amount, params)
#   exchange.create_market_buy_order (symbol, amount, params)

#   // using general createMarketOrder and side = 'buy' or 'sell'
#   exchange.createMarketOrder (symbol, side, amount, params)
#   exchange.create_market_order (symbol, side, amount, params)

#   // using general createOrder, type = 'market' and side = 'buy' or 'sell'
#   exchange.createOrder (symbol, 'market', side, amount, ...)
#   exchange.create_order (symbol, 'market', side, amount, ...)


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
