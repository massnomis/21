import streamlit as st
import plotly
import plotly.express as px
import pandas as pd
import json

st.title("USDC-MATIC")
t_f = False
st.sidebar.write("Choose y-axis scale")
check = st.sidebar.checkbox("Linear/Log")
if check: 
    t_f = True

df = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/9ddcf906-7c7a-4ea4-908a-e37f2f8157b5/data/latest",
convert_dates=["TIMESTAMP_NTZ"],
)

st.dataframe(df)

st.markdown("""
""")

df = px.scatter(
    df, #this is the dataframe you are trying to plot
    x = "BLOCK_TIMESTAMP",
    y = "USDC/MATIC",
    color = "TX_TO_ADDRESS_NAME",
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600,
    log_y = t_f

)
st.plotly_chart(df)



df = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/9ddcf906-7c7a-4ea4-908a-e37f2f8157b5/data/latest",
convert_dates=["TIMESTAMP_NTZ"],
)



#-------------------------------------------------------








df = px.scatter(
    df, #this is the dataframe you are trying to plot
    x = "BLOCK_TIMESTAMP",
    y = "USDC",
    color = "TX_TO_ADDRESS_NAME",
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600,
    log_y = t_f
    
)
st.plotly_chart(df)




df = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/9ddcf906-7c7a-4ea4-908a-e37f2f8157b5/data/latest",
convert_dates=["TIMESTAMP_NTZ"],
)




#-------------------------------------------------------



st.markdown("""
""")





df = px.scatter_3d(
    df, #this is the dataframe you are trying to plot
    x = "BLOCK_TIMESTAMP",
    y = "USDC",
    z = "USDC/MATIC",
    color = "TX_TO_ADDRESS_NAME",
    # orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600,
    log_y = t_f
    
)
st.plotly_chart(df)
