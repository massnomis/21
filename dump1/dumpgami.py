

import json
import requests
import logging
from web3 import Web3
from web3.exceptions import TransactionNotFound
from hexbytes import HexBytes
from cryptography.fernet import Fernet
import requests
import json
import streamlit as st
# TIMEOUT = 120
# POLL_LATENCY = 0.2
#


swap_chain = 10
swap_fromTokenAddress = ""
swap_toTokenAddress = ""
swap_amount = 100000000000000000000
label = "swap_fromTokenAddress"
swap_fromAddress = ""
swap_slippage = 1

title = st.text_input('Movie title', 'Life of Brian')
st.write('.', title)


pull_build = f"https://api.1inch.io/v4.0/{swap_chain}/swap?fromTokenAddress={swap_fromTokenAddress}&toTokenAddress={swap_toTokenAddress}&amount={swap_amount}&fromAddress={swap_fromAddress}&slippage={swap_slippage}"



# print(pull_build)

yes = swap_amount / 10 ** 18

#




swap_full_json = requests.get(pull_build)
swap_full_json = json.loads(swap_full_json.text)
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
# print(swap_toTokenAmount_decimal_adjusted)
inv_rate = swap_tofromTokenAmount_decimal_adjusted / swap_toTokenAmount_decimal_adjusted
rate = swap_toTokenAmount_decimal_adjusted / swap_tofromTokenAmount_decimal_adjusted
# print(rate)
# print(inv_rate)
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


#
# leg2 = {
#     "user_address": "",
#     "private_key": "",
#     "endpoint": "https://bsc-dataseed1.defibit.io",
# }
#
#
# config = leg2
#
# class Web3Extension:
#     def __init__(self, config):
#         self.web3 = Web3(Web3.HTTPProvider(config.get('endpoint')))
#         self.user_address = self.checksum(config.get('user_address', None))
#         self.private_key = config.get('private_key', None)
#
#     def checksum(self, address):
#         if not address:
#             logging.debug('Address is None, skipping checksum.')
#             return None
#         if self.web3.isAddress(address):
#             return self.web3.toChecksumAddress(address)
#         return address
#
#     def to_wei(self, val):
#         return int(self.web3.toWei(val, 'ether'))
#
#     def from_wei(self, val):
#         return float(self.web3.fromWei(val, 'ether'))
#
#     def get_provider_uri(self):
#         return self.web3.provider.endpoint_uri
#
#     def get_block(self, identifier):
#         return self.web3.eth.get_block(identifier)
#
#     def get_block_time(self, identifier):
#         return self.web3.eth.get_block(identifier).timestamp
#
#     def get_latest_block(self):
#         return self.web3.eth.get_block('latest')
#
#     def get_address_nonce(self):
#         assert self.user_address is not None, 'User address not initialized.'
#         return self.web3.eth.get_transaction_count(self.user_address)
#
#     def get_transaction(self, tx_hash):
#         return self.web3.eth.get_transaction(tx_hash)
#
#     def _sign_transaction(self, transaction, private_key):
#         return self.web3.eth.account.sign_transaction(transaction, private_key)
#
#     def _send_raw_transaction(self, signed_tx):
#         raw_tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
#         return self.web3.toHex(raw_tx_hash)  # tx_hash in hexa
#
#     def build_transaction(self, to, value, gas, gas_price, data=None):
#         assert self.user_address is not None, 'User address not initialized.'
#         tx = {
#             'from': self.checksum(self.user_address),
#             'nonce': self.get_address_nonce(),
#             'to': self.checksum(to),
#             'value': value,
#             'gas': gas,
#             'gasPrice': gas_price,
#         }
#         if data is not None:
#             tx.update({'data': data})
#         return tx
#
#     def sign_and_send(self, transaction):
#         assert self.private_key is not None, 'Private key unavailable.'
#         signed_tx = self._sign_transaction(transaction, self.private_key)
#         return self._send_raw_transaction(signed_tx)
#
#     def get_transaction_receipt(self, tx_hash, wait=False, timeout=TIMEOUT, poll_latency=POLL_LATENCY):
#         try:
#             if wait:
#                 return self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout, poll_latency)
#             return self.web3.eth.get_transaction_receipt(tx_hash)
#         except TransactionNotFound:
#             return {"transactionHash": HexBytes(tx_hash), "blockNumber": -1, 'status': -1}
#
#
# W3 = Web3Extension(config)
# tx = W3.build_transaction(to=tx_data_to, value=tx_data_value, gas=tx_data_gas, gas_price=tx_data_gasPrice, data=tx_data_data)
# # print(tx)
# resp = W3.sign_and_send(transaction=tx)
# print(resp)
# # result = W3.get_transaction(tx_hash=resp)
# # print(result)