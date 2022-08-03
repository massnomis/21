from CurveSim import pool
import streamlit as st
import plotly
import math
import plotly.express as px
import pandas as pd

A = st.select_slider('Amplification Coefficient',[1000 * i for i in range(1, 5+1)])
assets = 3
p0 = 836_355_104
p1 = 1_611_442_201
p2 = 1_656_948_615

p = pool(A, [p0, p1, p2], assets, p=None, tokens=None, fee=3*10**6)
st.write("0: USDT")
st.write("1: DAI")
st.write("2: USDC")

st.write(p.xp())



# fromm = 1
# to = 0
# st.select_slider('from', [0,1,2])
# st.select_slider('to', [0,1,2])


def make_lists(r, func):
    t = list(r)
    return t, [func(x) for x in t]

xlist, ylist = make_lists(range(1,500 +1, 100), lambda i: p.exchange(0, 1, i))
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
st.write('USDT-DAI')
st.plotly_chart(aaa)





p = pool(A, [p0, p1, p2], assets, p=None, tokens=None, fee=3*10**6)

def make_lists(r, func):
    t = list(r)
    return t, [func(x) for x in t]

xlist, ylist = make_lists(range(100000,5000000000 +1, 100000), lambda i: p.dydxfee(0, 1, i))
# xlist, ylist = make_lists([i / 10 for i in range(100)], lambda x: math.sin(x))

df = pd.DataFrame(list(zip(xlist, ylist)), columns = ['x','y'])

aaa = px.scatter(
    df, #this is the dataframe you are trying to plot
    x = 'x',
    y = 'y',
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600

)
st.write('USDT-DAI')
st.plotly_chart(aaa)


p = pool(A, [p0, p1, p2], assets, p=None, tokens=None, fee=3*10**6)

def make_lists(r, func):
    t = list(r)
    return t, [func(x) for x in t]

xlist, ylist = make_lists(range(1,1000000 +1, 100), lambda i: p.dydxfee(0, 1, i))
# xlist, ylist = make_lists([i / 10 for i in range(100)], lambda x: math.sin(x))

df = pd.DataFrame(list(zip(xlist, ylist)), columns = ['x','y'])

aaa = px.scatter(
    df, #this is the dataframe you are trying to plot
    x = 'x',
    y = 'y',
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600

)
st.write('USDT-DAI')
st.plotly_chart(aaa)



p = pool(A, [p0, p1, p2], assets, p=None, tokens=None, fee=3*10**6)

def make_lists(r, func):
    t = list(r)
    return t, [func(x) for x in t]

xlist, ylist = make_lists(range(100000,5000000000 +1, 100000), lambda i: p.dydxfee(1, 0, i))
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
st.write('DAI-USDT')
st.plotly_chart(aaa)



#
# p = pool(A, [836_355_104, 1_611_442_201, 1_656_948_615], 3, p=None, tokens=None, fee=3*10**6)
#
#
#
# def make_lists(r, func):
#     t = list(r)
#     return t, [func(x) for x in t]
#
# xlist, ylist = make_lists(range(10,1000000 +1, 100), lambda i: p.exchange(1, 2, i))
# # xlist, ylist = make_lists([i / 10 for i in range(100)], lambda x: math.sin(x))
#
# df = pd.DataFrame(list(zip(xlist, ylist)), columns = ['x','y'])
#
# aaa = px.bar(
#     df, #this is the dataframe you are trying to plot
#     x = 'x',
#     y = 'y',
#     # color = "TX_TO_ADDRESS_NAME",
#     orientation = "v",
#     template = "plotly_white",
#     width = 1000,
#     height = 600
#
# )
# st.write("DAI-USDC")
# st.plotly_chart(aaa)

#
#
# p = pool(A, [836_355_104, 1_611_442_201, 1_656_948_615], 3, p=None, tokens=None, fee=3*10**6)
#
#
#
#
# def make_lists(r, func):
#     t = list(r)
#     return t, [func(x) for x in t]
#
# xlist, ylist = make_lists(range(10,1000000 +1, 100), lambda i: p.exchange(2, 1, i))
# # xlist, ylist = make_lists([i / 10 for i in range(100)], lambda x: math.sin(x))
#
# df = pd.DataFrame(list(zip(xlist, ylist)), columns = ['x','y'])
#
# aaa = px.bar(
#     df, #this is the dataframe you are trying to plot
#     x = 'x',
#     y = 'y',
#     # color = "TX_TO_ADDRESS_NAME",
#     orientation = "v",
#     template = "plotly_white",
#     width = 1000,
#     height = 600
#
# )
# st.write("USDC-DAI")
# st.plotly_chart(aaa)
# #


#
# p = pool(A, [836_355_104, 1_611_442_201, 1_656_948_615], 3, p=None, tokens=None, fee=3*10**6)
#
# def make_lists(r, func):
#     t = list(r)
#     return t, [func(x) for x in t]
#
# xlist, ylist = make_lists(range(10,1000000 +1, 100), lambda i: p.exchange(0, 2, i))
# # xlist, ylist = make_lists([i / 10 for i in range(100)], lambda x: math.sin(x))
#
# df = pd.DataFrame(list(zip(xlist, ylist)), columns = ['x','y'])
#
# aaa = px.bar(
#     df, #this is the dataframe you are trying to plot
#     x = 'x',
#     y = 'y',
#     # color = "TX_TO_ADDRESS_NAME",
#     orientation = "v",
#     template = "plotly_white",
#     width = 1000,
#     height = 600
#
# )
# st.write("USDT-USDC")
#
# st.plotly_chart(aaa)
# #
# #
# p = pool(A, [836_355_104, 1_611_442_201, 1_656_948_615], 3, p=None, tokens=None, fee=3*10**6)
#
# def make_lists(r, func):
#     t = list(r)
#     return t, [func(x) for x in t]
#
# xlist, ylist = make_lists(range(10,1000000 +1, 100), lambda i: p.exchange(2, 0, i))
# # xlist, ylist = make_lists([i / 10 for i in range(100)], lambda x: math.sin(x))
#
# df = pd.DataFrame(list(zip(xlist, ylist)), columns = ['x','y'])
#
# aaa = px.scatter(
#     df, #this is the dataframe you are trying to plot
#     x = 'x',
#     y = 'y',
#     # color = "TX_TO_ADDRESS_NAME",
#     orientation = "v",
#     template = "plotly_white",
#     width = 1000,
#     height = 600
#
# )
# st.write("USDC-USDT")
# st.plotly_chart(aaa)
#


#
# chain_id = st.select_slider('chain_id',['1','10','56','100','137','42161','43114'])
# st.write("chain_id =" + chain_id)
# https://api.curve.fi/api/getFactoryPools






