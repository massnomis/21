import streamlit as st
import requests
import json
import pandas as pd
import math
from itertools import accumulate
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

from itertools import chain

import plotly.express as px
from datetime import datetime
# ts = int('1645598410')

# print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
import json
import requests
import pandas as pd
import random
def app():
    page = st.container()
    premiums = requests.get('https://ftxpremiums.com/assets/data/premiums.json')
    premiums = json.loads(premiums.text)
    premiums = pd.DataFrame(premiums)
    # print(premiums)
    page.write(premiums)
    lending = requests.get('https://ftxpremiums.com/assets/data/lending.json')
    lending = json.loads(lending.text)
    lending = pd.DataFrame(lending)
    # print(lending)
    page.write(lending)
    funding = requests.get('https://ftxpremiums.com/assets/data/funding.json')
    funding = json.loads(funding.text)
    funding = pd.DataFrame(funding)
    # print(funding)
    page.write(funding)
    funding_names = funding['name']
    page.write(funding_names)
    page.write("Longs pay shorts if positive, shorts pay longs if negative. 1/24 times the average premium over the hour.")
    NAME = page.selectbox("Perp Name", funding_names, index =2,key = random.randint(1, 100))
    custom = requests.get(f"https://ftxpremiums.com/assets/data/funding_data/{NAME}.json").json()

    custom = pd.DataFrame(custom)
    custom['rate'] = custom['rate'].astype(float)
    custom['time'] =  pd.to_datetime(custom['time'], unit='s')
    custom = custom.sort_values(by="time")

    custom['rate'] = custom['rate'] * 1000
    custom['accumulated']  = (list(accumulate(custom['rate'])))

    bbbbbb = px.scatter(custom,x='time',y='rate')
    page.plotly_chart(bbbbbb)
    bbbbbbb = px.scatter(custom,x='time',y='accumulated')
    page.plotly_chart(bbbbbbb)


    lending_names = lending['name']
    
    NAME_LENDING = page.selectbox("Lending Token", lending_names, index = 1,key = random.randint(1, 100))
    page.write(lending_names)

    custom_lending = requests.get(f"https://ftx.com/api/spot_margin/history?coin={NAME_LENDING}&start_time=960368456&end_time=1854597556").json()

    custom_lending = pd.DataFrame(custom_lending['result'])
    custom_lending['rate'] = custom_lending['rate'].astype(float)
    custom_lending['time'] =  pd.to_datetime(custom_lending['time'])
    custom_lending = custom_lending.sort_values(by="time", ascending=True)

    custom_lending['accumulated']  = (list(accumulate(custom_lending['rate'] * custom_lending['size'])))

    custom_lending['rate'] = custom_lending['rate'] * 24 * 36500
    page.write(custom_lending)
    bbbbbb = px.scatter(custom_lending,x='time',y='rate')
    page.plotly_chart(bbbbbb)

    bbbbbbbb = px.bar(custom_lending,x='time',y='size')
    page.plotly_chart(bbbbbbbb)
    bbbbbbb = px.scatter(custom_lending,x='time',y='accumulated')
    page.plotly_chart(bbbbbbb)