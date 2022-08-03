
from CurveSim import pool
import streamlit as st
import plotly
import math
import plotly.express as px
import pandas as pd
import requests
import json

t_f = False
st.sidebar.write("Choose y-axis scale")
check = st.sidebar.checkbox("Linear/Log")
if check:
    t_f = True


CRV = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/d6b45546-4c33-4453-83ed-b0c29f24a2f1/data/latest",
convert_dates=["TIMESTAMP_NTZ"],
)


cvxCRV = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/e67ea397-b602-49b4-9e04-007960d14e78/data/latest",
convert_dates=["TIMESTAMP_NTZ"],
)
A = st.number_input('Amplification Coefficient', min_value=None, max_value=None, value=50)
st.write(A)


fee = st.number_input('fee_bps', min_value=None, max_value=None, value=(4))
st.write(fee)


CRV_b = int(CRV['BALANCE'].iloc[0])
cvxCRV_b = int(cvxCRV['BALANCE'].iloc[0])

# fee = 4
# A = 50
Token_Amt_0 = CRV_b
Token_Amt_1 = cvxCRV_b

Token_Amt_0 = st.number_input('Token_Amt_0', min_value=None, max_value=None, value=Token_Amt_0)
st.write(Token_Amt_0)


Token_Amt_1 = st.number_input('Token_Amt_1', min_value=None, max_value=None, value=Token_Amt_1)
st.write(Token_Amt_1)



p = pool(A, [Token_Amt_0, Token_Amt_1], 2, p=None, tokens=None, fee = (fee*10**6) )
st.write(p.xp())










max_token = max(Token_Amt_0,Token_Amt_1)

# st.write(max_token)

# from_token = st.number_input('from_token', min_value=0, max_value=1, value=(1))
# to_token = st.number_input('to_token', min_value=0, max_value=1, value=(0))



def make_lists(r, func):
    t = list(r)
    return t, [func(x) for x in t]

xlist, ylist = make_lists(range(1000,max_token +1, 1000), lambda i: p.dydxfee(0, 1, i))
# xlist, ylist = make_lists([i / 10 for i in range(100)], lambda x: math.sin(x))

df = pd.DataFrame(list(zip(xlist, ylist)), columns = ['x','y'])

aaa = px.scatter(
    df, #this is the dataframe you are trying to plot
    x = 'x',
    y = 'y',
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600,
    log_y = t_f

)
# st.write(from_token + to_token)
st.plotly_chart(aaa)




def make_lists(r, func):
    t = list(r)
    return t, [func(x) for x in t]

xlist, ylist = make_lists(range(1000,max_token +1, 1000), lambda i: p.dydxfee(1, 0, i))
# xlist, ylist = make_lists([i / 10 for i in range(100)], lambda x: math.sin(x))

df = pd.DataFrame(list(zip(xlist, ylist)), columns = ['x','y'])

aaa = px.scatter(
    df, #this is the dataframe you are trying to plot
    x = 'x',
    y = 'y',
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600,
    log_y = t_f

)
# st.write(from_token + to_token)
st.plotly_chart(aaa)

# st.write(p.xp())
# st.write(p.D())
# st.write(p.y())
# st.write(p.y_D())
# st.write(p.dy())
# st.write(p.exchange())
# st.write(p.remove_liquidity_imbalance())
# st.write(p.calc_withdraw_one_coin())
# st.write(p.dydx())
# dydxfee
# optarb
# optarbs


