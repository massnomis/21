import requests
import pandas as pd
import time
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
place1 = st.empty()
place2 = st.empty()
df = pd.DataFrame()
place3 = st.empty()
place4 = st.empty()
df1 = pd.DataFrame()
for i in range(20):
    df = pd.concat([df, pd.json_normalize(requests.get("https://api.cryptowat.ch/markets/kraken/btcusd/orderbook").json()["result"]).assign(timestamp=pd.to_datetime("now", utc=True))])
    d = df.loc[:, ["timestamp", "asks"]].explode("asks").assign(
    price_asks=lambda d: d["asks"].apply(lambda a: a[0]),
    size_asks=lambda d: d["asks"].apply(lambda a: a[1]),
    
    
    
    )

    with place1.container():
        st.plotly_chart(px.scatter(d, x="timestamp", y="price_asks", size="size_asks"))
    with place2.container():
        st.plotly_chart(go.Figure(go.Heatmap(x=d["timestamp"], y=d["price_asks"], z=d["size_asks"])))
    df1 = pd.concat([df1, pd.json_normalize(requests.get("https://api.cryptowat.ch/markets/kraken/btcusd/orderbook").json()["result"]).assign(timestamp=pd.to_datetime("now", utc=True))])
    f = df1.loc[:, ["timestamp", "bids"]].explode("bids").assign(
    price_bids=lambda f: f["bids"].apply(lambda a: a[0]),
    size_bids=lambda f: f["bids"].apply(lambda a: a[1]),
    
    
    
    )

    with place3.container():
        st.plotly_chart(px.scatter(f, x="timestamp", y="price_bids", size="size_bids"))
    with place4.container():
        st.plotly_chart(go.Figure(go.Heatmap(x=f["timestamp"], y=f["price_bids"], z=f["size_bids"])))

    time.sleep(1)

# for i in range(20):

#     time.sleep(1)

