import streamlit as st
import requests
import json
import pandas as pd
import math

from itertools import chain

import plotly.express as px



st.set_page_config(
   page_title="Ex-stream-ly Cool App",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)

st.write("Select Network & Chain ID")
chain_list = pd.DataFrame({'chain_id': [1, 56, 137, 10, 42161, 100, 43114, 250],
                   'chain': ['(ETH)','(BSC)','(MATIC)','(OETH)','(AETH)', '(xDAI)', '(AVAX)', '(FTM)']},
                  index=['Ethereum','Binance Smart Chain','Polygon', 'Optimism', 'Arbitrum', 'Gnosis Chain', 'Avalanche', 'Fantom'])
st.dataframe(chain_list)




chain_id = 137

chain_id = st.select_slider('chain_id',
                       [
                           '1','10','56','100','137','42161','43114', '250'
                       ]
                       )
st.write("chain_id =" + chain_id)






healthcheck = requests.get(f"https://api.1inch.io/v4.0/{chain_id}/healthcheck")
healthcheck = json.loads(healthcheck.text)
healthcheck = pd.DataFrame.from_dict(healthcheck, orient="index")
st.write("HealthCheck RQ")
st.dataframe(healthcheck)

tokens_list = requests.get(f"https://api.1inch.io/v4.0/{chain_id}/tokens")
tokens_list = json.loads(tokens_list.text)
tokens_list = [tokens_list['tokens'][x] for x in tokens_list['tokens']]
symbol_list = [elem["symbol"] for elem in tokens_list]
st.write("Tokens List")

st.dataframe(tokens_list)


tokens_list = pd.DataFrame(tokens_list)
Clean_Token_df = tokens_list

tokenIN = 'MATIC'

tokenIN = st.selectbox('tokenIN',
                       symbol_list
                       )
address_of_said_tokenIN = tokens_list.set_index("symbol").loc[tokenIN]["address"]
st.write(address_of_said_tokenIN)

decimal_of_said_tokenIN = tokens_list.set_index("symbol").loc[tokenIN]["decimals"]
st.write(decimal_of_said_tokenIN)
tokenOUT = 'USDC'

tokenOUT = st.selectbox('tokenOUT',
                       symbol_list
                       )
address_of_said_tokenOUT = tokens_list.set_index("symbol").loc[tokenOUT]["address"]
st.write(address_of_said_tokenOUT)

decimal_of_said_tokenOUT = tokens_list.set_index("symbol").loc[tokenOUT]["decimals"]
st.write(decimal_of_said_tokenOUT)


st.write("SWAPPA")

liq_sauce = requests.get(f"https://api.1inch.io/v4.0/{chain_id}/liquidity-sources")
liq_sauce = json.loads(liq_sauce.text)
liq_sauce = pd.json_normalize(liq_sauce, 'protocols',errors="ignore")

Clean_liq_df = liq_sauce
Clean_liq_df.drop(columns=['img','img_color'], axis=1, inplace=True)

st.write("liquidity sources")

st.dataframe(Clean_liq_df)

number_unformat = st.number_input('amt_in', min_value=None, max_value=None, value=1)
st.write(number_unformat)

DecimalFix = int(math.pow(10,decimal_of_said_tokenIN) * number_unformat)
st.write(DecimalFix)
st.write("""Test Swap""")


url_swapToken_p1 = (f"https://api.1inch.io/v4.0/{chain_id}/quote?fromTokenAddress=")
url_swapToken_p2 = '{}&toTokenAddress={}&amount={}'.format(address_of_said_tokenIN, address_of_said_tokenOUT, DecimalFix)
url_swapToken_p3 = url_swapToken_p1 + url_swapToken_p2
st.write(url_swapToken_p3)


token_return = requests.get(url_swapToken_p3)
token_return = json.loads(token_return.text)
amount_toToken = int(token_return['toTokenAmount'])

amount_toToken_correct = ((amount_toToken) / (10 ** decimal_of_said_tokenOUT))

st.write("token output")
st.write(amount_toToken_correct)

rate1 = number_unformat / amount_toToken_correct
rate2 = amount_toToken_correct / number_unformat

st.write("in/out rate")
st.write(rate1)
st.write("out/in rate")
st.write(rate2)

l1 = requests.get(url_swapToken_p3)
l2 = json.loads(l1.text)


actual = l2['protocols']
actual = list(chain(*actual))
series = {
    'hop_num': [],
    'name': [],
    'toTokenAddress': [],
    'fromTokenAddress': [],
    'part': []
}
for hop, item in enumerate(actual):
  for path in item:
    series['hop_num'].append(hop)
    series['name'].append(path['name'])
    series['toTokenAddress'].append(path['toTokenAddress'])
    series['fromTokenAddress'].append(path['fromTokenAddress'])
    series['part'].append(path['part'])
final = pd.DataFrame.from_dict(series)

tokens_list = pd.DataFrame(tokens_list)

right_on_merger = tokens_list.merge(final, left_on = 'address', right_on = 'toTokenAddress')

names = {"symbol": "symbol_t"}


left_on_merger = tokens_list.merge(final, left_on = 'address', right_on = 'fromTokenAddress')

namez = {"symbol": "symbol_f"}

filteredDfL = left_on_merger[["symbol", "hop_num", "name_y", "part"]]
filteredDfL = filteredDfL.rename(columns = namez)

filteredDfR = right_on_merger[["symbol", "hop_num", "name_y", "part"]]
filteredDfR = filteredDfR.rename(columns = names)

second_last = filteredDfR.merge(filteredDfL)

second_last['path'] = second_last['symbol_f'] + "-" + second_last['symbol_t'] + ":" + second_last['name_y']

Final_Path = second_last[["hop_num", "part", "path"]]

Final_namez = {"name_y": "Liquidity_Source"}
Final_Path = Final_Path.rename(columns = Final_namez)


st.dataframe(Final_Path)

Final_Path = px.bar(
    Final_Path, #this is the dataframe you are trying to plot
    x = "hop_num",
    y = "part",
    color = "path",
    # title = "<b>DIY / Choose your own adventure - Polygon Fees</b>",
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600
)

st.plotly_chart(Final_Path)

ordermap = requests.get(url_swapToken_p3)
ordermap = json.loads(ordermap.text)
ordermap = pd.json_normalize(ordermap, 'protocols',errors="ignore")

st.title('KYC')
st.camera_input('lol')
