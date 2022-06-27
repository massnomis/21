import requests
import pandas as pd
import time
df = pd.DataFrame()
for i in range(20):
    df = pd.concat([df, pd.json_normalize(requests.get("https://api.cryptowat.ch/markets/kraken/btcusd/orderbook").json()["result"]).assign(timestamp=pd.to_datetime("now"))])
    time.sleep(1)
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

d = df.loc[:, ["timestamp", "asks"]].explode("asks").assign(
    price=lambda d: d["asks"].apply(lambda a: a[0]),
    size=lambda d: d["asks"].apply(lambda a: a[1]),
)


px.scatter(d, x="timestamp", y="size", color="price")
go.Figure(go.Heatmap(x=d["timestamp"], y=d["size"], z=d["price"]))
