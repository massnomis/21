from cgi import print_exception
import secrets
from symtable import Symbol
import ccxt
from git import AmbiguousObjectName
from more_itertools import side_effect
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import pandas as pd
import time
import json
import streamlit as st


ftx = ccxt.ftx()
api_key = st.text_input("API Key")
secret = st.text_input("Secret")
exchange = ccxt.ftx({
    'apiKey': "o-K3J3uWrgVg1XJoA7M7HTSkKhnNWuUDHkBv2vIx",
    'secret': "RILDuy61-zChmkfdFQ0s-G5jneevMbN8n5vvHhK0",
    'subaccount': "h"
})



symbol = 'CVX-PERP' 
side = 'buy'
amount = 1
price = 4.187
type = 'limit'


symbol = st.text_input('Enter symbol', value='CUSDT/USDT')
side = st.text_input('Enter side', value='buy')
amount = st.number_input('Enter amount', value=1)
price = st.number_input('Enter price', value=0.0208575)
type = st.text_input('Enter type', value='limit')

st.write(symbol,side,amount,price,type)

yes = st.checkbox('execute')

if yes:
    order = exchange.create_order(symbol, type, side, amount, price)
    st.write(order)

