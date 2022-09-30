# import streamlit, json and pandas
# pull from https://raw.githubusercontent.com/DefiLlama/chainlist/main/constants/extraRpcs.json and st.code it
# then, make a dropdown menu with the chain names and st.code the rpc
# then, make a button that says "add to metamask" and when clicked, it adds the rpc to metamask
# 
from urllib import response
import streamlit as st
import json
import requests
import pandas as pd
extrarpsc = requests.get('https://raw.githubusercontent.com/DefiLlama/chainlist/main/constants/extraRpcs.json').json()
st.write(extrarpsc)

chainids = requests.get('https://raw.githubusercontent.com/DefiLlama/chainlist/main/constants/chainIds.js')
chainids = chainids.text
# chainids = json.loads(chainids)

chainids = chainids[chainids.find('{'):chainids.find(';')]
# take this str and make it a dict

# take this dict and make it a df
chainids = pd.DataFrame(chainids, index=[0])
st.dataframe(chainids)

# import json
# import requests
# df = requests.get('https://node-api.flipsidecrypto.com/api/v2/queries/a5898a28-b950-40b4-8677-1af86297f228/data/latest').json()
