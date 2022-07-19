import plotly.express as px
import pandas as pd
import json
import requests
import streamlit as st

from sys import version, exit

from distutils import errors
from distutils.log import error
import streamlit as st
import pandas as pd 
import numpy as np
import altair as alt
from itertools import cycle
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import pandas as pd
import pandas_profiling
import streamlit as st

# from streamlit_gallery.utils.readme import readme
from streamlit_pandas_profiling import st_profile_report
st.set_page_config(layout="wide")

eth = "https://node-api.flipsidecrypto.com/api/v2/queries/fd06b165-9b39-4a3e-a496-e352225e6011/data/latest"
poly = "https://node-api.flipsidecrypto.com/api/v2/queries/b6937d3a-152f-4261-ac26-64bf84a31744/data/latest"
df_eth = pd.read_json(
    eth,
    convert_dates=["TIMESTAMP_NTZ"],
)
st.write(df_eth)
df_poly = pd.read_json(
    poly,
    convert_dates=["TIMESTAMP_NTZ"],
)
st.write(df_poly)

merged_df = pd.merge(df_eth, df_poly, on="HOUR")
st.write(merged_df)
# def gen_report(df):

#         pr = gen_profile_report(df, explorative=True)

#         st.write(df)

#         with st.expander("REPORT", expanded=True):
#             st_profile_report(pr)


# @st.cache(allow_output_mutation=True)
# def gen_profile_report(df, *report_args, **report_kwargs):
#     return df.profile_report(*report_args, **report_kwargs)
# gen_report_click = st.checkbox("Generate report", False)
# if gen_report_click:
#     gen_report(df=merged_df)
# df = merged_df


st.subheader("GAS PRICE vs ASSET PRICES")
st.write("In the chart, ETH prices does not really influence gas price. We clearly see high fees on both range of the ETH price. It s less obvious for Polygon though. ")
st.plotly_chart(px.scatter(merged_df, x="MATICUSD_AVG", y="PRICE", color="EGAS_PRICE_AVG_USD"), use_container_width=True)

st.subheader("ETH GAS PRICE vs ETH PRICE")
st.write("More in details, on ETH we see high fees in both sides of the ETH price range")
st.plotly_chart(px.bar(df, y ="EGAS_PRICE_AVG_USD", x ="HOUR", color="PRICE"), use_container_width=True)

st.subheader("POLYGON GAS PRICE vs MATIC PRICE")
st.write("Again here, we can t really say the MATIC price influence the Gas Price")
st.plotly_chart(px.bar(df, y ="GAS_PRICE_AVG_USD", x ="HOUR", color="MATICUSD_AVG"), use_container_width=True)

st.subheader("MARKET IMPACT on ETH and MATIC GAS PRICES")
st.write("The chart is very interesting as we see High Gas prices in the higher and lower range of the asset price. But more than that, we notice a drop a Gas prices and when we observe big price change. Litteraly, we can start that market volatility as a bigger impact on GAS prices than the the ASSET prices aboslute value")
st.plotly_chart(px.scatter(df, y =["GAS_PRICE_AVG_USD", "EGAS_PRICE_AVG_USD"], x ="HOUR", color="PRICE", log_y=True), use_container_width=True)

st.subheader("MARKET IMPACT on ETH and MATIC TRANSACTION FEES")
st.write("The chart focus on fees paid per hour on ETH and Polygon. Unlike the gas price, we observe a spike in transaction fees during volatility market drop.")
st.plotly_chart(px.scatter(df, y =["PFEES", "EFEES_USD", "PRICE"], x ="HOUR", color="PRICE", log_y=True), use_container_width=True)

st.subheader("POLYGON FEES vs MATIC GAS PRICE")
st.write("More in details, this chart is very interesting as we observe the Negative Correlation between GAS price and PAID FEES")
st.plotly_chart(px.scatter(df, y =["PFEES", "GAS_PRICE_AVG_USD"], x ="HOUR", log_y=True), use_container_width=True)

st.subheader("ETH FEES vs ETH GAS PRICE")
st.write("Same on ETH, Negative Correlation between GAS price and PAID FEES ")
st.plotly_chart(px.scatter(df, y =["EFEES_USD", "EGAS_PRICE_AVG_USD"], x ="HOUR", log_y=True), use_container_width=True)

st.write("The Negative correlation is counter Intuitive, so in order to understand how the could happen, we will have a close look in Gas limit efficiency")

st.subheader("MATIC GAS LIMIT EFFICIENCY")
st.write("Very interesting chart showing how Market volatily impacts the GAS LIMIT efficiency")
st.plotly_chart(px.scatter(df, y ="PCT_AVG_GAS_LIMIT_EFFICIENCY_PER_TRANSACTION", x ="HOUR", color="MATICUSD_AVG", log_y=True), use_container_width=True)
    
st.subheader("MATICS GAS LIMIT EFFICIENCY")
st.write("SAME on ETH, the Market volatily impacts the GAS LIMIT efficiency")
st.plotly_chart(px.scatter(df, y ="PCT_AVG_EGAS_LIMIT_EFFICIENCY", x ="HOUR", color="PRICE", log_y=True), use_container_width=True)
    # pip install pandas_profiling --user
    # pip install streamlit_pandas_profiling --user

st.subheader("CONSEQUENTLY")
st.write("Even though we observe a drop in GAS PRICE due to ASSET PRICE drop, during a high volatility period, GAS LIMIT use becomes more Ineficiency reflecting the market panic, or the emergency of each transaction to be validated.")
st.write("Last observation regarding Polygon FEES, we observe a strong drop in transaction fees since the 5th of July, but we can't really dig deeper into that direction because of a lack of data in FS Tables.")  