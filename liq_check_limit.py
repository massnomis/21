import pandas as pd
import plotly.express as px
import requests
import streamlit as st
import math
import json

chainID_dict = { "Ethereum": 1, "Binance Smart Chain": 56, "Polygon": 137, "Optimism": 10, "Arbitrum": 42161, "Gnosis Chain": 100, "Avalanche": 43114, "Fantom": 250 }
# chainId_choice = "Ethereum"
chainId_choice_st = st.selectbox("Select Chain ID", list(chainID_dict.keys()))
chainId = chainID_dict[chainId_choice_st] 
page = 1 #  page -Pagination step, default: 1 (page = offset / limit) 
sort_by_dict = {'1': 'createDateTime', '2': 'takerRate', '3': 'makerRate', '4': 'makerAmount', '5': 'takerAmount'}
# sort_by_choice = '1'
sortBy = st.selectbox("Sort by", list(sort_by_dict.values()))
# sortBy = sort_by_dict[sort_by_choice_st]
# limit = 100 #  limit -Number of limit orders to receive (default: 100, max: 500)
limit = st.number_input("Limit", value=100, min_value=1, max_value=500)
limit = int(limit)
st.write(limit)
status_dict = {'1': "%5B1%5D&", '12': "%5B1%2C2%5D&", '123': "%5B1%2C2%2C3%5D&", '2':"%5B2%5D&",'23':"%5B2%2C3%5D&",'3':"%5B3%5D&"}
# status_choice = '_123_' #  
st.write("statuses [1,2,3] 1 - valid limit orders, 2 - temporary invalid limit orders, 3 - invalid limit orders")
status_choice_st = st.selectbox("Status", list(status_dict.keys()))
status = status_dict[status_choice_st]








healthcheck = requests.get(f"https://api.1inch.io/v4.0/{chainId}/healthcheck").json()

st.write("HealthCheck RQ",healthcheck)

tokens_list = requests.get(f"https://api.1inch.io/v4.0/{chainId}/tokens")
tokens_list = json.loads(tokens_list.text)
tokens_list = [tokens_list["tokens"][x] for x in tokens_list["tokens"]]
symbol_list = [elem["symbol"] for elem in tokens_list]
st.write("Tokens List")

st.dataframe(tokens_list)

# button here for manual input or not....
agree = st.checkbox("Manual Address Input?")
address_of_said_tokenIN = "null"
address_of_said_tokenOUT = "null"
decimal_of_said_tokenIN = 0
decimal_of_said_tokenOUT = 0


if agree:
    st.write("noswag")
    token_IN_test = st.text_input("manually addy in", address_of_said_tokenIN)
    st.write(token_IN_test)
    address_of_said_tokenIN = token_IN_test
    token_OUT_test = st.text_input("manually addy out", address_of_said_tokenOUT)
    st.write(token_OUT_test)
    address_of_said_tokenOUT = token_OUT_test
    decimal_of_said_tokenIN = st.number_input("decimal_of_said_tokenIN", value=18)
    decimal_of_said_tokenOUT = st.number_input("decimal_of_said_tokenOUT", value=6)
else:

    st.write("Great!")
    tokens_list = pd.DataFrame(tokens_list)

    tokenIN = st.selectbox("tokenIN", tokens_list['symbol'], index=103)
    address_of_said_tokenIN = tokens_list.set_index("symbol").loc[tokenIN]["address"]
    st.write(address_of_said_tokenIN)

    decimal_of_said_tokenIN = tokens_list.set_index("symbol").loc[tokenIN]["decimals"]
    st.write("decimals:",decimal_of_said_tokenIN)

    tokenOUT = st.selectbox("tokenOUT", tokens_list['symbol'], index=146)
    address_of_said_tokenOUT = tokens_list.set_index("symbol").loc[tokenOUT]["address"]
    st.write(address_of_said_tokenOUT)

    decimal_of_said_tokenOUT = tokens_list.set_index("symbol").loc[tokenOUT]["decimals"]
    st.write("decimals:",decimal_of_said_tokenOUT)









# number_unformat = st.number_input("amt_in", min_value=None, max_value=None, value=0.01)
# st.write(number_unformat)
# DecimalFix = int(math.pow(10, decimal_of_said_tokenIN) * number_unformat)












takerAsset = address_of_said_tokenIN
makerAsset = address_of_said_tokenOUT











url = f'https://limit-orders.1inch.io/v2.0/{chainId}/limit-order/all?page={page}&limit={limit}&statuses={status}sortBy={sortBy}&takerAsset={takerAsset}&makerAsset={makerAsset}'
# url_choice  = st.button("url?")
# if url_choice:
st.write(url)
ping_limit_orders = requests.get(url).json()
# st.write(ping_limit_orders)
ping_limit_orders_to_df = pd.DataFrame(ping_limit_orders)
# st.write(ping_limit_orders_to_df)




fixed_df = ping_limit_orders_to_df.copy()
fixed_df = fixed_df.drop(columns=["signature", "orderHash", "data", "makerAllowance", "isMakerContract"])
fixed_df['fixed_remaining_maker_amount'] = (fixed_df['remainingMakerAmount']).apply(lambda x: float(x)) * (1 / math.pow(10, decimal_of_said_tokenIN))
fixed_df['fixed_maker_balance'] = (fixed_df['makerBalance']).apply(lambda x: float(x)) * (1 / math.pow(10, decimal_of_said_tokenIN))
fixed_df = fixed_df.drop(columns=["remainingMakerAmount", "makerBalance"])
st.write(fixed_df)
stink_save_bid_drawdown = 0.8
stink_save_ask_drawup = 1.2
stink_save_d = fixed_df['makerRate'].median()*stink_save_bid_drawdown
stink_save_u = fixed_df['makerRate'].median()*stink_save_ask_drawup

fixed_df = fixed_df[fixed_df.makerRate.apply(lambda x: float(x)) > stink_save_u]
fixed_df = fixed_df[fixed_df.makerRate.apply(lambda x: float(x)) < stink_save_d]

st.plotly_chart(px.bar(fixed_df, x="makerRate", y="fixed_remaining_maker_amount"))
