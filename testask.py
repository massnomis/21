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
# st.write(df_eth)
df_poly = pd.read_json(
    poly,
    convert_dates=["TIMESTAMP_NTZ"],
)
# st.write(df_poly)

merged_df = pd.merge(df_eth, df_poly, on="HOUR")
st.write(merged_df)
def gen_report(df):

        pr = gen_profile_report(df, explorative=True)

        st.write(df)

        with st.expander("REPORT", expanded=True):
            st_profile_report(pr)


@st.cache(allow_output_mutation=True)
def gen_profile_report(df, *report_args, **report_kwargs):
    return df.profile_report(*report_args, **report_kwargs)
gen_report_click = st.checkbox("Generate report", False)
if gen_report_click:
    gen_report(df=merged_df)

# with placeholder:
df=merged_df
st.write(df.columns)
st.write(df.head())
# df = df.fillna('null')

# gb = GridOptionsBuilder.from_dataframe(df)
# gb.configure_pagination()
# gb.configure_side_bar()
# gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
# gridOptions = gb.build()
# gb.configure_selection(selection_mode="multiple", use_checkbox=True)

# data = AgGrid(df, 
#               gridOptions=gridOptions, 
#               enable_enterprise_modules=True, 
#               allow_unsafe_jscode=True, 
#               update_mode=GridUpdateMode.SELECTION_CHANGED)
# # df = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True)
# st.write(data)
# selected_rows = data["selected_rows"]
# selected_rows = pd.DataFrame(selected_rows)
# st.write(selected_rows)
# df = pd.DataFrame(df["data"])
# df = df.fillna(0)

# st.dataframe(df)


chart_type = st.selectbox("Chart type", ["line", "bar", "scatter"])


number_of_y_axis = st.number_input("Number of y values to plot", value=1, min_value=1, max_value=3)

color = st.checkbox("Color sort?")
if number_of_y_axis == 1:
    x = st.selectbox("X axis", df.columns, index = 0)
    y = st.selectbox("Y axis", df.columns, index = 3)
    if color:
        color_sort = st.selectbox("Color by", df.columns)
        if chart_type == "line":
            st.code(f'st.plotly_chart(px.line(df, y ="{y}", x ="{x}", color="{color_sort}"), use_container_width=True)')
            st.plotly_chart(px.line(df, y =y, x =x, color=color_sort), use_container_width=True)
        if chart_type == "bar":
            st.code(f'st.plotly_chart(px.bar(df, y ="{y}", x ="{x}", color="{color_sort}"), use_container_width=True)')
            st.plotly_chart(px.bar(df, y =y, x =x, color=color_sort), use_container_width=True)
        if chart_type == "scatter":
            st.code(f'st.plotly_chart(px.scatter(df, y ="{y}", x ="{x}", color="{color_sort}"), use_container_width=True)')
            st.plotly_chart(px.scatter(df, y =y, x =x, color=color_sort), use_container_width=True)
    else:
        if chart_type == "line":
            st.code(f'st.plotly_chart(px.line(df, y ="{y}", x ="{x}"), use_container_width=True)')
            st.plotly_chart(px.line(df, y =y, x =x), use_container_width=True)
        if chart_type == "bar":
            st.code(f'st.plotly_chart(px.bar(df, y ="{y}", x ="{x}"), use_container_width=True)')
            st.plotly_chart(px.bar(df, y =y, x =x), use_container_width=True)
        if chart_type == "scatter":
            st.code(f'st.plotly_chart(px.scatter(df, y ="{y}", x ="{x}"), use_container_width=True)')
            st.plotly_chart(px.scatter(df, y =y, x =x), use_container_width=True)
if number_of_y_axis == 2:
    x = st.selectbox("X axis", df.columns)
    y1 = st.selectbox("Y axis 1", df.columns)
    y2 = st.selectbox("Y axis 2", df.columns)
    if color:
        color_sort = st.selectbox("Color by", df.columns)
        if chart_type == "line":
            st.plotly_chart(px.line(df, y =[y1, y2], x =x, color=color_sort), use_container_width=True)
        if chart_type == "bar":
            st.plotly_chart(px.bar(df, y =[y1, y2], x =x, color=color_sort), use_container_width=True)
        if chart_type == "scatter":
            st.plotly_chart(px.scatter(df, y =[y1, y2], x =x, color=color_sort), use_container_width=True)
    else:
        if chart_type == "line":
            st.plotly_chart(px.line(df, y =[y1, y2], x =x), use_container_width=True)
        if chart_type == "bar":
            st.plotly_chart(px.bar(df, y =[y1, y2], x =x), use_container_width=True)
        if chart_type == "scatter":
            st.plotly_chart(px.scatter(df, y =[y1, y2], x =x), use_container_width=True)
if number_of_y_axis == 3: 
    x = st.selectbox("X axis", df.columns)
    y1 = st.selectbox("Y axis 1", df.columns)
    y2 = st.selectbox("Y axis 2", df.columns)
    y3 = st.selectbox("Y axis 3", df.columns)
    if color:
        color_sort = st.selectbox("Color by", df.columns)
        if chart_type == "line":
            st.plotly_chart(px.line(df, y =[y1, y2, y3], x =x, color=color_sort), use_container_width=True)
        if chart_type == "bar":
            st.plotly_chart(px.bar(df, y =[y1, y2, y3], x =x, color=color_sort), use_container_width=True)
        if chart_type == "scatter":
            st.plotly_chart(px.scatter(df, y =[y1, y2, y3], x =x, color=color_sort), use_container_width=True)
    else:
        if chart_type == "line":
            st.plotly_chart(px.line(df, y =[y1, y2, y3], x =x), use_container_width=True)
        if chart_type == "bar":
            st.plotly_chart(px.bar(df, y =[y1, y2, y3], x =x), use_container_width=True)
        if chart_type == "scatter":
            st.plotly_chart(px.scatter(df, y =[y1, y2, y3], x =x), use_container_width=True)

    # pip install pandas_profiling --user
    # pip install streamlit_pandas_profiling --user