import streamlit as st
import requests
import json
import pandas as pd
import math

from itertools import chain

import plotly.express as px


liq_sauce = requests.get("https://stats.curve.fi/raw-stats/3pool-1m.json")
liq_sauce = json.loads(liq_sauce.text)
# liq_sauce = pd.json_normalize(liq_sauce, 'balances',errors="ignore")
#
# Clean_liq_df = liq_sauce
# Clean_liq_df.drop(columns=['img','img_color'], axis=1, inplace=True)

st.dataframe(liq_sauce)


# https://stats.curve.fi/raw-stats/3pool-1m.json