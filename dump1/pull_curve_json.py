# import streamlit as st
# import requests
# import json
# import pandas as pd
# import math
#
# from itertools import chain
#
# import plotly.express as px
# from datetime import datetime
# ts = int('1645598410')
#
# print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
#
# # liq_sauce = requests.get("https://stats.curve.fi/raw-stats/3pool-1m.json")
# # liq_sauce = json.loads(liq_sauce.text)
# #
# # st.write(liq_sauce)
#
#
#
#
#
# # https://stats.curve.fi/raw-stats/3pool-1m.json
import pandas as pd
import streamlit as st
import requests
import plotly
import plotly.express as px
import json
import time

data = {
    'Name':
        [
         'Yaniv',
         'Yasha',
         'Avishay',
         'Sam',
         'Tim',
         'Asif',
         'raz',
         'Ylann'
         ],
    'address':
        [
         "0x3e35698c962BCFfBab99594aff3fa136db78b300",
         "0xEe3dBd4d25000C599bBF3B4497D12c733e7A0cB4",
         "0x52B9C25c4d16a2efe83c89bcfC6fE259B05658A5",
         "0xba2ef5189B762bd4C9E7f0b50fBBaB65193935e8",
         "0x48E92AaDd3b92Aa875fe08BF27fe44080eEC749a",
         "0x6bA98440b46d12b46d3393b21319c38AaC12249a",
         "0xa68166badfc75a15ee2f8a30a8230f8e1b8b4f82",
         "0xc562e686cfdc46a4cc7294447611ee8a952e4a03"
         ]
}
df = pd.DataFrame(data)
st.title("The EF LinkedIn Token Party")
points = []
for address in df['address']:
    bal_custom = requests.get(
        f"https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress=0x23a32ba2b63051950e8421c18fb300870993d9a9&address={address}&tag=latest&apikey=FSQ6MKYTF5335UAIX3IQZP8XYUX394AU8Q").json()
    bal = float(bal_custom['result']) / 10 ** 18
    list.append(points, bal)
    time.sleep(0.5)

df['points'] = points
# print(df)

df = df.sort_values(by=['points'], ascending=False)
df['rank'] = df['points'].rank(ascending = False)
st.write("The LeaderBoard")




df = df.set_index('address')
# print(df)


st.write(df)


LeaderBoard = px.bar(
    df, #this is the dataframe you are trying to plot
    x = "Name",
    y = "points",
    color = "rank",
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600
)
st.write("The chart")
st.plotly_chart(LeaderBoard)


st.write("The Recents")
# recents =
query_id = "28ec29cc-7bc8-4245-bd56-837ad4bedb15"
df = pd.read_json(f"https://api.flipsidecrypto.com/api/v2/queries/{query_id}/data/latest",
convert_dates=["TIMESTAMP_NTZ"],
)
df = px.bar(
    df,  # this is the dataframe you are trying to plot
    x="TIME",
    y="ACTUAL_AMT",
    color = "NAME",
    orientation="v",
    template="plotly_white",
    width=1000,
    height=600
)
st.plotly_chart(df)


query_id = "b89af3ae-02e3-492e-868d-d2a2c9f669db"
df = pd.read_json(f"https://api.flipsidecrypto.com/api/v2/queries/{query_id}/data/latest",
convert_dates=["TIMESTAMP_NTZ"],
)
st.write(df)


st.write("For the most recent transaction data, check on chain")
st.markdown("""https://polygonscan.com/token/0x23a32ba2b63051950e8421c18fb300870993d9a9""")




st.title("ahem...")

st.markdown("""
If you need a reminder - These are the participating positions:""")

st.markdown(""" 
R&D-
DeFi Developer - efficientfrontier.28.324@applynow.io
""")
st.markdown(""" 

Full-Stack / BackEnd - efficientfrontier.48.829@applynow.io """)
st.markdown(""" 

Head of DevOps - efficientfrontier.AA.82F@applynow.io """)
st.markdown(""" 

Head of QA and Automation - efficientfrontier.87.826@applynow.io""")
st.markdown("""Product Manager - efficientfrontier.D5.32B@applynow.io""")
st.markdown("""All R&D CVs you’re not sure where to send - efficientfrontier.92.C22@applynow.io""")

st.markdown("""Trading: Trading Operations Specialist - efficientfrontier.9E.225@applynow.io""")

st.markdown("""PLEASE don’t forget to add a link to our career pages in your posts! the link is efrontier.io/careers""")

st.title("...")
st.write("@massnomis")
