import time
import logging
from web3 import Web3
from web3.exceptions import TransactionNotFound
from hexbytes import HexBytes
from cryptography.fernet import Fernet
import requests
import json
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import math
from itertools import chain

TIMEOUT = 120
POLL_LATENCY = 0.2

# while True:


        

st.write("Select Network & Chain ID")
chain_list = pd.DataFrame(
    {
        "chain_id": [1, 56, 137, 10, 42161, 100, 43114, 250],
        "chain": [
            "(ETH)",
            "(BSC)",
            "(MATIC)",
            "(OETH)",
            "(AETH)",
            "(xDAI)",
            "(AVAX)",
            "(FTM)",
        ],
    },
    index=[
        "Ethereum",
        "Binance Smart Chain",
        "Polygon",
        "Optimism",
        "Arbitrum",
        "Gnosis Chain",
        "Avalanche",
        "Fantom",
    ],
)
st.dataframe(chain_list)


chain_id = st.selectbox(
    "chain_id", ["1", "10", "56", "100", "137", "42161", "43114", "250"], key = 12
)
st.write("chain_id =" + chain_id)


healthcheck = requests.get(f"https://api.1inch.io/v4.0/{chain_id}/healthcheck")
healthcheck = json.loads(healthcheck.text)
healthcheck = pd.DataFrame.from_dict(healthcheck, orient="index")
st.write("HealthCheck RQ")
st.dataframe(healthcheck)

tokens_list = requests.get(f"https://api.1inch.io/v4.0/{chain_id}/tokens")
tokens_list = json.loads(tokens_list.text)
tokens_list = [tokens_list["tokens"][x] for x in tokens_list["tokens"]]
symbol_list = [elem["symbol"] for elem in tokens_list]
st.write("Tokens List")

st.dataframe(tokens_list)

# button here for manual input or not....
agree = st.checkbox("Manual Address Input?")
address_of_said_tokenIN = "null"
address_of_said_tokenOUT = "null"
decimal_of_said_tokenIN = 0
decimal_of_said_tokenOUT = 0


if agree:
    st.write("noswag")
    token_IN_test = st.text_input("manually addy in", address_of_said_tokenIN)
    st.write(token_IN_test)
    address_of_said_tokenIN = token_IN_test

    token_OUT_test = st.text_input("manually addy out", address_of_said_tokenOUT)
    st.write(token_OUT_test)
    address_of_said_tokenOUT = token_OUT_test
    decimal_of_said_tokenIN = st.number_input("decimal_of_said_tokenIN", value=18)
    # st.write(config_p_key)
    decimal_of_said_tokenOUT = st.number_input("decimal_of_said_tokenOUT", value=6)
    # st.write(config_rpc)
else:

    st.write("Great!")
    tokens_list = pd.DataFrame(tokens_list)

    tokenIN = "MATIC"

    tokenIN = st.selectbox("tokenIN", tokens_list['symbol'], index=5)
    address_of_said_tokenIN = tokens_list.set_index("symbol").loc[tokenIN]["address"]
    st.write(address_of_said_tokenIN)

    decimal_of_said_tokenIN = tokens_list.set_index("symbol").loc[tokenIN]["decimals"]
    st.write(decimal_of_said_tokenIN)
    tokenOUT = "USDC"

    tokenOUT = st.selectbox("tokenOUT", tokens_list['symbol'], index=10 )
    address_of_said_tokenOUT = tokens_list.set_index("symbol").loc[tokenOUT]["address"]
    st.write(address_of_said_tokenOUT)

    decimal_of_said_tokenOUT = tokens_list.set_index("symbol").loc[tokenOUT]["decimals"]
    st.write(decimal_of_said_tokenOUT)









number_unformat = st.number_input("amt_in",
    min_value=0.00001,
    max_value=5.0,
    step=1e-6,
    format="%.5f")
st.write(number_unformat)
DecimalFix = int(math.pow(10, decimal_of_said_tokenIN) * number_unformat)


url_swapToken_p1 = f"https://api.1inch.io/v4.0/{chain_id}/quote?fromTokenAddress="
url_swapToken_p2 = "{}&toTokenAddress={}&amount={}".format(
    address_of_said_tokenIN, address_of_said_tokenOUT, DecimalFix
)
url_swapToken_p3 = url_swapToken_p1 + url_swapToken_p2


