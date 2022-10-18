import os
import requests
from pinatapy import PinataPy
import json
import streamlit as st

from dotenv import load_dotenv
# load_dotenv()  # take environment variables from .env.





PinataAPIKey = "4bbc23ad99d8ed840bc1"

PinataAPISecret = "c57a8a7a4c8ecfa787d84651c1d65641f7dec858bcac15d6a29e8b476c8e5600"

# JWT
# (Secret access token)
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiIxYzc1MTE3My04YTQyLTQ3NTYtOTRiYS1iNWUzMDgwYjM5YTUiLCJlbWFpbCI6Im1hc3Nub21pc0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGluX3BvbGljeSI6eyJyZWdpb25zIjpbeyJpZCI6Ik5ZQzEiLCJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MX1dLCJ2ZXJzaW9uIjoxfSwibWZhX2VuYWJsZWQiOmZhbHNlLCJzdGF0dXMiOiJBQ1RJVkUifSwiYXV0aGVudGljYXRpb25UeXBlIjoic2NvcGVkS2V5Iiwic2NvcGVkS2V5S2V5IjoiNGJiYzIzYWQ5OWQ4ZWQ4NDBiYzEiLCJzY29wZWRLZXlTZWNyZXQiOiJjNTdhOGE3YTRjOGVjZmE3ODdkODQ2NTFjMWQ2NTY0MWY3ZGVjODU4YmNhYzE1ZDZhMjllOGI0NzZjOGU1NjAwIiwiaWF0IjoxNjY0NTEwODcwfQ.0NqEkLji1CFR_QZmryKNSy5auLuJPEOf-beyWi_kWgM
# # 
# 


# Connect to the IPFS cloud service
pinata_api_key=str(PinataAPIKey)
pinata_secret_api_key=str(PinataAPISecret)
pinata = PinataPy(pinata_api_key,pinata_secret_api_key)

# Upload the file
file = st.text_input("Enter the file path")
result = pinata.pin_file_to_ipfs(file+".py")

# Should return the CID (unique identifier) of the file
st.write('''hould return the CID (unique identifier) of the file''')
st.write(result)

# Anything waiting to be done?
st.write(''' Anything waiting to be done?''')



st.write(pinata.pin_jobs())

# 
# 
st.write('''List of items we have pinned so far''')
# st.write(pinata.pin_list())
pin_pipn_list = pinata.pin_list()
st.dataframe(pin_pipn_list["rows"])
# Total data in use
st.write(''' Total data in use''')
st.write(pinata.user_pinned_data_total())

# Get our pinned item
st.write('''Get our pinned item''')
# gateway="https://gateway.pinata.cloud/ipfs/"
gateway="https://ipfs.io/ipfs/"
st.code(gateway+result['IpfsHash'])

req = (requests.get(url=gateway+result['IpfsHash'])).text
st.code(req)


custom = st.text_input('custom hash')
if custom:
    st.code(gateway+custom)
    reqq = (requests.get(gateway+custom)).text
    st.code(reqq)
upload_check = requests.get("https://ipfs.io/ipfs/QmRyVm5zTKCXCRxjeDSpg3Rgfbc926Mf932KFA5Ck862Yj").text
st.code(upload_check)