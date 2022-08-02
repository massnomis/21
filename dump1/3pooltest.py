from CurveSim import pool
import streamlit as st
import plotly
import math
import plotly.express as px
import pandas as pd
import requests
import json

dai = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/61ac1429-fae9-4d53-bf38-d10ef915bc45/data/latest",
convert_dates=["TIMESTAMP_NTZ"],
)


usdt = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/e2016547-e3cb-45d2-b1b5-2dd960d31165/data/latest",
convert_dates=["TIMESTAMP_NTZ"],
)

usdc = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/3e66fa03-a447-41d5-8023-983169e562b8/data/latest",
convert_dates=["TIMESTAMP_NTZ"],
)



dai_b = dai['BALANCE'].iloc[0]
usdt_b = usdt['BALANCE'].iloc[0]
usdc_b = usdc['BALANCE'].iloc[0]



A = st.select_slider('Amplification Coefficient',[1000 * i for i in range(1, 5+1)])
assets = 3
p0 = dai_b
p1 = usdt_b
p2 = usdc_b

p = pool(A, [p0, p1, p2], assets, p=None, tokens=None, fee=3*10**6)
st.write("0: USDT")
st.write("1: DAI")
st.write("2: USDC")

st.write(p.xp())

from_token = 0
to_token = 1
from_token = st.select_slider('from',[0,1,2])
to_token = st.select_slider('to',[0,1,2])

p = pool(A, [p0, p1, p2], assets, p=None, tokens=None, fee=3*10**6)

def make_lists(r, func):
    t = list(r)
    return t, [func(x) for x in t]

xlist, ylist = make_lists(range(100000,5000000000 +1, 100000), lambda i: p.dydxfee(from_token, to_token, i))
# xlist, ylist = make_lists([i / 10 for i in range(100)], lambda x: math.sin(x))

df = pd.DataFrame(list(zip(xlist, ylist)), columns = ['x','y'])

aaa = px.bar(
    df, #this is the dataframe you are trying to plot
    x = 'x',
    y = 'y',
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600

)
st.write(from_token + to_token)
st.plotly_chart(aaa)