token_return = requests.get(url_swapToken_p3)
token_return = json.loads(token_return.text)

amount_toToken = int(token_return["toTokenAmount"])

amount_toToken_correct = (amount_toToken) / (10 ** decimal_of_said_tokenOUT)



rate1 = number_unformat / amount_toToken_correct
rate2 = amount_toToken_correct / number_unformat



qq = {"i": [], "number_unformat": [], "rate2": []}
df2 = pd.DataFrame(qq)


i = 0

start_range = number_unformat

end_range = st.number_input("end range of quote",
    min_value=0.0001,
    max_value=5.0,
    step=1e-6,
    format="%.5f")
st.write(end_range)

i_max = st.number_input("how many quotes to check?", min_value=None, max_value=None, value=5)
st.write(i_max)

ping_size = (end_range - start_range) / i_max
DecimalFix = int(math.pow(10, decimal_of_said_tokenIN) * number_unformat)



DecimalFix = int(math.pow(10, decimal_of_said_tokenIN) * number_unformat)

# def get_quote(DecimalFix, address_of_said_tokenIN, address_of_said_tokenOUT, decimal_of_said_tokenIN, decimal_of_said_tokenOUT):
while i < i_max:
    DecimalFix1 = int(math.pow(10, decimal_of_said_tokenIN) * number_unformat)
    url_swapToken_p1 = f"https://api.1inch.io/v4.0/{chain_id}/quote?fromTokenAddress="
    url_swapToken_p2 = "{}&toTokenAddress={}&amount={}".format(
        address_of_said_tokenIN, address_of_said_tokenOUT, DecimalFix1
    )
    url_swapToken_p3 = url_swapToken_p1 + url_swapToken_p2
    # st.write(url_swapToken_p3)
    token_return = requests.get(url_swapToken_p3)
    token_return = json.loads(token_return.text)
    amount_toToken = int(token_return["toTokenAmount"])
    amount_toToken_correct = (amount_toToken) / (10 ** decimal_of_said_tokenOUT)
    rate1 = number_unformat / amount_toToken_correct
    rate2 = amount_toToken_correct / number_unformat
    l1 = requests.get(url_swapToken_p3)
    l2 = json.loads(l1.text)
    number_unformat = number_unformat + ping_size
    df2.loc[i] = [i, number_unformat, rate2]
    i = i + 1
    l1 = requests.get(url_swapToken_p3)
    l2 = json.loads(l1.text)

    actual = l2["protocols"]
    actual = list(chain(*actual))
    series = {
        "hop_num": [],
        "name": [],
        "toTokenAddress": [],
        "fromTokenAddress": [],
        "part": [],
    }
    for hop, item in enumerate(actual):
        for path in item:
            series["hop_num"].append(hop)
            series["name"].append(path["name"])
            series["toTokenAddress"].append(path["toTokenAddress"])
            series["fromTokenAddress"].append(path["fromTokenAddress"])
            series["part"].append(path["part"])
    final = pd.DataFrame.from_dict(series)

    tokens_list = pd.DataFrame(tokens_list)

    right_on_merger = tokens_list.merge(
        final, left_on="address", right_on="toTokenAddress"
    )

    names = {"symbol": "symbol_t"}

    left_on_merger = tokens_list.merge(
        final, left_on="address", right_on="fromTokenAddress"
    )

    namez = {"symbol": "symbol_f"}

    filteredDfL = left_on_merger[["symbol", "hop_num", "name_y", "part"]]
    filteredDfL = filteredDfL.rename(columns=namez)

    filteredDfR = right_on_merger[["symbol", "hop_num", "name_y", "part"]]
    filteredDfR = filteredDfR.rename(columns=names)

    second_last = filteredDfR.merge(filteredDfL)

    second_last["path"] = (
        second_last["symbol_f"]
        + "-"
        + second_last["symbol_t"]
        + ":"
        + second_last["name_y"]
    )

    Final_Path = second_last[["hop_num", "part", "path"]]

    Final_namez = {"name_y": "Liquidity_Source"}
    Final_Path = Final_Path.rename(columns=Final_namez)

