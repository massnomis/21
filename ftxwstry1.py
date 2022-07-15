from ftx import ThreadedWebsocketManager
import os
import streamlit as st
def on_read(payload):
    print(payload)


os.environ['API'] = '6lPPRFX1r4x_6ENY6GnhgYr3AdPv34x8Bc-MRH_V'
os.environ['SECRET'] = 'OnQqs_nox4NS2OYm5z8ulXJ9rMkbOo5_nNwGe53V' 

# st.write(os.environ["API"])
# st.write(os.environ["SECRET"])

API = os.environ["API"]
SECRET = os.environ["SECRET"]

wsm = ThreadedWebsocketManager(API, SECRET)
wsm.start()

# Un-auth subscribe
# name = 'market_connection'
# wsm.start_socket(on_read, socket_name=name)
# wsm.subscribe(name, channel="ticker", op="subscribe", market="BTC/USDT")

# Auth subscribe
name = 'private_connection'
wsm.start_socket(on_read, socket_name=name)
wsm.login(socket_name=name)
wsm.subscribe(
    name,
    channel="orders",
    op="subscribe",
)
