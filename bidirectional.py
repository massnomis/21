import streamlit as page
import requests
import json
import pandas as pd
import math
import time
from itertools import chain

import plotly.express as px

# eth op bsc, gnosis poly arb avax


st.write("ETH-USDC and Back")
d = {'i':[], 'input':[],'eth': [], 'op': [],'gnosis':[],'poly':[],'arb':[],'avax':[],'bestoutput':[]}
df = pd.DataFrame(d)
i = 0
qq = {'i':[], 'input':[],'eth': [], 'op': [],'gnosis':[],'poly':[],'arb':[],'avax':[],'max':[]}
df2 = pd.DataFrame(qq)
qqq = 0
while qqq < 10:
    eth = "https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&toTokenAddress=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&amount=100000000000000000"

    token_return = requests.get(eth)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])

    amount_toToken_correct_eth = ((amount_toToken) / (10 ** 6))

    # st.write("token output MAIN")
    # st.write(amount_toToken_correct_eth)



    # st.write("token output OP")
    op = "https://api.1inch.io/v4.0/10/quote?fromTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&toTokenAddress=0x7f5c764cbc14f9669b88837ca1490cca17c31607&amount=100000000000000000"

    token_return = requests.get(op)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])

    amount_toToken_correct_op = ((amount_toToken) / (10 ** 6))
    # st.write(amount_toToken_correct_op)

    # st.write("token output BSC")

    # st.write(amount_toToken_correct_BSC)

    # st.write("token output GNOSIS")
    GNOSIS = "https://api.1inch.io/v4.0/56/quote?fromTokenAddress=0x2170ed0880ac9a755fd29b2688956bd959f933f8&toTokenAddress=0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d&amount=100000000000000000"

    token_return = requests.get(GNOSIS)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])

    amount_toToken_correct_GNOSIS = ((amount_toToken) / (10 ** 18))
    # st.write(amount_toToken_correct_GNOSIS)

    # st.write("token output POLY")
    POLY = "https://api.1inch.io/v4.0/137/quote?fromTokenAddress=0x7ceb23fd6bc0add59e62ac25578270cff1b9f619&toTokenAddress=0x2791bca1f2de4661ed88a30c99a7a9449aa84174&amount=100000000000000000"

    token_return = requests.get(POLY)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])

    amount_toToken_correct_POLY = ((amount_toToken) / (10 ** 6))
    # st.write(amount_toToken_correct_POLY)

    # st.write("token output ARB")
    ARB = "https://api.1inch.io/v4.0/42161/quote?fromTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&toTokenAddress=0xff970a61a04b1ca14834a43f5de4533ebddb5cc8&amount=100000000000000000"

    token_return = requests.get(ARB)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])

    amount_toToken_correct_ARB = ((amount_toToken) / (10 ** 6))
    # st.write(amount_toToken_correct_ARB)

    # st.write("token output AVAX")
    AVAX = "https://api.1inch.io/v4.0/43114/quote?fromTokenAddress=0x49d5c2bdffac6ce2bfdb6640f4f80f226bc10bab&toTokenAddress=0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e&amount=100000000000000000"

    token_return = requests.get(AVAX)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])

    amount_toToken_correct_AVAX = ((amount_toToken) / (10 ** 6))
    # st.write(amount_toToken_correct_AVAX)
    findmaxlist = [amount_toToken_correct_eth,amount_toToken_correct_op,amount_toToken_correct_GNOSIS, amount_toToken_correct_POLY, amount_toToken_correct_ARB,amount_toToken_correct_AVAX]


    bestoutput = max(findmaxlist)

    bestoutput = str(bestoutput)
    bestoutputxxx = bestoutput
    # chainb = df.idxmax(axis=1)
    inputfixed = 0.1
    df.loc[i] = [i,inputfixed,amount_toToken_correct_eth,amount_toToken_correct_op,amount_toToken_correct_GNOSIS, amount_toToken_correct_POLY, amount_toToken_correct_ARB,amount_toToken_correct_AVAX,bestoutput]

    # st.write(bestoutput)
    bestoutput_fixed = bestoutput.replace(".", "")
    # st.write(bestoutput_fixed)
    input1 = bestoutput_fixed
    input = input1

    # st.write(input)


    inverse_url_eth = (f"https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&toTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&amount={input}")
    # st.write(inverse_url_eth)
    token_return = requests.get(inverse_url_eth)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])
    inverse_eth = ((amount_toToken) / (10 ** 18))
    # st.write(inverse_eth)

    inverse_url_op = (f"https://api.1inch.io/v4.0/10/quote?fromTokenAddress=0x7f5c764cbc14f9669b88837ca1490cca17c31607&toTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&amount={input}")
    token_return = requests.get(inverse_url_op)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])
    inverse_op = ((amount_toToken) / (10 ** 18))
    # st.write(inverse_op)



    inverse_url_gnosis = (f"https://api.1inch.io/v4.0/100/quote?fromTokenAddress=0xddafbb505ad214d7b80b1f830fccc89b60fb7a83&toTokenAddress=0x6a023ccd1ff6f2045c3309768ead9e68f978f6e1&amount={input}")
    token_return = requests.get(inverse_url_gnosis)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])
    inverse_gnosis = ((amount_toToken) / (10 ** 18))
    # st.write(inverse_gnosis)

    inverse_url_poly = (f"https://api.1inch.io/v4.0/137/quote?fromTokenAddress=0x2791bca1f2de4661ed88a30c99a7a9449aa84174&toTokenAddress=0x7ceb23fd6bc0add59e62ac25578270cff1b9f619&amount={input}")
    token_return = requests.get(inverse_url_eth)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])
    inverse_poly = ((amount_toToken) / (10 ** 18))
    # st.write(inverse_poly)

    inverse_url_arb = (f"https://api.1inch.io/v4.0/42161/quote?fromTokenAddress=0xff970a61a04b1ca14834a43f5de4533ebddb5cc8&toTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&amount={input}")
    token_return = requests.get(inverse_url_arb)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])
    inverse_arb = ((amount_toToken) / (10 ** 18))
    # st.write(inverse_arb)

    inverse_url_avax = (f"https://api.1inch.io/v4.0/43114/quote?fromTokenAddress=0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e&toTokenAddress=0x49d5c2bdffac6ce2bfdb6640f4f80f226bc10bab&amount={input}")
    token_return = requests.get(inverse_url_avax)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])
    inverse_avax = ((amount_toToken) / (10 ** 18))
    # st.write(inverse_avax)

    findmaxlistinv = [inverse_eth, inverse_op, 
                inverse_gnosis, inverse_poly, inverse_arb,
                inverse_avax]
    bestoutput = max(findmaxlistinv)
    bestoutput = (bestoutput)

    df2.loc[i] = [i, bestoutputxxx, inverse_eth, inverse_op, 
                inverse_gnosis, inverse_poly, inverse_arb,                    inverse_avax, bestoutput]
    # st.write(df)
    # st.write(df2)
    # st.write(bestoutput)
    profit = bestoutput - 0.1
    # final = df.append([df], [df2])

    # st.write(final)
    qqq = qqq+1
    i = i+1

    # st.write(profit)
    # page.write(qqq)
    time.sleep(1)

page.write(df)
page.write(df2)
chart = px.line(
    df, #this is the dataframe you are trying to plot
    x = "i",
    y = ['eth','op','gnosis','poly','arb','avax'],
    orientation = "v",
    # color = "WEIGHT",
    template = "plotly_white",
    width = 1000,
    height = 600
)
page.plotly_chart(chart)
chart2 = px.line(
    df2, #this is the dataframe you are trying to plot
    x = "i",
    y = ['eth','op','gnosis','poly','arb','avax'],
    orientation = "v",
    # color = "WEIGHT",
    template = "plotly_white",
    width = 1000,
    height = 600
)
page.plotly_chart(chart2)

