import streamlit as st
import requests
import json
import pandas as pd
import math

from itertools import chain

import plotly.express as px
qq = {'i':[], 'input':[],'eth': [], 'op': [], 'bsc':[],'gnosis':[],'poly':[],'arb':[],'avax':[],'bestoutput':[]}
df2 = pd.DataFrame(qq)



input1 = 300
input = input1 * (10 ** 4)
i = 0
qqq = 0
while qqq < 150:
    inverse_url_eth = (f"https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&toTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&amount={input}")
    token_return = requests.get(inverse_url_eth)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])
    inverse_eth = ((amount_toToken) / (10 ** 16))
    # st.write(inverse_eth)

    inverse_url_op = (f"https://api.1inch.io/v4.0/10/quote?fromTokenAddress=0x7f5c764cbc14f9669b88837ca1490cca17c31607&toTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&amount={input}")
    token_return = requests.get(inverse_url_op)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])
    inverse_op = ((amount_toToken) / (10 ** 16))
    # st.write(inverse_op)

    inverse_url_bsc = (f"https://api.1inch.io/v4.0/56/quote?fromTokenAddress=0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d&toTokenAddress=0x2170ed0880ac9a755fd29b2688956bd959f933f8&amount={input}")
    token_return = requests.get(inverse_url_bsc)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])
    inverse_bsc = ((amount_toToken) / (10 ** 4))
    # st.write(inverse_bsc)

    inverse_url_gnosis = (f"https://api.1inch.io/v4.0/100/quote?fromTokenAddress=0xddafbb505ad214d7b80b1f830fccc89b60fb7a83&toTokenAddress=0x6a023ccd1ff6f2045c3309768ead9e68f978f6e1&amount={input}")
    token_return = requests.get(inverse_url_gnosis)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])
    inverse_gnosis = ((amount_toToken) / (10 ** 16))
    # st.write(inverse_gnosis)

    inverse_url_poly = (f"https://api.1inch.io/v4.0/137/quote?fromTokenAddress=0x2791bca1f2de4661ed88a30c99a7a9449aa84174&toTokenAddress=0x7ceb23fd6bc0add59e62ac25578270cff1b9f619&amount={input}")
    token_return = requests.get(inverse_url_eth)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])
    inverse_poly = ((amount_toToken) / (10 ** 16))
    # st.write(inverse_poly)

    inverse_url_arb = (f"https://api.1inch.io/v4.0/42161/quote?fromTokenAddress=0xff970a61a04b1ca14834a43f5de4533ebddb5cc8&toTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&amount={input}")
    token_return = requests.get(inverse_url_arb)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])
    inverse_arb = ((amount_toToken) / (10 ** 16))
    # st.write(inverse_arb)

    inverse_url_avax = (f"https://api.1inch.io/v4.0/43114/quote?fromTokenAddress=0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e&toTokenAddress=0x49d5c2bdffac6ce2bfdb6640f4f80f226bc10bab&amount={input}")
    token_return = requests.get(inverse_url_avax)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])
    inverse_avax = ((amount_toToken) / (10 ** 16))
    # st.write(inverse_avax)

    findmaxlistinv = [inverse_eth, inverse_op, inverse_bsc,
                 inverse_gnosis, inverse_poly, inverse_arb,
                 inverse_avax]
    bestoutput = max(findmaxlistinv)
    bestoutput = (bestoutput)

    df2.loc[i] = [i, input1, inverse_eth, inverse_op, inverse_bsc,
                 inverse_gnosis, inverse_poly, inverse_arb,
                 inverse_avax, bestoutput]
    # st.write(df2)

    st.write(bestoutput)
    qqq = qqq+1