st.write(Final_Path)




df2['Token_In_Amount'] = df2['number_unformat']
df2['Rate'] = df2['rate2'] 
df2['Token Out Amount'] = df2['Rate'] * df2['Token_In_Amount']
df2 = df2.drop(columns=['rate2', 'number_unformat']) 

st.write(df2)

Final_Path = px.line(
    df2,  # this is the dataframe you are trying to plot
    x="Token_In_Amount",
    y="Rate"
)
st.plotly_chart(Final_Path)
Final_Path = px.bar(
    df2,  # this is the dataframe you are trying to plot
    x="Token_In_Amount",
    y="Rate"
)






swap_chain = chain_id
swap_fromTokenAddress = address_of_said_tokenIN
#  "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
swap_toTokenAddress = address_of_said_tokenOUT
# "0x2791bca1f2de4661ed88a30c99a7a9449aa84174"
swap_amount = DecimalFix
# 10000000000000
swap_fromAddress = st.text_input("swap_fromAddress", "0xdF2D2F76E8E8827f92814E49e7D95Fc1e33E4148")
# ?"0xdF2D2F76E8E8827f92814E49e7D95Fc1e33E4148"
swap_slippage = st.number_input('slipage', min_value=None, max_value=None, value=1)
    # 1,5,10)

# pull = "https://api.1inch.io/v4.0/10/swap?fromTokenAddress=0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE&toTokenAddress=0x7F5c764cBc14f9669B88837ca1490cCa17c31607&amount=1000000000000&fromAddress=0xdF2D2F76E8E8827f92814E49e7D95Fc1e33E4148&slippage=1"
pull_build = (f"https://api.1inch.io/v4.0/{swap_chain}/swap?fromTokenAddress={swap_fromTokenAddress}&toTokenAddress={swap_toTokenAddress}&amount={swap_amount}&fromAddress={swap_fromAddress}&slippage={swap_slippage}")
# st.write(pull_build)




swap_full_json = requests.get(pull_build)
swap_full_json = json.loads(swap_full_json.text)
# st.write(swap_full_json)
swap_fromToken = (swap_full_json['fromToken'])
swap_fromToken_symbol = (swap_fromToken['symbol'])
swap_fromToken_name = (swap_fromToken['name'])
swap_fromToken_decimals = int(swap_fromToken['decimals'])
swap_fromToken_address = (swap_fromToken['address'])


swap_toToken = (swap_full_json['toToken'])
swap_toToken_symbol = (swap_toToken['symbol'])
swap_toToken_name = (swap_toToken['name'])
swap_toToken_decimals = int(swap_toToken['decimals'])
swap_toToken_address = (swap_toToken['address'])




swap_tofromTokenAmount = int(swap_full_json['fromTokenAmount'])
swap_tofromTokenAmount_decimal_adjusted = (swap_tofromTokenAmount) / (10 ** swap_fromToken_decimals)
swap_toTokenAmount = int(swap_full_json['toTokenAmount'])
swap_toTokenAmount_decimal_adjusted = (swap_toTokenAmount) / (10 ** swap_toToken_decimals)


inv_rate = swap_tofromTokenAmount_decimal_adjusted / swap_toTokenAmount_decimal_adjusted
rate = swap_toTokenAmount_decimal_adjusted / swap_tofromTokenAmount_decimal_adjusted


tx_data = (swap_full_json['tx'])



tx_data_from = (tx_data['from'])
tx_data_to = (tx_data['to'])
tx_data_data = (tx_data['data'])
tx_data_value = int(tx_data['value'])
tx_data_gas = int(tx_data['gas'])
tx_data_gasPrice = int(tx_data['gasPrice'])
gas_cost_native = tx_data_gas * tx_data_gasPrice
gas_cost_eth = gas_cost_native / (10 ** 18)
gas_cost_usd = gas_cost_eth * rate





swap_chain2 = chain_id

