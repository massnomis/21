import time
import logging
from web3 import Web3
from web3.exceptions import TransactionNotFound
from hexbytes import HexBytes
from cryptography.fernet import Fernet
import requests
import json
import pandas as pd
import math

from itertools import chain

import plotly.express as px
import streamlit as st
TIMEOUT = 120
POLL_LATENCY = 0.2
# something for the swap idk

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





chain_id = st.selectbox('chain_id',  [
                           '1','10','56','100','137','42161','43114', '250'
                       ])
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

# button here for manual input or not....
agree = st.checkbox('Manual Address Input?')
address_of_said_tokenIN = 'null'
address_of_said_tokenOUT = 'null'
decimal_of_said_tokenIN = 0
decimal_of_said_tokenOUT = 0


if agree:
    st.write("noswag")
    token_IN_test = st.text_input('manually addy in', address_of_said_tokenIN)
    st.write(token_IN_test)
    address_of_said_tokenIN = token_IN_test

    token_OUT_test = st.text_input('manually addy out', address_of_said_tokenOUT)
    st.write(token_OUT_test)
    address_of_said_tokenOUT = token_OUT_test

else:
    # address_of_said_tokenIN = token_IN_test
    # address_of_said_tokenOUT = token_OUT_test

    st.write('Great!')
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

number_unformat = st.number_input('amt_in', min_value=None, max_value=None, value=0.0001)
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
st.write(token_return)

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

# trigger = st.text_input('write yues to execute?', '...')
# st.write(':-)', trigger)
# flag = 'clear'
# st.write(flag)



# we have already, need to merge...


# chain_id
# address_of_said_tokenIN
# address_of_said_tokenOUT
# DecimalFix

# swap_chain = chain_id
# swap_fromTokenAddress = "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83"
# swap_toTokenAddress = "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1"
# swap_amount = 100

swap_chain = chain_id
token_IN_test = address_of_said_tokenIN
swap_fromTokenAddress = token_IN_test
# swap_toTokenAddress = swap_toTokenAddress
swap_toTokenAddress = address_of_said_tokenOUT
swap_amount = DecimalFix



# need to get user input for this one
swap_fromAddress = "0xdF2D2F76E8E8827f92814E49e7D95Fc1e33E4148"
swap_slippage = 1








pull_build = f'https://api.1inch.io/v4.0/{swap_chain}/swap?fromTokenAddress={swap_fromTokenAddress}&toTokenAddress={swap_toTokenAddress}&amount={swap_amount}&fromAddress={swap_fromAddress}&slippage={swap_slippage}'
# st.write(pull_build)
st.markdown("api endpoint [link](%s)" % pull_build)




swap_full_json = requests.get(pull_build)
swap_full_json = json.loads(swap_full_json.text)

st.write(swap_full_json)

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
gas_cost_native_fixed = gas_cost_native / (10 ** 18)
gas_cost_usd = gas_cost_native_fixed * rate




# st.write(gas_cost_native)








config = {
    "user_address": "0xdF2D2F76E8E8827f92814E49e7D95Fc1e33E4148",
    "private_key": "8be0c0f4ee5a83c99dc3dc8fcf12626511df62e1c443bb4aeef9bd46a64d7560",
    "endpoint": "https://xdai-rpc.gateway.pokt.network",
}




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

    def build_transaction(self, to, value, gas, gas_price, chain_id, data=None):
        assert self.user_address is not None, 'User address not initialized.'
        tx = {
            'from': self.checksum(self.user_address),
            'nonce': self.get_address_nonce(),
            'to': self.checksum(to),
            'value': value,
            'gas': gas,
            'chainId': chain_id,
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
trigger = st.checkbox('send tx?')
chain_id = int(chain_id)
if trigger:
    W3 = Web3Extension(config)
    tx = W3.build_transaction(to=tx_data_to, value=tx_data_value, gas=tx_data_gas, gas_price=tx_data_gasPrice, chain_id=chain_id, data=tx_data_data)
    resp1 = W3.sign_and_send(transaction=tx)
    st.write("sent")
    st.write(tx)
    # st.markdown(resp1)
    tx_data = f'https://blockscout.com/xdai/mainnet/tx/{resp1}'
    st.markdown("tx_data [link](%s)" % tx_data)

else:
    flag = "waiting..."
    st.write(flag)


