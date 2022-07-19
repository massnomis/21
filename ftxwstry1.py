

# st.write(os.environ["API"])
# st.write(os.environ["SECRET"])



import asyncio
import websockets
import json
import time
# import auth
import hmac 
import streamlit as st
import pprint
import os
from decouple import config
import streamlit as st
def on_read(payload):
    st.write(payload)
import pandas as pd
placeholder = st.empty()
data_pd = pd.DataFrame()
sum_data = pd.DataFrame()

df = pd.DataFrame()
API = config("API")
SECRET = config("SECRET")

api_key = API
secret_key = SECRET
placeholder = st.empty()
async def handler():
    async with websockets.connect('wss://ftx.com/ws/') as ws:
        
        
        ts = int(time.time() * 1000)
        signature = hmac.new(secret_key.encode(), f'{ts}websocket_login'.encode(), 'sha256').hexdigest()
        auth = {'op': 'login', 'args': {'key': api_key,
                                    'sign': signature, 
                                    'time': ts
                                    }}
        await ws.send(json.dumps(auth))
        data = {'op': 'subscribe', 'channel': 'fills'}
        await ws.send(json.dumps(data))
        

        async for message in ws:
            
            data = json.loads(message)
            with placeholder:
                global data_pd
                global df
                global sum_data
                if data['type'] == 'update':
                    st.write(data)
                    data_pd = data['data']
                    data_pd = pd.DataFrame(data_pd, index=[0])
                    st.write(data_pd)
                    df = df.append(data_pd, ignore_index=False)
                    sum_data = df['size'].sum()
                    st.write(data,df,sum_data)

    return await data


# st.write(sum_data)

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
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(handler())
