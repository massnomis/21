import requests 
import json
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def getdata(url):
    r = requests.get(url)
    data = json.loads(r.text)
    return data

def createjson(df):
    json_string = json.dumps(df)
    return json_string

df=getdata("https://ftx.com/api/markets")
df=pd.DataFrame(df['result'],columns=['name'])
dated_future = st.selectbox("dated_future", df, index=0)
perp = st.selectbox("perp", df, index=0)
financing_market = st.selectbox("financing_market", df, index=0)

df0 = getdata(f"https://ftx.com/api/futures/{dated_future}/stats")
st.write({dated_future}, df0)
df2 = getdata(f"https://ftx.com/api/futures/{perp}/stats")
st.write({perp}, df2)
#df1 = getdata(f"https://ftx.com/api/spot_margin/{financing_market}/stats")
#st.write("asset stats", df1)


df00 = getdata(f"https://ftx.com/api/markets/{dated_future}/candles?resolution=14400")
df00 = pd.DataFrame(df00['result'])

df22 = getdata(f"https://ftx.com/api/markets/{perp}/candles?resolution=14400")
df22 = pd.DataFrame(df22['result'])

df11 = getdata(f"https://ftx.com/api/markets/{financing_market}/candles?resolution=14400")
df11 = pd.DataFrame(df11['result'])


fig0 = make_subplots(rows=2, cols=1, shared_xaxes=True, 
            vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
            row_width=[0.2, 0.7])
# include candlestick with rangeselector
fig0.add_trace(go.Candlestick(x=df00['startTime'],open=df00['open'], high=df00['high'],low=df00['low'], close=df00['close'],name="OHLC"), row=1, col=1)
# include a go.Bar trace for volumes
fig0.add_trace(go.Bar(x=df00['startTime'], y=df00['volume'],
            showlegend=False), row=2, col=1)
fig0.update(layout_xaxis_rangeslider_visible=False)
st.plotly_chart(fig0, use_container_width=True)
st.write("Order book", df00)






fig2 = make_subplots(rows=2, cols=1, shared_xaxes=True, 
            vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
            row_width=[0.2, 0.7])

# include candlestick with rangeselector
fig2.add_trace(go.Candlestick(x=df22['startTime'],open=df22['open'], high=df22['high'],low=df22['low'], close=df22['close'],name="OHLC"), row=1, col=1)

# include a go.Bar trace for volumes
fig2.add_trace(go.Bar(x=df22['startTime'], y=df22['volume'],
            showlegend=False), row=2, col=1)

fig2.update(layout_xaxis_rangeslider_visible=False)
st.plotly_chart(fig0, use_container_width=True)


st.write("Order book", df22)



#######################################################################




fig1 = make_subplots(rows=2, cols=1, shared_xaxes=True, 
            vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
            row_width=[0.2, 0.7])

# include candlestick with rangeselector
fig1.add_trace(go.Candlestick(x=df11['startTime'],open=df11['open'], high=df11['high'],low=df11['low'], close=df22['close'],name="OHLC"), row=1, col=1)

# include a go.Bar trace for volumes
fig1.add_trace(go.Bar(x=df11['startTime'], y=df11['volume'],
            showlegend=False), row=2, col=1)

fig1.update(layout_xaxis_rangeslider_visible=False)
st.plotly_chart(fig1, use_container_width=True)


st.write("Order book", df11)



