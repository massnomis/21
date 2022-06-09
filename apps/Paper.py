
from itertools import accumulate
import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import random
def app():   
    page = st.container()

    tftkn = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/9e36dbae-40e6-4443-a54a-b7166e78ed71/data/latest')
    page.markdown('https://app.truefi.io/lend')
    llal = px.line(tftkn,x='DAYZ',y='PRICE', color = 'TFTOKEN',render_mode="SVG")
    page.plotly_chart(llal)
    page.write(tftkn)
    mmm = px.line(tftkn,x='DAYZ',y='APY', color = 'TFTOKEN',render_mode="SVG")
    page.plotly_chart(mmm)
