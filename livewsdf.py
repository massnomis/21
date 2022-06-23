import asyncio
import websockets
import json
import streamlit as st
import pandas as pd
df = pd.DataFrame(columns = ['id', 'price', 'size', 'side', 'liquidation', 'time'])



placeholder1 = st.empty()
# for seconds in range(200):
# while True: 

 

async def consumer() -> None:
    async with websockets.connect("wss://ftx.com/ws/") as websocket:
        await websocket.send(
            json.dumps(
                {"op": "subscribe", "channel": "trades", "market": "BTC-PERP"}
            )
        )
        totalVol = 0
        async for message in websocket:
            message = json.loads(message)
            if message["type"] == "update":
                result = message["data"]
                for record in result:
                    totalVol += record["size"] * record["price"]
                global df
                while True:
                    with placeholder1.container():
                        df = df.append(result, ignore_index=True)
                        st.dataframe(df)

asyncio.run(consumer())

# import json

# import pandas as pd
# import websocket

# df = pd.DataFrame(columns=['foreignNotional', 'grossValue', 'homeNotional', 'price', 'side',
#                            'size', 'symbol', 'tickDirection', 'timestamp', 'trdMatchID'])


# def on_message(ws, message):
#     msg = json.loads(message)
#     print(msg)
#     global df
#     # `ignore_index=True` has to be provided, otherwise you'll get
#     # "Can only append a Series if ignore_index=True or if the Series has a name" errors
#     df = df.append(msg, ignore_index=True)


# def on_error(ws, error):
#     print(error)


# def on_close(ws):
#     print("### closed ###")


# def on_open(ws):
#     return


# if __name__ == "__main__":
#     ws = websocket.WebSocketApp("wss://www.bitmex.com/realtime?subscribe=trade:XBTUSD",
#                                 on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
#     ws.run_forever()
