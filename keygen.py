# import json
# import requests
# df = requests.get('https://node-api.flipsidecrypto.com/api/v2/queries/a5898a28-b950-40b4-8677-1af86297f228/data/latest').json()


import streamlit as st
from web3.auto import w3

checkbox = st.checkbox('generate new address')
if checkbox:
    acct = w3.eth.account.create()
    addy = (acct.address)
    private_key = (acct.privateKey.hex()[2:])
    st.write('Your private key is: ')
    st.code(private_key)
    st.write('Your address is: ')
    st.code(addy)