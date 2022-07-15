

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

API = os.environ["API"] = 
SECRET = os.environ["SECRET"] =  

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
                if data['type'] == 'update':
                    st.write(data)
            
    return await data
# asyncio.run(handler())

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(handler())
