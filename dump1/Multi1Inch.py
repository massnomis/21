import streamlit as st
import requests
import json
import pandas as pd
import math
import time
from itertools import chain

import plotly.express as px

#def get_price():
#    res = requests.get(url='',params={
#    'fromTokenAddress=':
#                       })
#    print(json.dumps(res.json(), indent=5, sort_keys=True))
#    return res.json()['price']
#    
##    url_swapToken_p1 = (f"https://api.1inch.io/v4.0/{chain_id}/quote?fromTokenAddress=")
##    url_swapToken_p2 = '{}&toTokenAddress={}&amount={}'.format(address_of_said_tokenIN, address_of_said_tokenOUT, DecimalFix)
##    url_swapToken_p3 = url_swapToken_p1 + url_swapToken_p2
##    st.write(url_swapToken_p3)
##
##
##    token_return = requests.get(url_swapToken_p3)
##    token_return = json.loads(token_return.text)
##    amount_toToken = int(token_return['toTokenAmount'])


# eth op bsc, gnosis poly arb avax
d = {'i':[], 'input':[],'eth': [], 'op': [], 'bsc':[],'gnosis':[],'poly':[],'arb':[],'avax':[],'bestoutput':[]}
df = pd.DataFrame(d)
i = 0
# qq = {'i':[], 'input':[],'eth': [], 'op': [], 'bsc':[],'gnosis':[],'poly':[],'arb':[],'avax':[],'max':[]}
# df2 = pd.DataFrame(qq)
# st.write(df)
while i < 10:
    i = i+1
    input = 0.1
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
    BSC = "https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&toTokenAddress=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&amount=100000000000000000"

    token_return = requests.get(BSC)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])

    amount_toToken_correct_BSC = ((amount_toToken) / (10 ** 6))
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
    findmaxlist = [amount_toToken_correct_eth,amount_toToken_correct_op,amount_toToken_correct_BSC,amount_toToken_correct_GNOSIS, amount_toToken_correct_POLY, amount_toToken_correct_ARB,amount_toToken_correct_AVAX]


    bestoutput = max(findmaxlist)

    bestoutput = str(bestoutput)


    df.loc[i] = [i,input,amount_toToken_correct_eth,amount_toToken_correct_op,amount_toToken_correct_BSC,amount_toToken_correct_GNOSIS, amount_toToken_correct_POLY, amount_toToken_correct_ARB,amount_toToken_correct_AVAX,bestoutput]

    time.sleep(1)

    # st.write(df)




st.write(df)
chart = px.line(
    df, #this is the dataframe you are trying to plot
    x = "i",
    y = ['eth','op','bsc','gnosis','poly','arb','avax'],
    orientation = "v",
    # color = "WEIGHT",
    template = "plotly_white",
    width = 1000,
    height = 600
)
st.plotly_chart(chart)




# https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&toTokenAddress=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&amount=1000000000000000000
# https://api.1inch.io/v4.0/10/quote?fromTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&toTokenAddress=0x7f5c764cbc14f9669b88837ca1490cca17c31607&amount=1000000000000000000
# https://api.1inch.io/v4.0/56/quote?fromTokenAddress=0x2170ed0880ac9a755fd29b2688956bd959f933f8&toTokenAddress=0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d&amount=1000000000000000000
# https://api.1inch.io/v4.0/56/quote?fromTokenAddress=0x6a023ccd1ff6f2045c3309768ead9e68f978f6e1&toTokenAddress=0xddafbb505ad214d7b80b1f830fccc89b60fb7a83&amount=1000000000000000000
# https://api.1inch.io/v4.0/137/quote?fromTokenAddress=0x7ceb23fd6bc0add59e62ac25578270cff1b9f619&toTokenAddress=0x2791bca1f2de4661ed88a30c99a7a9449aa84174&amount=1000000000000000000
# https://api.1inch.io/v4.0/42161/quote?fromTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&toTokenAddress=0xff970a61a04b1ca14834a43f5de4533ebddb5cc8&amount=1000000000000000000
# https://api.1inch.io/v4.0/43114/quote?fromTokenAddress=0x49d5c2bdffac6ce2bfdb6640f4f80f226bc10bab&toTokenAddress=0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e&amount=1000000000000000000

