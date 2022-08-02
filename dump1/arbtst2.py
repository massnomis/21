import time
import logging

import requests
import json
import pandas as pd
import math

from itertools import chain

import plotly.express as px
import streamlit as st

qq = {'i':[], 'number_unformat':[], 'rate2':[]}
df2 = pd.DataFrame(qq)

tick_size = .1
i = 0
number_unformat = 10000
decimal_of_said_tokenIN = 18
decimal_of_said_tokenOUT = 18




while i < 30:
    DecimalFix = int(math.pow(10,decimal_of_said_tokenIN) * number_unformat)
    url_swapToken_p3 = f'https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&toTokenAddress=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48&amount={DecimalFix}'
    token_return = requests.get(url_swapToken_p3)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return['toTokenAmount'])
    amount_toToken_correct = ((amount_toToken) / (10 ** decimal_of_said_tokenOUT))
    rate1 = number_unformat / amount_toToken_correct
    rate2 = amount_toToken_correct / 22
    l1 = requests.get(url_swapToken_p3)
    l2 = json.loads(l1.text)
    number_unformat = number_unformat * (1.1 + tick_size)
    df2.loc[i] = [i, number_unformat, rate2]
    i = i + 1
st.write(df2)
















Final_Path = px.bar(
    df2, #this is the dataframe you are trying to plot
    x = "number_unformat",
    y = "rate2",
    # color = "path",
    # title = "<b>DIY / Choose your own adventure - Polygon Fees</b>",
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600
)
st.plotly_chart(Final_Path)

Final_Path = px.bar(
    df2, #this is the dataframe you are trying to plot
    x = "number_unformat",
    y = "rate2",
    # color = "path",
    # title = "<b>DIY / Choose your own adventure - Polygon Fees</b>",
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600
)
st.plotly_chart(Final_Path)

Final_Path = px.scatter(
    df2, #this is the dataframe you are trying to plot
    x = "number_unformat",
    y = "rate2",
    # color = "path",
    # title = "<b>DIY / Choose your own adventure - Polygon Fees</b>",
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600
)
st.plotly_chart(Final_Path)
Final_Path2 = px.scatter(
    df2, #this is the dataframe you are trying to plot
    x = "rate2",
    y = "number_unformat",
    # color = "path",
    # title = "<b>DIY / Choose your own adventure - Polygon Fees</b>",
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600
)
st.plotly_chart(Final_Path2)
Final_Path = px.line(
    df2, #this is the dataframe you are trying to plot
    x = "number_unformat",
    y = "rate2",
    # color = "path",
    # title = "<b>DIY / Choose your own adventure - Polygon Fees</b>",
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600
)
st.plotly_chart(Final_Path)
Final_Path2 = px.line(
    df2, #this is the dataframe you are trying to plot
    x = "rate2",
    y = "number_unformat",
    # color = "path",
    # title = "<b>DIY / Choose your own adventure - Polygon Fees</b>",
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600
)
st.plotly_chart(Final_Path2)




