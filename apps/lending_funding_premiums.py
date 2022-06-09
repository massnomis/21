import streamlit as st
import requests
import json
import pandas as pd
import math
import time
from itertools import accumulate
# from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

from itertools import chain

import plotly.express as px
from datetime import datetime
# ts = int('1645598410')

# print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
import json
import requests
import pandas as pd
import random

premiums = requests.get('https://ftxpremiums.com/assets/data/premiums.json')
premiums = json.loads(premiums.text)
premiums = pd.DataFrame(premiums)
# print(premiums)
st.write("cash and carry premiums")
st.write(premiums)
lending = requests.get('https://ftxpremiums.com/assets/data/lending.json')
lending = json.loads(lending.text)
lending = pd.DataFrame(lending)
# print(lending)    
st.write("lending rates")

st.write(lending)
funding = requests.get('https://ftxpremiums.com/assets/data/funding.json')
funding = json.loads(funding.text)
funding = pd.DataFrame(funding)
# print(funding)
st.write("funding rates")

st.write(funding)
funding_names = funding['name']
# page.write(funding_names)
st.write("Longs pay shorts if positive, shorts pay longs if negative. 1/24 times the average premium over the hour.")
NAME = st.selectbox("Perp Name", funding_names)
custom = requests.get(f"https://ftxpremiums.com/assets/data/funding_data/{NAME}.json").json()

custom = pd.DataFrame(custom)
custom['rate'] = custom['rate'].astype(float)
custom['time'] =  pd.to_datetime(custom['time'], unit='s')
custom = custom.sort_values(by="time")

custom['rate'] = custom['rate'] * 1000
custom['accumulated']  = (list(accumulate(custom['rate'])))

bbbbbb = px.scatter(custom,x='time',y='rate',render_mode="SVG")
st.plotly_chart(bbbbbb)
bbbbbbb = px.scatter(custom,x='time',y='accumulated',render_mode="SVG")
st.plotly_chart(bbbbbbb)


lending_names = lending['name']
# @st.cache
NAME_LENDING = st.selectbox("Lending Token", lending_names)
# page.write(lending_names)

custom_lending = requests.get(f"https://ftx.com/api/spot_margin/history?coin={NAME_LENDING}&start_time=960368456&end_time=1854597556").json()

custom_lending = pd.DataFrame(custom_lending['result'])
custom_lending['rate'] = custom_lending['rate'].astype(float)
custom_lending['time'] =  pd.to_datetime(custom_lending['time'])
custom_lending = custom_lending.sort_values(by="time", ascending=True)

# custom_lending['accumulated']  = (list(accumulate(custom_lending['rate'] * custom_lending['size'])))

custom_lending['rateAPY'] = custom_lending['rate'] * 24 * 36500
custom_lending['interest'] = custom_lending['rate'] * custom_lending['size']
st.write(custom_lending)
aaa = px.line(custom_lending,x='time',y='rate',render_mode="SVG")
st.plotly_chart(aaa)
aaa = px.line(custom_lending,x='time',y='rateAPY',render_mode="SVG")
st.plotly_chart(aaa)
aa = px.line(custom_lending,x='time',y='size',render_mode="SVG")
st.plotly_chart(aa)
a = px.line(custom_lending,x='time',y='interest',render_mode="SVG")
st.plotly_chart(a)
