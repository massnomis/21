from eth_account.messages import encode_structured_data
from web3 import Web3
import requests
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
w3 = Web3(Web3.HTTPProvider("https://cloudflare-eth.com"))  
wallet_key = ""
chainId = 137
# lets build the predicate
contract_abi = [{"anonymous":"false","inputs":[{"indexed":"true","internalType":"address","name":"maker","type":"address"},{"indexed":"false","internalType":"uint256","name":"newNonce","type":"uint256"}],"name":"NonceIncreased","type":"event"},{"anonymous":"false","inputs":[{"indexed":"true","internalType":"address","name":"maker","type":"address"},{"indexed":"false","internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":"false","internalType":"uint256","name":"remainingRaw","type":"uint256"}],"name":"OrderCanceled","type":"event"},{"anonymous":"false","inputs":[{"indexed":"true","internalType":"address","name":"maker","type":"address"},{"indexed":"false","internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":"false","internalType":"uint256","name":"remaining","type":"uint256"}],"name":"OrderFilled","type":"event"},{"anonymous":"false","inputs":[{"indexed":"false","internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":"false","internalType":"uint256","name":"makingAmount","type":"uint256"}],"name":"OrderFilledRFQ","type":"event"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"LIMIT_ORDER_RFQ_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"LIMIT_ORDER_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"amount","type":"uint8"}],"name":"advanceNonce","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"targets","type":"address[]"},{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"and","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"target","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"arbitraryStaticCall","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"address","name":"makerAsset","type":"address"},{"internalType":"address","name":"takerAsset","type":"address"},{"internalType":"address","name":"maker","type":"address"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"address","name":"allowedSender","type":"address"},{"internalType":"uint256","name":"makingAmount","type":"uint256"},{"internalType":"uint256","name":"takingAmount","type":"uint256"},{"internalType":"bytes","name":"makerAssetData","type":"bytes"},{"internalType":"bytes","name":"takerAssetData","type":"bytes"},{"internalType":"bytes","name":"getMakerAmount","type":"bytes"},{"internalType":"bytes","name":"getTakerAmount","type":"bytes"},{"internalType":"bytes","name":"predicate","type":"bytes"},{"internalType":"bytes","name":"permit","type":"bytes"},{"internalType":"bytes","name":"interaction","type":"bytes"}],"internalType":"struct OrderMixin.Order","name":"order","type":"tuple"}],"name":"cancelOrder","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"orderInfo","type":"uint256"}],"name":"cancelOrderRFQ","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"address","name":"makerAsset","type":"address"},{"internalType":"address","name":"takerAsset","type":"address"},{"internalType":"address","name":"maker","type":"address"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"address","name":"allowedSender","type":"address"},{"internalType":"uint256","name":"makingAmount","type":"uint256"},{"internalType":"uint256","name":"takingAmount","type":"uint256"},{"internalType":"bytes","name":"makerAssetData","type":"bytes"},{"internalType":"bytes","name":"takerAssetData","type":"bytes"},{"internalType":"bytes","name":"getMakerAmount","type":"bytes"},{"internalType":"bytes","name":"getTakerAmount","type":"bytes"},{"internalType":"bytes","name":"predicate","type":"bytes"},{"internalType":"bytes","name":"permit","type":"bytes"},{"internalType":"bytes","name":"interaction","type":"bytes"}],"internalType":"struct OrderMixin.Order","name":"order","type":"tuple"}],"name":"checkPredicate","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract AggregatorV3Interface","name":"oracle1","type":"address"},{"internalType":"contract AggregatorV3Interface","name":"oracle2","type":"address"},{"internalType":"uint256","name":"spread","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"doublePrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"address","name":"target","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"eq","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"address","name":"makerAsset","type":"address"},{"internalType":"address","name":"takerAsset","type":"address"},{"internalType":"address","name":"maker","type":"address"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"address","name":"allowedSender","type":"address"},{"internalType":"uint256","name":"makingAmount","type":"uint256"},{"internalType":"uint256","name":"takingAmount","type":"uint256"},{"internalType":"bytes","name":"makerAssetData","type":"bytes"},{"internalType":"bytes","name":"takerAssetData","type":"bytes"},{"internalType":"bytes","name":"getMakerAmount","type":"bytes"},{"internalType":"bytes","name":"getTakerAmount","type":"bytes"},{"internalType":"bytes","name":"predicate","type":"bytes"},{"internalType":"bytes","name":"permit","type":"bytes"},{"internalType":"bytes","name":"interaction","type":"bytes"}],"internalType":"struct OrderMixin.Order","name":"order","type":"tuple"},{"internalType":"bytes","name":"signature","type":"bytes"},{"internalType":"uint256","name":"makingAmount","type":"uint256"},{"internalType":"uint256","name":"takingAmount","type":"uint256"},{"internalType":"uint256","name":"thresholdAmount","type":"uint256"}],"name":"fillOrder","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"info","type":"uint256"},{"internalType":"contract IERC20","name":"makerAsset","type":"address"},{"internalType":"contract IERC20","name":"takerAsset","type":"address"},{"internalType":"address","name":"maker","type":"address"},{"internalType":"address","name":"allowedSender","type":"address"},{"internalType":"uint256","name":"makingAmount","type":"uint256"},{"internalType":"uint256","name":"takingAmount","type":"uint256"}],"internalType":"struct OrderRFQMixin.OrderRFQ","name":"order","type":"tuple"},{"internalType":"bytes","name":"signature","type":"bytes"},{"internalType":"uint256","name":"makingAmount","type":"uint256"},{"internalType":"uint256","name":"takingAmount","type":"uint256"}],"name":"fillOrderRFQ","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"info","type":"uint256"},{"internalType":"contract IERC20","name":"makerAsset","type":"address"},{"internalType":"contract IERC20","name":"takerAsset","type":"address"},{"internalType":"address","name":"maker","type":"address"},{"internalType":"address","name":"allowedSender","type":"address"},{"internalType":"uint256","name":"makingAmount","type":"uint256"},{"internalType":"uint256","name":"takingAmount","type":"uint256"}],"internalType":"struct OrderRFQMixin.OrderRFQ","name":"order","type":"tuple"},{"internalType":"bytes","name":"signature","type":"bytes"},{"internalType":"uint256","name":"makingAmount","type":"uint256"},{"internalType":"uint256","name":"takingAmount","type":"uint256"},{"internalType":"address","name":"target","type":"address"}],"name":"fillOrderRFQTo","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"info","type":"uint256"},{"internalType":"contract IERC20","name":"makerAsset","type":"address"},{"internalType":"contract IERC20","name":"takerAsset","type":"address"},{"internalType":"address","name":"maker","type":"address"},{"internalType":"address","name":"allowedSender","type":"address"},{"internalType":"uint256","name":"makingAmount","type":"uint256"},{"internalType":"uint256","name":"takingAmount","type":"uint256"}],"internalType":"struct OrderRFQMixin.OrderRFQ","name":"order","type":"tuple"},{"internalType":"bytes","name":"signature","type":"bytes"},{"internalType":"uint256","name":"makingAmount","type":"uint256"},{"internalType":"uint256","name":"takingAmount","type":"uint256"},{"internalType":"address","name":"target","type":"address"},{"internalType":"bytes","name":"permit","type":"bytes"}],"name":"fillOrderRFQToWithPermit","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"address","name":"makerAsset","type":"address"},{"internalType":"address","name":"takerAsset","type":"address"},{"internalType":"address","name":"maker","type":"address"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"address","name":"allowedSender","type":"address"},{"internalType":"uint256","name":"makingAmount","type":"uint256"},{"internalType":"uint256","name":"takingAmount","type":"uint256"},{"internalType":"bytes","name":"makerAssetData","type":"bytes"},{"internalType":"bytes","name":"takerAssetData","type":"bytes"},{"internalType":"bytes","name":"getMakerAmount","type":"bytes"},{"internalType":"bytes","name":"getTakerAmount","type":"bytes"},{"internalType":"bytes","name":"predicate","type":"bytes"},{"internalType":"bytes","name":"permit","type":"bytes"},{"internalType":"bytes","name":"interaction","type":"bytes"}],"internalType":"struct OrderMixin.Order","name":"order","type":"tuple"},{"internalType":"bytes","name":"signature","type":"bytes"},{"internalType":"uint256","name":"makingAmount","type":"uint256"},{"internalType":"uint256","name":"takingAmount","type":"uint256"},{"internalType":"uint256","name":"thresholdAmount","type":"uint256"},{"internalType":"address","name":"target","type":"address"}],"name":"fillOrderTo","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"address","name":"makerAsset","type":"address"},{"internalType":"address","name":"takerAsset","type":"address"},{"internalType":"address","name":"maker","type":"address"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"address","name":"allowedSender","type":"address"},{"internalType":"uint256","name":"makingAmount","type":"uint256"},{"internalType":"uint256","name":"takingAmount","type":"uint256"},{"internalType":"bytes","name":"makerAssetData","type":"bytes"},{"internalType":"bytes","name":"takerAssetData","type":"bytes"},{"internalType":"bytes","name":"getMakerAmount","type":"bytes"},{"internalType":"bytes","name":"getTakerAmount","type":"bytes"},{"internalType":"bytes","name":"predicate","type":"bytes"},{"internalType":"bytes","name":"permit","type":"bytes"},{"internalType":"bytes","name":"interaction","type":"bytes"}],"internalType":"struct OrderMixin.Order","name":"order","type":"tuple"},{"internalType":"bytes","name":"signature","type":"bytes"},{"internalType":"uint256","name":"makingAmount","type":"uint256"},{"internalType":"uint256","name":"takingAmount","type":"uint256"},{"internalType":"uint256","name":"thresholdAmount","type":"uint256"},{"internalType":"address","name":"target","type":"address"},{"internalType":"bytes","name":"permit","type":"bytes"}],"name":"fillOrderToWithPermit","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"orderMakerAmount","type":"uint256"},{"internalType":"uint256","name":"orderTakerAmount","type":"uint256"},{"internalType":"uint256","name":"swapTakerAmount","type":"uint256"}],"name":"getMakerAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"orderMakerAmount","type":"uint256"},{"internalType":"uint256","name":"orderTakerAmount","type":"uint256"},{"internalType":"uint256","name":"swapMakerAmount","type":"uint256"}],"name":"getTakerAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"address","name":"target","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"gt","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"address","name":"makerAsset","type":"address"},{"internalType":"address","name":"takerAsset","type":"address"},{"internalType":"address","name":"maker","type":"address"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"address","name":"allowedSender","type":"address"},{"internalType":"uint256","name":"makingAmount","type":"uint256"},{"internalType":"uint256","name":"takingAmount","type":"uint256"},{"internalType":"bytes","name":"makerAssetData","type":"bytes"},{"internalType":"bytes","name":"takerAssetData","type":"bytes"},{"internalType":"bytes","name":"getMakerAmount","type":"bytes"},{"internalType":"bytes","name":"getTakerAmount","type":"bytes"},{"internalType":"bytes","name":"predicate","type":"bytes"},{"internalType":"bytes","name":"permit","type":"bytes"},{"internalType":"bytes","name":"interaction","type":"bytes"}],"internalType":"struct OrderMixin.Order","name":"order","type":"tuple"}],"name":"hashOrder","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"increaseNonce","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"maker","type":"address"},{"internalType":"uint256","name":"slot","type":"uint256"}],"name":"invalidatorForOrderRFQ","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"address","name":"target","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"lt","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonce","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"makerAddress","type":"address"},{"internalType":"uint256","name":"makerNonce","type":"uint256"}],"name":"nonceEquals","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"targets","type":"address[]"},{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"or","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"orderHash","type":"bytes32"}],"name":"remaining","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"orderHash","type":"bytes32"}],"name":"remainingRaw","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32[]","name":"orderHashes","type":"bytes32[]"}],"name":"remainingsRaw","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"targets","type":"address[]"},{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"simulateCalls","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract AggregatorV3Interface","name":"oracle","type":"address"},{"internalType":"uint256","name":"inverseAndSpread","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"singlePrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"time","type":"uint256"}],"name":"timestampBelow","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]
contract = w3.eth.contract(address="0x94Bc2a1C732BcAd7343B25af48385Fe76E08734f", abi=contract_abi)

