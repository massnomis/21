from CurveSim import pool
import streamlit as st
import plotly
import math
import plotly.express as px
import pandas as pd
import random


A = st.select_slider('Amplification Coefficient',[10 * i for i in range(1, 5+1)], key = random.randint(1, 100))


CRV = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/d6b45546-4c33-4453-83ed-b0c29f24a2f1/data/latest",
convert_dates=["TIMESTAMP_NTZ"],
)


cvxCRV = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/e67ea397-b602-49b4-9e04-007960d14e78/data/latest",
convert_dates=["TIMESTAMP_NTZ"],
)



CRV_b = CRV['BALANCE'].iloc[0]
cvxCRV_b = cvxCRV['BALANCE'].iloc[0]

assets = 2
p0 = CRV_b
p1 = cvxCRV_b


p = pool(A, [p0, p1], assets, p=None, tokens=None, fee=15*10**6)
st.write("0: CRV")
st.write("1: cvxCRV")


st.write(p.xp())






def make_lists(r, func):
    t = list(r)
    return t, [func(x) for x in t]

xlist, ylist = make_lists(range(1000,100000000 +1, 1000), lambda i: p.dydxfee(0, 1, i))
# xlist, ylist = make_lists([i / 10 for i in range(100)], lambda x: math.sin(x))

df = pd.DataFrame(list(zip(xlist, ylist)), columns = ['x','y'])

aaa = px.scatter(
    df, #this is the dataframe you are trying to plot
    x = 'x',
    y = 'y'

)
st.write('CRV-CVXCRV')
st.plotly_chart(aaa)

def make_lists(r, func):
    t = list(r)
    return t, [func(x) for x in t]

xlist, ylist = make_lists(range(1000,100000000 +1, 1000), lambda i: p.dydxfee(1, 0, i))
# xlist, ylist = make_lists([i / 10 for i in range(100)], lambda x: math.sin(x))

df = pd.DataFrame(list(zip(xlist, ylist)), columns = ['x','y'])

aaa = px.scatter(
    df, #this is the dataframe you are trying to plot
    x = 'x',
    y = 'y'

)
st.write('CVXCRV-CRV')
st.plotly_chart(aaa)

#
#
#
#
#
#
# CRV = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/d6b45546-4c33-4453-83ed-b0c29f24a2f1/data/latest",
# convert_dates=["TIMESTAMP_NTZ"],
# )
#
#
# cvxCRV = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/e67ea397-b602-49b4-9e04-007960d14e78/data/latest",
# convert_dates=["TIMESTAMP_NTZ"],
# )
#
#
#
# CRV_b = CRV['BALANCE'].iloc[0]
# cvxCRV_b = cvxCRV['BALANCE'].iloc[0]
#
# A = st.select_slider('Amplification Coefficient',[10 * i for i in range(1, 5+1)])
# assets = 3
# p0 = CRV_b
# p1 = cvxCRV_b
#
#
# p = pool(A, [p0, p1], assets, p=None, tokens=None, fee=15*10**6)
# st.write("0: CRV")
# st.write("1: cvxCRV")
#
#
# st.write(p.xp())
#
#

# def make_lists(r, func):
#     t = list(r)
#     return t, [func(x) for x in t]
#
# xlist, ylist = make_lists(range(100,100+1, 1), lambda i: p.dydxfee(0, 1, i))
# # xlist, ylist = make_lists([i / 10 for i in range(100)], lambda x: math.sin(x))
#
# df = pd.DataFrame(list(zip(xlist, ylist)), columns = ['x','y'])
#
# aaa = px.scatter(
#     df, #this is the dataframe you are trying to plot
#     x = 'x',
#     y = 'y',
#     orientation = "v",
#     template = "plotly_white",
#     width = 1000,
#     height = 600,
#     log_y = t_f
#
# )
# st.write('CRV-CVXCRV')
# st.plotly_chart(aaa)
#
# def make_lists(r, func):
#     t = list(r)
#     return t, [func(x) for x in t]
#
# xlist, ylist = make_lists(range(1,1000 +1, 1), lambda i: p.dydxfee(1, 0, i))
# # xlist, ylist = make_lists([i / 10 for i in range(100)], lambda x: math.sin(x))
#
# df = pd.DataFrame(list(zip(xlist, ylist)), columns = ['x','y'])
#
# aaa = px.scatter(
#     df, #this is the dataframe you are trying to plot
#     x = 'x',
#     y = 'y',
#     orientation = "v",
#     template = "plotly_white",
#     width = 1000,
#     height = 600,
#     log_y = t_f
#
# )
# st.write('CVXCRV-CRV')
# st.plotly_chart(aaa)

# d6b45546-4c33-4453-83ed-b0c29f24a2f1
# CRV

# e67ea397-b602-49b4-9e04-007960d14e78
# cvxCRV





