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
# st.write(extrarpsc)
# st.code(extrarpsc)
st.write("Select a chain")
chain = st.selectbox('Chain', list(extrarpsc.keys()))

df_chain_rpcs = pd.DataFrame(extrarpsc[chain]['rpcs'])
st.write(df_chain_rpcs)

st.write("which one")
rpc_choice = st.selectbox('rpc', df_chain_rpcs.index)
rpc_url = extrarpsc[chain]['rpcs'][rpc_choice]
st.code(rpc_url)