swap_fromTokenAddress2 = address_of_said_tokenOUT
#  st.selectbox("")
# "0x2791bca1f2de4661ed88a30c99a7a9449aa84174"
swap_toTokenAddress2 = address_of_said_tokenIN
#  "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
swap_amount2 = swap_toTokenAmount
swap_fromAddress2 = st.text_input("swap_fromAddress", "0x8fC1151dD92aB093EF0EB7cb144D573592510cAA")
# "0x8fC1151dD92aB093EF0EB7cb144D573592510cAA"
swap_slippage2 = 1

# pull2 = "https://api.1inch.io/v4.0/10/swap?fromTokenAddress=0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE&toTokenAddress=0x7F5c764cBc14f9669B88837ca1490cCa17c31607&amount=1000000000000&fromAddress=0xdF2D2F76E8E8827f92814E49e7D95Fc1e33E4148&slippage=1"
pull_build2 = (f"https://api.1inch.io/v4.0/{swap_chain2}/swap?fromTokenAddress={swap_fromTokenAddress2}&toTokenAddress={swap_toTokenAddress2}&amount={swap_amount2}&fromAddress={swap_fromAddress2}&slippage={swap_slippage2}")
# st.write(pull_build2)




swap_full_json2 = requests.get(pull_build2)
swap_full_json2 = json.loads(swap_full_json2.text)
# st.write(swap_full_json2)

swap_fromToken2 = (swap_full_json2['fromToken'])
swap_fromToken_symbol2 = (swap_fromToken2['symbol'])
swap_fromToken_name2 = (swap_fromToken2['name'])
swap_fromToken_decimals2 = int(swap_fromToken2['decimals'])
swap_fromToken_address2 = (swap_fromToken2['address'])


swap_toToken2 = (swap_full_json2['toToken'])
swap_toToken_symbo2 = (swap_toToken2['symbol'])
swap_toToken_name2 = (swap_toToken2['name'])
swap_toToken_decimals2 = int(swap_toToken2['decimals'])
swap_toToken_address2 = (swap_toToken2['address'])




swap_tofromTokenAmount2 = int(swap_full_json2['fromTokenAmount'])
swap_tofromTokenAmount_decimal_adjusted2 = (swap_tofromTokenAmount2) / (10 ** swap_fromToken_decimals2)
swap_toTokenAmount2 = int(swap_full_json2['toTokenAmount'])
swap_toTokenAmount_decimal_adjusted2 = (swap_toTokenAmount2) / (10 ** swap_toToken_decimals2)

inv_rate2 = swap_tofromTokenAmount_decimal_adjusted2 / swap_toTokenAmount_decimal_adjusted2
rate2 = swap_toTokenAmount_decimal_adjusted2 / swap_tofromTokenAmount_decimal_adjusted2


tx_data2 = (swap_full_json2['tx'])



tx_data_from2 = (tx_data2['from'])
tx_data_to2 = (tx_data2['to'])
tx_data_data2 = (tx_data2['data'])
tx_data_value2 = int(tx_data2['value'])
tx_data_gas2 = int(tx_data2['gas'])
tx_data_gasPrice2 = int(tx_data2['gasPrice'])
gas_cost_native2 = tx_data_gas2 * tx_data_gasPrice2
gas_cost_eth2 = gas_cost_native2 / (10 ** 18)
gas_cost_usd2 = gas_cost_eth2 * rate2


st.write(gas_cost_usd,gas_cost_usd2)
# st.write("swap_toTokenAmount2",swap_toTokenAmount2, "swap_amount", swap_amount, "gas_cost_native2" ,gas_cost_native2, "gas_cost_native",gas_cost_native)


# bepositive_to_swap = swap_toTokenAmount2 - swap_amount - gas_cost_native2 - gas_cost_native
# og input, last leg output, gas, gas
# print(gas_cost_native)
st.write('buy')
st.write("from", tokenIN + "to", tokenOUT)
st.write("from",swap_tofromTokenAmount_decimal_adjusted)
st.write("to",swap_toTokenAmount_decimal_adjusted)

st.write("inv_rate",inv_rate)
st.write("rate",rate)
# st.write(bepositive_to_swap)
st.write("sell")
st.write("from",tokenOUT, "to",
 tokenIN)
st.write("from",swap_tofromTokenAmount_decimal_adjusted2)
st.write("to",swap_toTokenAmount_decimal_adjusted2)
st.write("inv_rate2",inv_rate2)
st.write("rate2",rate2)


