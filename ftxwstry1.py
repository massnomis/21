from ftx import ThreadedWebsocketManager
import os
import streamlit as st
def on_read(payload):
    print(payload)



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
