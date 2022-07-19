from ftx import ThreadedWebsocketManager
import os
import streamlit as st
def on_read(payload):
    st.write(payload)



# st.write(os.environ["API"])
# st.write(os.environ["SECRET"])

API = os.environ["API"] = '6lPPRFX1r4x_6ENY6GnhgYr3AdPv34x8Bc-MRH_V'
SECRET = os.environ["SECRET"] = 'OnQqs_nox4NS2OYm5z8ulXJ9rMkbOo5_nNwGe53V' 

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
    channel="fills",
    op="subscribe",
)
