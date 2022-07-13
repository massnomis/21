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
exchange = ccxt.bitmex({
    'apiKey': 'NOAb2TuyuLgWkYbXOQGH-x9b',
    'secret': '_fAxf57mItdpX-A5KTxXRzJZY3zkeSKdCGlStwa95FAH81Gd',
})
if 'test' in exchange.urls:
    exchange.urls['api'] = exchange.urls['test'] # ←----- switch the base URL to testnet
x = pd.DataFrame(exchange.load_markets())
symbol = st.selectbox("pair", (pd.DataFrame(exchange.load_markets()).columns), index = 494 )
st.write(symbol)
st.write(x.astype(str))
precision = (x[symbol]['precision'])
precision_amount = precision['amount']
# st.write(precision)
# st.write(precision_amount)
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
# for i in range(1, 2):
#     cols = st.columns(2)
#     cols[0].subheader("bids")

#     cols[0].write(bids)
#     cols[1].subheader("asks")

#     cols[1].write(asks)
# st.write(asks,bids, use_container_width=True)
# st.write(asks_update,bids_update, use_container_width=True)
st.write(asks)
st.write(bids)
# asks.head()

for i in range(len(asks)):
    x = asks['price_ask'].iloc[i]
    y = asks['fixed_size_ask'].iloc[i]
import math

pct_expiry_dated = 0.25
latest_rateAPY_spot = 0.0088
latest_rateAPY_quote = 0.0020

holder = 1*((1-(latest_rateAPY_spot*pct_expiry_dated)))
alpha = 0
apy_to_beat = (((1+latest_rateAPY_quote)*(1+latest_rateAPY_spot)))+alpha-1
holder_2 = (1-(holder*apy_to_beat))*holder

precision_price = 0.05
precision_amount = 1000000



bid_new = pd.DataFrame(bids)
bid_new.head()
bid_new['mm_bid_price']  = round(round(bids['price_bid'] * holder_2 / precision_price) * precision_price, -int(math.floor(math.log10(precision_price))))
bid_new['mm_bid_size'] = bids['fixed_size_bid'] * precision_amount
#  round(round(bids['fixed_size_bid'] * holder_2 / precision_amount) * precision_amount, -int(math.floor(math.log10(precision_amount))))
bid_new = bid_new.drop(columns=['accumulated', 'accumulated_price', 'accumulated_avg_price','cash_equivelant','price_bid','fixed_size_bid'])

bid_new['mm_bid_size']
for col_name, data in bid_new.iterrows():
    x = (data['mm_bid_price'])
    y =(data['mm_bid_size'])
    order_init = exchange.createLimitBuyOrder(symbol='ETH_USDT',price=x,amount=y)
    # order_init = order_init['info']
    order_initt = pd.DataFrame(order_init['info'], index=[0])
    # order_init = order_init.rename(columns={0: "orderID"})
    st.dataframe(order_initt)
# df = {'info': {'orderID': '2feea312-3458-4f9f-b659-8927d18c038e', 'clOrdID': '', 'clOrdLinkID': '', 'account': '403419', 'symbol': 'ETH_USDT', 'side': 'Buy', 'simpleOrderQty': None, 'orderQty': '1000000', 'price': '1047.3', 'displayQty': None, 'stopPx': None, 'pegOffsetValue': None, 'pegPriceType': '', 'currency': 'USDT', 'settlCurrency': '', 'ordType': 'Limit', 'timeInForce': 'GoodTillCancel', 'execInst': '', 'contingencyType': '', 'exDestination': 'XBME', 'ordStatus': 'New', 'triggered': '', 'workingIndicator': True, 'ordRejReason': '', 'simpleLeavesQty': None, 'leavesQty': '1000000', 'simpleCumQty': None, 'cumQty': '0', 'avgPx': None, 'multiLegReportingType': 'SingleSecurity', 'text': 'Submitted via API.', 'transactTime': '2022-07-12T15:49:56.803Z', 'timestamp': '2022-07-12T15:49:56.803Z'}, 'id': '2feea312-3458-4f9f-b659-8927d18c038e', 'clientOrderId': None, 'timestamp': 1657640996803, 'datetime': '2022-07-12T15:49:56.803Z', 'lastTradeTimestamp': 1657640996803, 'symbol': 'ETH_USDT', 'type': 'limit', 'timeInForce': 'GTC', 'postOnly': None, 'side': 'buy', 'price': 1047.3, 'stopPrice': None, 'amount': 1000000.0, 'cost': 0.0, 'average': None, 'filled': 0.0, 'remaining': 1000000.0, 'status': 'open', 'fee': None, 'trades': [], 'fees': []}
# df = pd.DataFrame.from_dict(df)

# df = pd.DataFrame(df)
# st.write(df)
# order_id