prof = (float(swap_toTokenAmount_decimal_adjusted2) - float(swap_tofromTokenAmount_decimal_adjusted))
st.write("profit",prof)





# https://poly-rpc.gateway.pokt.network",
#     }

leg1 = {

}


config = leg1
# st.write(leg1)
leg2 = {

}


config2 = leg2
# st.write(leg2)
class Web3Extension:
    def __init__(self, config):
        self.web3 = Web3(Web3.HTTPProvider(config.get('endpoint')))
        self.user_address = self.checksum(config.get('user_address', None))
        self.private_key = config.get('private_key', None)

    def checksum(self, address):
        if not address:
            logging.debug('Address is None, skipping checksum.')
            return None
        if self.web3.isAddress(address):
            return self.web3.toChecksumAddress(address)
        return address

    def to_wei(self, val):
        return int(self.web3.toWei(val, 'ether'))

    def from_wei(self, val):
        return float(self.web3.fromWei(val, 'ether'))

    def get_provider_uri(self):
        return self.web3.provider.endpoint_uri

    def get_block(self, identifier):
        return self.web3.eth.get_block(identifier)

    def get_block_time(self, identifier):
        return self.web3.eth.get_block(identifier).timestamp

    def get_latest_block(self):
        return self.web3.eth.get_block('latest')

    def get_address_nonce(self):
        assert self.user_address is not None, 'User address not initialized.'
        return self.web3.eth.get_transaction_count(self.user_address)

    def get_transaction(self, tx_hash):
        return self.web3.eth.get_transaction(tx_hash)

    def _sign_transaction(self, transaction, private_key):
        return self.web3.eth.account.sign_transaction(transaction, private_key)

    def _send_raw_transaction(self, signed_tx):
        raw_tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.web3.toHex(raw_tx_hash)  # tx_hash in hexa

    def build_transaction(self, to, value, gas, gas_price, data=None):
        assert self.user_address is not None, 'User address not initialized.'
        tx = {
            'from': self.checksum(self.user_address),
            'nonce': self.get_address_nonce(),
            'to': self.checksum(to),
            'value': value,
            'gas': gas,
            'gasPrice': gas_price,
        }
        if data is not None:
            tx.update({'data': data})
        return tx

    def sign_and_send(self, transaction):
        assert self.private_key is not None, 'Private key unavailable.'
        signed_tx = self._sign_transaction(transaction, self.private_key)
        return self._send_raw_transaction(signed_tx)

    def get_transaction_receipt(self, tx_hash, wait=False, timeout=TIMEOUT, poll_latency=POLL_LATENCY):
        try:
            if wait:
                return self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout, poll_latency)
            return self.web3.eth.get_transaction_receipt(tx_hash)
        except TransactionNotFound:
            return {"transactionHash": HexBytes(tx_hash), "blockNumber": -1, 'status': -1}

bepositive_to_swap11 = st.button("swap1")
if bepositive_to_swap11:
    W3 = Web3Extension(config)
    tx = W3.build_transaction(to=tx_data_to, value=tx_data_value, gas=tx_data_gas, gas_price=tx_data_gasPrice, data=tx_data_data)
    st.write(tx)
    resp1 = W3.sign_and_send(transaction=tx)
    st.write('https://optimistic.etherscan.io/tx/'+ resp1)


bepositive_to_swap22 = st.button("swap2")
if bepositive_to_swap22:

    W32 = Web3Extension(config = config2)
    tx2 = W32.build_transaction(to=tx_data_to2, value=tx_data_value2, gas=tx_data_gas2, gas_price=tx_data_gasPrice2, data=tx_data_data2)
    st.write(tx2)
    resp2 = W32.sign_and_send(transaction=tx2)
    st.write('https://optimistic.etherscan.io/tx/'+ resp2)
# else:
#     st.write("leg1fail")



# if bepositive_to_swap:


# # else:
# #     st.write("leg2fail")

# # st.write("yeet")
# time.sleep(2)

# time.sleep(0.42069)
#
# result1 = W3.get_transaction(tx_hash=resp1)
# print(result1)
# result2 = W32.get_transaction(tx_hash=resp2)
# print(result2)
