from logging import PlaceHolder
from tkinter import Place
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
import math
import json
st.set_page_config(layout="wide")
PlaceHolder = st.empty()
PlaceHolder1 = st.empty()
PlaceHolder2 = st.empty()
PlaceHolder3 = st.empty()
PlaceHolder4 = st.empty()
PlaceHolder5 = st.empty()
PlaceHolder6 = st.empty()
PlaceHolder7 = st.empty()
PlaceHolder8 = st.empty()
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
tokens_list = tokens_list["tokens"]
tokens_list = pd.DataFrame(tokens_list)
tokens_list = tokens_list.T
tokens_list = tokens_list.reset_index()
# tokens_list = tokens_list.drop(columns=['index','logoURI', 'tags', 'eip2612', 'isFoT', 'synth', 'displayedSymbol'])


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

    tokenIN = st.selectbox("tokenIN", tokens_list['symbol'], index=146)
    address_of_said_tokenIN = tokens_list.set_index("symbol").loc[tokenIN]["address"]
    st.write(address_of_said_tokenIN)

    decimal_of_said_tokenIN = tokens_list.set_index("symbol").loc[tokenIN]["decimals"]
    st.write("decimals:",decimal_of_said_tokenIN)

    tokenOUT = st.selectbox("tokenOUT", tokens_list['symbol'], index=103)
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
try:
    ping_limit_orders = requests.get(url).json()
    # st.write(ping_limit_orders)
    st.json(ping_limit_orders)
    ping_limit_orders_to_df = pd.DataFrame(ping_limit_orders)
    # st.write(ping_limit_orders_to_df)

    fixed_df = ping_limit_orders_to_df.copy()
    st.write(fixed_df)
    # st.write(fixed_df)

    # fixed_df = fixed_df.drop(columns=["signature", "orderHash", "data", "makerAllowance", "isMakerContract"])
    fixed_df['fixed_remaining_maker_amount'] = (fixed_df['remainingMakerAmount']).apply(lambda x: float(x)) * (1 / math.pow(10, decimal_of_said_tokenIN))
    fixed_df['fixed_remaining_maker_amount'] = pd.to_numeric(fixed_df['fixed_remaining_maker_amount'])
    fixed_df['fixed_remaining_maker_amount2'] = 1 / fixed_df['fixed_remaining_maker_amount']     
    fixed_df['fixed_maker_balance'] = (fixed_df['makerBalance']).apply(lambda x: float(x)) * (1 / math.pow(10, decimal_of_said_tokenIN))
    fixed_df['take_dec'] = (decimal_of_said_tokenOUT)
    fixed_df['make_dec'] = (decimal_of_said_tokenIN)
    fixed_df['take_mult'] = (math.pow(10, decimal_of_said_tokenOUT))
    fixed_df['make_mult'] = (math.pow(10, decimal_of_said_tokenIN)) 
    fixed_df['make_take_mult'] =  fixed_df['make_mult'] * fixed_df['take_mult']
    fixed_df['make_take_div1'] = fixed_df['make_mult'] / fixed_df['take_mult']
    fixed_df['make_take_div2'] = fixed_df['take_mult'] / fixed_df['make_mult']
    
    fixed_df['try_fixr8_1'] = pd.to_numeric(fixed_df['makerRate']) * fixed_df['make_take_div1']
    # fixed_df['try_fixr8_2'] = pd.to_numeric(fixed_df['takerRate']) * fixed_df['make_take_div2']
    fixed_df['try_fixr8_3'] = pd.to_numeric(fixed_df['makerRate'])* fixed_df['make_take_div2']
    fixed_df['try_fixr8_4'] = pd.to_numeric(fixed_df['takerRate']) * fixed_df['make_take_div1']
    # fixed_df['fixed_maker_balance'] = pd.to_numeric(fixed_df['fixed_maker_balance']) * fixed_df['make_dec']
    fixed_df['fixed_remaining_maker_amount_init_eh'] =  fixed_df['fixed_remaining_maker_amount'] / fixed_df['make_mult']
    fixed_df['fixed_remaining_maker_amount_init_eh2'] =  fixed_df['fixed_remaining_maker_amount'] / fixed_df['take_mult']
    
    fixed_df = fixed_df.drop(columns=["remainingMakerAmount", "makerBalance"])
    st.write(fixed_df)
    stink_save_bid_drawdown = .00000005
    stink_save_ask_drawup = 2000000000
    stink_save_d = fixed_df['makerRate'].median()*stink_save_bid_drawdown
    stink_save_u = fixed_df['makerRate'].median()*stink_save_ask_drawup
    fixed_df['makerRate'] = pd.to_numeric(fixed_df['makerRate'])
    
    fixed_df['takerRate'] = pd.to_numeric(fixed_df['takerRate'])
    fixed_df.sort_values(by=['makerRate'], inplace=True)

    fixed_df['remaining_liq_cum'] = fixed_df['fixed_remaining_maker_amount'].cumsum()
    fixed_df['remaining_liq_cum_init'] = fixed_df['fixed_remaining_maker_amount_init_eh'].cumsum()
    fixed_df['remaining_liq_cum_init2'] = fixed_df['fixed_remaining_maker_amount_init_eh2'].cumsum()

   # fixed_df = fixed_df[fixed_df.makerRate.apply(lambda x: float(x)) < stink_save_u]
    # fixed_df = fixed_df[fixed_df.makerRate.apply(lambda x: float(x)) > stink_save_d]
    # with PlaceHolder:
    st.plotly_chart(px.bar(fixed_df, x="try_fixr8_3", y="fixed_remaining_maker_amount"), use_container_width=True)
    st.plotly_chart(px.bar(fixed_df, x="try_fixr8_4", y="fixed_remaining_maker_amount"), use_container_width=True)
    st.plotly_chart(px.scatter(fixed_df, x="try_fixr8_3", y="fixed_remaining_maker_amount"), use_container_width=True)
    st.plotly_chart(px.scatter(fixed_df, x="try_fixr8_4", y="fixed_remaining_maker_amount"), use_container_width=True)
    st.plotly_chart(px.line(fixed_df, x="try_fixr8_3", y="remaining_liq_cum"), use_container_width=True)
    st.plotly_chart(px.line(fixed_df, x="try_fixr8_4", y="remaining_liq_cum"), use_container_width=True)
    st.plotly_chart(px.bar(fixed_df, x="try_fixr8_3", y="fixed_remaining_maker_amount_init_eh"), use_container_width=True)
    st.plotly_chart(px.bar(fixed_df, x="try_fixr8_4", y="fixed_remaining_maker_amount_init_eh"), use_container_width=True)
    st.plotly_chart(px.scatter(fixed_df, x="try_fixr8_3", y="fixed_remaining_maker_amount_init_eh"), use_container_width=True)
    st.plotly_chart(px.scatter(fixed_df, x="try_fixr8_4", y="fixed_remaining_maker_amount_init_eh"), use_container_width=True)
    st.plotly_chart(px.line(fixed_df, x="try_fixr8_3", y="remaining_liq_cum_init"), use_container_width=True)
    st.plotly_chart(px.line(fixed_df, x="try_fixr8_4", y="remaining_liq_cum_init"), use_container_width=True)
    st.plotly_chart(px.bar(fixed_df, x="try_fixr8_3", y="fixed_remaining_maker_amount2"), use_container_width=True)
    st.plotly_chart(px.bar(fixed_df, x="try_fixr8_4", y="fixed_remaining_maker_amount2"), use_container_width=True)
    st.plotly_chart(px.scatter(fixed_df, x="try_fixr8_3", y="fixed_remaining_maker_amount"), use_container_width=True)
    st.plotly_chart(px.scatter(fixed_df, x="try_fixr8_4", y="fixed_remaining_maker_amount"), use_container_width=True)
    st.plotly_chart(px.line(fixed_df, x="try_fixr8_3", y="remaining_liq_cum"), use_container_width=True)
    st.plotly_chart(px.line(fixed_df, x="try_fixr8_4", y="remaining_liq_cum"), use_container_width=True)
    st.plotly_chart(px.bar(fixed_df, x="try_fixr8_3", y="fixed_remaining_maker_amount_init_eh2"), use_container_width=True)
    st.plotly_chart(px.bar(fixed_df, x="try_fixr8_4", y="fixed_remaining_maker_amount_init_eh2"), use_container_width=True)
    st.plotly_chart(px.scatter(fixed_df, x="try_fixr8_3", y="fixed_remaining_maker_amount_init_eh2"), use_container_width=True)
    st.plotly_chart(px.scatter(fixed_df, x="try_fixr8_4", y="fixed_remaining_maker_amount_init_eh2"), use_container_width=True)
    st.plotly_chart(px.line(fixed_df, x="try_fixr8_3", y="remaining_liq_cum_init2"), use_container_width=True)
    st.plotly_chart(px.line(fixed_df, x="try_fixr8_4", y="remaining_liq_cum_init2"), use_container_width=True)

except KeyError:
    st.write("No data found") 