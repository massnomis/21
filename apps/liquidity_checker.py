import json
import math
from itertools import chain

import pandas as pd
import plotly.express as px
import requests
import streamlit as page
import random



page.write("Select Network & Chain ID")
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
page.dataframe(chain_list)


chain_id = page.selectbox(
    "chain_id", ["1", "10", "56", "100", "137", "42161", "43114", "250"], key = random.randint(1, 100)
)
page.write("chain_id =" + chain_id)


healthcheck = requests.get(f"https://api.1inch.io/v4.0/{chain_id}/healthcheck")
healthcheck = json.loads(healthcheck.text)
healthcheck = pd.DataFrame.from_dict(healthcheck, orient="index")
page.write("HealthCheck RQ")
page.dataframe(healthcheck)

tokens_list = requests.get(f"https://api.1inch.io/v4.0/{chain_id}/tokens")
tokens_list = json.loads(tokens_list.text)
tokens_list = [tokens_list["tokens"][x] for x in tokens_list["tokens"]]
symbol_list = [elem["symbol"] for elem in tokens_list]
page.write("Tokens List")

page.dataframe(tokens_list)





tokens_list = pd.DataFrame(tokens_list)


tokenIN = page.selectbox("tokenIN", tokens_list['symbol'], index=10,key = random.randint(1, 100))
address_of_said_tokenIN = tokens_list.set_index("symbol").loc[tokenIN]["address"]
page.write(address_of_said_tokenIN)

decimal_of_said_tokenIN = tokens_list.set_index("symbol").loc[tokenIN]["decimals"]
page.write(decimal_of_said_tokenIN)
tokenOUT = "USDC"

tokenOUT = page.selectbox("tokenOUT", tokens_list['symbol'], index=5, key = random.randint(1, 100))
address_of_said_tokenOUT = tokens_list.set_index("symbol").loc[tokenOUT]["address"]
page.write(address_of_said_tokenOUT)

decimal_of_said_tokenOUT = tokens_list.set_index("symbol").loc[tokenOUT]["decimals"]
page.write(decimal_of_said_tokenOUT)




returned = page.number_input("starting amount in", min_value=None, max_value=None, value=0.01)
page.write(returned)
DecimalFix = int(math.pow(10, decimal_of_said_tokenIN) * returned)


url_swapToken_p1 = f"https://api.1inch.io/v4.0/{chain_id}/quote?fromTokenAddress="
url_swapToken_p2 = "{}&toTokenAddress={}&amount={}".format(
    address_of_said_tokenIN, address_of_said_tokenOUT, DecimalFix
)
url_swapToken_p3 = url_swapToken_p1 + url_swapToken_p2


token_return = requests.get(url_swapToken_p3)
token_return = json.loads(token_return.text)

amount_toToken = int(token_return["toTokenAmount"])
amount_fromToken = int(token_return["fromTokenAmount"])

amount_toToken_correct = (amount_toToken) / (10 ** decimal_of_said_tokenOUT)
amount_fromToken_correct = (amount_toToken) / (10 ** decimal_of_said_tokenIN)



rate1 = returned / amount_toToken_correct
rate = amount_toToken_correct / returned



qq = {"i": [], "returned": [], "rate": []}
df2 = pd.DataFrame(qq)


i = 0

start_range = returned

end_range = page.number_input("end range of quote", min_value=None, max_value=None, value=100)
page.write(end_range)

i_max = page.number_input("how many quotes to check?", min_value=None, max_value=None, value=5)
page.write(i_max)

ping_size = (end_range - start_range) / i_max
DecimalFix = int(math.pow(10, decimal_of_said_tokenIN) * returned)



DecimalFix = int(math.pow(10, decimal_of_said_tokenIN) * returned)
page.write("checking quote number...")

while i < i_max:
    DecimalFix1 = int(math.pow(10, decimal_of_said_tokenIN) * returned)
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
    rate = returned / amount_toToken_correct
    rate = amount_toToken_correct / returned
    l1 = requests.get(url_swapToken_p3)
    l2 = json.loads(l1.text)
    returned = returned + ping_size
    df2.loc[i] = [i, returned, rate]
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
    page.write(i)
page.write(Final_Path)

df2['in'] = df2['rate'] * df2['returned']
df2 = df2[['i', 'in','returned','rate']]
# df2 = df2[-1:] + df2[:-1]
page.dataframe(df2)

Final_Path = px.line(
    df2,  # this is the dataframe you are trying to plot
    x="returned",
    y="rate"
)
page.plotly_chart(Final_Path)
Final_Path = px.bar(
    df2,  # this is the dataframe you are trying to plot
    x="returned",
    y="rate"
)
page.plotly_chart(Final_Path)