erc20_abi = [{"constant":"true","inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"false","inputs":[{"name":"_upgradedAddress","type":"address"}],"name":"deprecate","outputs":[],"payable":"false","stateMutability":"nonpayable","type":"function"},{"constant":"false","inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":"false","stateMutability":"nonpayable","type":"function"},{"constant":"true","inputs":[],"name":"deprecated","outputs":[{"name":"","type":"bool"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"false","inputs":[{"name":"_evilUser","type":"address"}],"name":"addBlackList","outputs":[],"payable":"false","stateMutability":"nonpayable","type":"function"},{"constant":"true","inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"false","inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":"false","stateMutability":"nonpayable","type":"function"},{"constant":"true","inputs":[],"name":"upgradedAddress","outputs":[{"name":"","type":"address"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"true","inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"true","inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"true","inputs":[],"name":"maximumFee","outputs":[{"name":"","type":"uint256"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"true","inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"false","inputs":[],"name":"unpause","outputs":[],"payable":"false","stateMutability":"nonpayable","type":"function"},{"constant":"true","inputs":[{"name":"_maker","type":"address"}],"name":"getBlackListStatus","outputs":[{"name":"","type":"bool"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"true","inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowed","outputs":[{"name":"","type":"uint256"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"true","inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"true","inputs":[{"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"false","inputs":[],"name":"pause","outputs":[],"payable":"false","stateMutability":"nonpayable","type":"function"},{"constant":"true","inputs":[],"name":"getOwner","outputs":[{"name":"","type":"address"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"true","inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"true","inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"false","inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":"false","stateMutability":"nonpayable","type":"function"},{"constant":"false","inputs":[{"name":"newBasisPoints","type":"uint256"},{"name":"newMaxFee","type":"uint256"}],"name":"setParams","outputs":[],"payable":"false","stateMutability":"nonpayable","type":"function"},{"constant":"false","inputs":[{"name":"amount","type":"uint256"}],"name":"issue","outputs":[],"payable":"false","stateMutability":"nonpayable","type":"function"},{"constant":"false","inputs":[{"name":"amount","type":"uint256"}],"name":"redeem","outputs":[],"payable":"false","stateMutability":"nonpayable","type":"function"},{"constant":"true","inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"true","inputs":[],"name":"basisPointsRate","outputs":[{"name":"","type":"uint256"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"true","inputs":[{"name":"","type":"address"}],"name":"isBlackListed","outputs":[{"name":"","type":"bool"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"false","inputs":[{"name":"_clearedUser","type":"address"}],"name":"removeBlackList","outputs":[],"payable":"false","stateMutability":"nonpayable","type":"function"},{"constant":"true","inputs":[],"name":"MAX_UINT","outputs":[{"name":"","type":"uint256"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"false","inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":"false","stateMutability":"nonpayable","type":"function"},{"constant":"false","inputs":[{"name":"_blackListedUser","type":"address"}],"name":"destroyBlackFunds","outputs":[],"payable":"false","stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_initialSupply","type":"uint256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint256"}],"payable":"false","stateMutability":"nonpayable","type":"constructor"},{"anonymous":"false","inputs":[{"indexed":"false","name":"amount","type":"uint256"}],"name":"Issue","type":"event"},{"anonymous":"false","inputs":[{"indexed":"false","name":"amount","type":"uint256"}],"name":"Redeem","type":"event"},{"anonymous":"false","inputs":[{"indexed":"false","name":"newAddress","type":"address"}],"name":"Deprecate","type":"event"},{"anonymous":"false","inputs":[{"indexed":"false","name":"feeBasisPoints","type":"uint256"},{"indexed":"false","name":"maxFee","type":"uint256"}],"name":"Params","type":"event"},{"anonymous":"false","inputs":[{"indexed":"false","name":"_blackListedUser","type":"address"},{"indexed":"false","name":"_balance","type":"uint256"}],"name":"DestroyedBlackFunds","type":"event"},{"anonymous":"false","inputs":[{"indexed":"false","name":"_user","type":"address"}],"name":"AddedBlackList","type":"event"},{"anonymous":"false","inputs":[{"indexed":"false","name":"_user","type":"address"}],"name":"RemovedBlackList","type":"event"},{"anonymous":"false","inputs":[{"indexed":"true","name":"owner","type":"address"},{"indexed":"true","name":"spender","type":"address"},{"indexed":"false","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":"false","inputs":[{"indexed":"true","name":"from","type":"address"},{"indexed":"true","name":"to","type":"address"},{"indexed":"false","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":"false","inputs":[],"name":"Pause","type":"event"},{"anonymous":"false","inputs":[],"name":"Unpause","type":"event"}]

# your addy goes here
makerAddress = Web3.toChecksumAddress("0xda19326733C370Bd43FD9a9Aa5A1ae94E0a8B6d4")
takerAddress = "0x0000000000000000000000000000000000000000"
makerAsset = Web3.toChecksumAddress("0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270")
takerAsset = Web3.toChecksumAddress("0x2791bca1f2de4661ed88a30c99a7a9449aa84174")
makingAmount = "100000000"
takingAmount = "100000000"

# maker asset contract
makerAssetContract = w3.eth.contract(address=makerAsset, abi=erc20_abi)
# taker asset contract
takerAssetContract = w3.eth.contract(address=takerAsset, abi=erc20_abi)

makerAssetData = makerAssetContract.encodeABI(fn_name="transferFrom", args=[makerAddress, takerAddress, int(makingAmount)])
takerAssetData = takerAssetContract.encodeABI(fn_name="transferFrom", args=[takerAddress, makerAddress, int(takingAmount)])

getMakerAmount = contract.encodeABI(fn_name="getMakerAmount", args=[int(makingAmount), int(takingAmount), 0])
getMakerAmount = getMakerAmount[:-64]
getTakerAmount = contract.encodeABI(fn_name="getTakerAmount", args=[int(makingAmount), int(takingAmount), 0])
getTakerAmount = getTakerAmount[:-64]

# contract encode abi with the timestamp below function and the current time + 180 seconds
predicate = contract.encodeABI(fn_name="timestampBelow", args=[w3.eth.getBlock('latest').timestamp + 180])

order_data = {
    "makerAsset": makerAsset,
    "takerAsset": takerAsset,
    "maker": makerAddress,
    "allowedSender": "0x0000000000000000000000000000000000000000",
    "receiver": "0x0000000000000000000000000000000000000000",
    "makingAmount": makingAmount,
    "takingAmount": takingAmount,
    "makerAssetData": "0x", #str(makerAssetData),
    "takerAssetData": "0x", #str(takerAssetData),
    "getMakerAmount": getMakerAmount,
    "getTakerAmount": getTakerAmount,
    "predicate": predicate,
    "permit": "0x",
    "interaction": "0x",
    "salt": "1", # random number to make the order unique
}

order_types = [
    {"name": "salt", "type": "uint256"},
    {"name": "makerAsset", "type": "address"},
    {"name": "takerAsset", "type": "address"},
    {"name": "maker", "type": "address"},
    {"name": "receiver", "type": "address"},
    {"name": "allowedSender", "type": "address"},
    {"name": "makingAmount", "type": "uint256"},
    {"name": "takingAmount", "type": "uint256"},
    {"name": "makerAssetData", "type": "bytes"},
    {"name": "takerAssetData", "type": "bytes"},
    {"name": "getMakerAmount", "type": "bytes"},
    {"name": "getTakerAmount", "type": "bytes"},
    {"name": "predicate", "type": "bytes"},
    {"name": "permit", "type": "bytes"},
    {"name": "interaction", "type": "bytes"},
]
def fix_data_types(data, types):
    """
    Order data values are all strings as this is what the API expects. This function fixes their types for
    encoding purposes.
    """
    fixed_data = {}
    for dictionary in types:
        if "bytes" in dictionary["type"]:
            fixed_data[dictionary["name"]] = (Web3.toBytes(hexstr=data[dictionary["name"]]))
        elif "int" in dictionary["type"]:
            fixed_data[dictionary["name"]] = int(data[dictionary["name"]])
        else:
            fixed_data[dictionary["name"]] = data[dictionary["name"]]
    return fixed_data
eip712_data = {
    "primaryType": "Order",
    "types": {
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"},
            {"name": "chainId", "type": "uint256"},
            {"name": "verifyingContract", "type": "address"},
        ],
        "Order": order_types
    },
    "domain": {
        "name": "1inch Limit Order Protocol",
        "version": "2",
        "chainId": chainId,
        "verifyingContract": "0x94bc2a1c732bcad7343b25af48385fe76e08734f",
    },
    "message": fix_data_types(order_data, order_types),
}
encoded_message = encode_structured_data(eip712_data)
# st.json(encoded_message)
signed_message = w3.eth.account.sign_message(encoded_message, wallet_key)
false = False
limit_order = {
#     "signature": "0xaa5b823a665363a45a840c14acd5cb3428ee757f2db47316f34589c0c90b6693127a30ce589d9d9ece0edd9bd27f772856d40392a5f0b4770c97684226676df81c",
#     "orderHash": "0x48f9888da137bdb21e129abce279a83fc62ece03d20faf28ccb5c96ab46a870e",
#     "createDateTime": "2022-07-24T19:27:50.032Z",
#     "remainingMakerAmount": "100",
#     "makerBalance": "7234636",
#     "makerAllowance": "115792089237316195423570985008687907853269984665640564039457584007913129639935",
#     "data": {
"salt": "1284937370206",

"makerAsset": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
"takerAsset": "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270",
#   "getMakerAmount": "0xf4a215c300000000000000000000000000000000000000000000000000000000000000640000000000000000000000000000000000000000000000000000accdd281e000",
#   "getTakerAmount": "0x296637bf00000000000000000000000000000000000000000000000000000000000000640000000000000000000000000000000000000000000000000000accdd281e000",
"makerAssetData": "0x",
"takerAssetData": "0x",
"makingAmount": "100",
"takingAmount": "190000000000000",
"predicate": "0x961d5b1e000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000000000000000200000000000000000000000094bc2a1c732bcad7343b25af48385fe76e08734f00000000000000000000000094bc2a1c732bcad7343b25af48385fe76e08734f0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000044cf6fc6e30000000000000000000000008fc1151dd92ab093ef0eb7cb144d573592510caa000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002463592c2b0000000000000000000000000000000000000000000000000000000062e6d79a00000000000000000000000000000000000000000000000000000000",
"permit": "0x",

"interaction": "0xf01ef4051130cc8871fa0c17024a6d62e379e8568fc1151dd92ab093ef0eb7cb144d573592510caa",
    #   "receiver": "0xf01ef4051130cc8871fa0c17024a6d62e379e856",
    #   "allowedSender": "0x0000000000000000000000000000000000000000",

    #   "maker": "0x8fc1151dd92ab093ef0eb7cb144d573592510caa"
    # },
    # "makerRate": "1900000000000.000000000000000000",
    # "takerRate": "5.26315E-13",
    # "isMakerContract": false
  }
  

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
TIMEOUT = 120
POLL_LATENCY = 0.2


leg2 = {
    "private_key": "",
    "user_address": "0xda19326733C370Bd43FD9a9Aa5A1ae94E0a8B6d4",
    "endpoint": "https://rpc-mainnet.matic.quiknode.pro",
}

config = leg2
tx_data_gas = 210000
tx_data_gasPrice = 40000000000
tx_data_value = '0x0'

import logging

from hexbytes import HexBytes
from web3 import Web3
from web3.exceptions import TransactionNotFound


class Web3Extension:
    def __init__(self, config):
        self.web3 = Web3(Web3.HTTPProvider(config.get("endpoint")))
        self.user_address = self.checksum(config.get("user_address", None))
        self.private_key = config.get("private_key", None)

    def checksum(self, address):
        if not address:
            logging.debug("Address is None, skipping checksum.")
            return None
        if self.web3.isAddress(address):
            return self.web3.toChecksumAddress(address)
        return address

    def to_wei(self, val):
        return int(self.web3.toWei(val, "ether"))

    def from_wei(self, val):
        return float(self.web3.fromWei(val, "ether"))

    def get_provider_uri(self):
        return self.web3.provider.endpoint_uri

    def get_block(self, identifier):
        return self.web3.eth.get_block(identifier)

    def get_block_time(self, identifier):
        return self.web3.eth.get_block(identifier).timestamp

    def get_latest_block(self):
        return self.web3.eth.get_block("latest")

    def get_address_nonce(self):
        assert self.user_address is not None, "User address not initialized."
        return self.web3.eth.get_transaction_count(self.user_address)

    def get_transaction(self, tx_hash):
        return self.web3.eth.get_transaction(tx_hash)

    def _sign_transaction(self, transaction, private_key):
        return self.web3.eth.account.sign_transaction(transaction, private_key)

    def _send_raw_transaction(self, signed_tx):
        raw_tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.web3.toHex(raw_tx_hash)  # tx_hash in hexa

    def build_transaction(self, to, value, gas, gas_price, chain_id, data=None):
        assert self.user_address is not None, "User address not initialized."
        tx = {
            "from": self.checksum(self.user_address),
            "nonce": self.get_address_nonce(),
            "to": self.checksum(to),
            "value": value,
            "gas": gas,
            "gasPrice": gas_price,
            "chainId": chain_id,
        }
        if data is not None:
            tx.update({"data": data})
        return tx

    def sign_and_send(self, transaction):
        assert self.private_key is not None, "Private key unavailable."
        signed_tx = self._sign_transaction(transaction, self.private_key)
        return self._send_raw_transaction(signed_tx)

    def get_transaction_receipt(
        self, tx_hash, wait=False, timeout=120, poll_latency=0.2
    ):
        try:
            if wait:
                return self.web3.eth.wait_for_transaction_receipt(
                    tx_hash, timeout, poll_latency
                )
            return self.web3.eth.get_transaction_receipt(tx_hash)
        except TransactionNotFound:
            return {
                "transactionHash": HexBytes(tx_hash),
                "blockNumber": -1,
                "status": -1,
            }


chain_id = 137
W3 = Web3Extension(config)

into_order = signed_message.signature.hex()
limitOrderSignature = into_order
makingAmount = 100
takingAmount = 0
thresholdAmount = 10

fill_limit_order = {"order": order_data, "signature": into_order,  "makingAmount":makingAmount,  "takingAmount":takingAmount, "thresholdAmount":thresholdAmount}
fill_limit_order = fill_limit_order


addy_poly = "0x94bc2a1c732bcad7343b25af48385fe76e08734f"
tx_data_to = addy_poly
tx_data_data = fill_limit_order


tx = W3.build_transaction(to=tx_data_to, value=tx_data_value, gas=tx_data_gas, gas_price=tx_data_gasPrice, data=tx_data_data, chain_id=chain_id)
print(tx)
resp = W3.sign_and_send(transaction=tx)
print(resp)
result = W3.get_transaction(tx_hash=resp)
print(result)
