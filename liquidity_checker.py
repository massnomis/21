import json
import math
from itertools import chain

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
import random




st.write("Select Network & Chain ID")
chain_list = pd.DataFrame(
    {
        "chain_id": [1, 56, 137, 10, 42161, 100, 43114, 250],
        "chain": [
            "(ETH)",
            "(BSC)",
            "(MATIC)",
            "(OETH)",
            "(AETH)",
            "(xDAI)",
            "(AVAX)",
            "(FTM)",
        ],
    },
    index=[
        "Ethereum",
        "Binance Smart Chain",
        "Polygon",
        "Optimism",
        "Arbitrum",
        "Gnosis Chain",
        "Avalanche",
        "Fantom",
    ],
)
st.dataframe(chain_list)


chain_id = st.selectbox(
    "chain_id", ["1", "10", "56", "100", "137", "42161", "43114", "250"]
)
st.write("chain_id =" + chain_id)


healthcheck = requests.get(f"https://api.1inch.io/v4.0/{chain_id}/healthcheck")
healthcheck = json.loads(healthcheck.text)
healthcheck = pd.DataFrame.from_dict(healthcheck, orient="index")
st.write("HealthCheck RQ")
st.dataframe(healthcheck)

tokens_list = requests.get(f"https://api.1inch.io/v4.0/{chain_id}/tokens")
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
    # st.write(config_p_key)
    decimal_of_said_tokenOUT = st.number_input("decimal_of_said_tokenOUT", value=6)
    # st.write(config_rpc)
else:

    st.write("Great!")
    tokens_list = pd.DataFrame(tokens_list)

    tokenIN = "MATIC"

    tokenIN = st.selectbox("tokenIN", tokens_list['symbol'], index=5)
    address_of_said_tokenIN = tokens_list.set_index("symbol").loc[tokenIN]["address"]
    st.write(address_of_said_tokenIN)

    decimal_of_said_tokenIN = tokens_list.set_index("symbol").loc[tokenIN]["decimals"]
    st.write(decimal_of_said_tokenIN)
    tokenOUT = "USDC"

    tokenOUT = st.selectbox("tokenOUT", tokens_list['symbol'], index=10 )
    address_of_said_tokenOUT = tokens_list.set_index("symbol").loc[tokenOUT]["address"]
    st.write(address_of_said_tokenOUT)

    decimal_of_said_tokenOUT = tokens_list.set_index("symbol").loc[tokenOUT]["decimals"]
    st.write(decimal_of_said_tokenOUT)









number_unformat = st.number_input("amt_in", min_value=None, max_value=None, value=0.01)
st.write(number_unformat)
DecimalFix = int(math.pow(10, decimal_of_said_tokenIN) * number_unformat)


url_swapToken_p1 = f"https://api.1inch.io/v4.0/{chain_id}/quote?fromTokenAddress="
url_swapToken_p2 = "{}&toTokenAddress={}&amount={}".format(
    address_of_said_tokenIN, address_of_said_tokenOUT, DecimalFix
)
url_swapToken_p3 = url_swapToken_p1 + url_swapToken_p2


token_return = requests.get(url_swapToken_p3)
token_return = json.loads(token_return.text)

amount_toToken = int(token_return["toTokenAmount"])

amount_toToken_correct = (amount_toToken) / (10 ** decimal_of_said_tokenOUT)



rate1 = number_unformat / amount_toToken_correct
rate2 = amount_toToken_correct / number_unformat



qq = {"i": [], "number_unformat": [], "rate2": []}
df2 = pd.DataFrame(qq)


i = 0

start_range = number_unformat

end_range = st.number_input("end range of quote", min_value=None, max_value=None, value=10000)
st.write(end_range)

i_max = st.number_input("how many quotes to check?", min_value=None, max_value=None, value=5)
st.write(i_max)

ping_size = (end_range - start_range) / i_max
DecimalFix = int(math.pow(10, decimal_of_said_tokenIN) * number_unformat)



DecimalFix = int(math.pow(10, decimal_of_said_tokenIN) * number_unformat)


while i < i_max:
    DecimalFix1 = int(math.pow(10, decimal_of_said_tokenIN) * number_unformat)
    url_swapToken_p1 = f"https://api.1inch.io/v4.0/{chain_id}/quote?fromTokenAddress="
    url_swapToken_p2 = "{}&toTokenAddress={}&amount={}".format(
        address_of_said_tokenIN, address_of_said_tokenOUT, DecimalFix1
    )
    url_swapToken_p3 = url_swapToken_p1 + url_swapToken_p2
    # st.write(url_swapToken_p3)
    token_return = requests.get(url_swapToken_p3)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return["toTokenAmount"])
    amount_toToken_correct = (amount_toToken) / (10 ** decimal_of_said_tokenOUT)
    rate1 = number_unformat / amount_toToken_correct
    rate2 = amount_toToken_correct / number_unformat
    l1 = requests.get(url_swapToken_p3)
    l2 = json.loads(l1.text)
    number_unformat = number_unformat + ping_size
    df2.loc[i] = [i, number_unformat, rate2]
    i = i + 1
    l1 = requests.get(url_swapToken_p3)
    l2 = json.loads(l1.text)

    actual = l2["protocols"]
    actual = list(chain(*actual))
    series = {
        "hop_num": [],
        "name": [],
        "toTokenAddress": [],
        "fromTokenAddress": [],
        "part": [],
    }
    for hop, item in enumerate(actual):
        for path in item:
            series["hop_num"].append(hop)
            series["name"].append(path["name"])
            series["toTokenAddress"].append(path["toTokenAddress"])
            series["fromTokenAddress"].append(path["fromTokenAddress"])
            series["part"].append(path["part"])
    final = pd.DataFrame.from_dict(series)

    tokens_list = pd.DataFrame(tokens_list)

    right_on_merger = tokens_list.merge(
        final, left_on="address", right_on="toTokenAddress"
    )

    names = {"symbol": "symbol_t"}

    left_on_merger = tokens_list.merge(
        final, left_on="address", right_on="fromTokenAddress"
    )

    namez = {"symbol": "symbol_f"}

    filteredDfL = left_on_merger[["symbol", "hop_num", "name_y", "part"]]
    filteredDfL = filteredDfL.rename(columns=namez)

    filteredDfR = right_on_merger[["symbol", "hop_num", "name_y", "part"]]
    filteredDfR = filteredDfR.rename(columns=names)

    second_last = filteredDfR.merge(filteredDfL)

    second_last["path"] = (
        second_last["symbol_f"]
        + "-"
        + second_last["symbol_t"]
        + ":"
        + second_last["name_y"]
    )

    Final_Path = second_last[["hop_num", "part", "path"]]

    Final_namez = {"name_y": "Liquidity_Source"}
    Final_Path = Final_Path.rename(columns=Final_namez)

st.write(Final_Path)




df2['Token_In_Amount'] = df2['number_unformat']
df2['Rate'] = df2['rate2'] 
df2['Token Out Amount'] = df2['Rate'] * df2['Token_In_Amount']
df2 = df2.drop(columns=['rate2', 'number_unformat']) 

st.write(df2)

Final_Path = px.line(
    df2,  # this is the dataframe you are trying to plot
    x="Token_In_Amount",
    y="Rate"
)
st.plotly_chart(Final_Path)
Final_Path = px.bar(
    df2,  # this is the dataframe you are trying to plot
    x="Token_In_Amount",
    y="Rate"
)
st.plotly_chart(Final_Path)

