# import streamlit as st
# from websocket import create_connection
# import re
# ws = create_connection("wss://stream.binance.com/stream")
# pair = 'bnbusdt' #BNB-USDT
# ws.send('{"method":"SUBSCRIBE","params":["'+pair+'@aggTrade"],"id":1}')
# ws.recv()
# oldPrice = float(re.findall('"p":"([\d.]+)',ws.recv())[0])
# print(oldPrice)
# while(True):
# 	price = float(re.findall('"p":"([\d.]+)',ws.recv())[0])
# 	if (100 * (price-oldPrice)/oldPrice > 0.01):
# 		st.write(price)
# 	if price>oldPrice:
# 		oldPrice = price
# 		st.write(price)
#
# st.write(price)
import json
import requests
inverse_url_eth = ("https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&toTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&amount=300812911")
token_return = requests.get(inverse_url_eth)
token_return = json.loads(token_return.text)
amount_toToken = int(token_return['toTokenAmount'])
inverse_eth = ((amount_toToken) / (10 ** 16))
print(inverse_eth)