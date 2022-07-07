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

dexes = "https://node-api.flipsidecrypto.com/api/v2/queries/f13a6fcb-0ed5-4788-b3a9-34c10e0db820/data/latest"
df_dexes = pd.read_json(
    dexes,
    convert_dates=["TIMESTAMP_NTZ"],
)
st.write(df_dexes)



























df = df_dexes
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
    gen_report(df=df_dexes)
st.write(df.columns)
st.write(df.head())


chart_type = st.selectbox("Chart type", ["line", "bar", "scatter"])


number_of_y_axis = st.number_input("Number of y values to plot", value=1, min_value=1, max_value=3)
color = st.checkbox("Color sort?")
log_y = st.checkbox("Log scale  Y ?")
log_x = st.checkbox("Log scale  X ?")



if number_of_y_axis == 1:
    x = st.selectbox("X axis", df.columns, index = 0)
    y = st.selectbox("Y axis", df.columns, index = 3)
    if color:
        color_sort = st.selectbox("Color by", df.columns)
        if chart_type == "line":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.line(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.line(df, y =y, x ="{x}", color=color_sort, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.line(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.line(df, y =y, x =x, color=color_sort, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.line(df, y ="{y}", x ="{x}", color="{color_sort}"), use_container_width=True)')
                st.plotly_chart(px.line(df, y =y, x =x, color=color_sort), use_container_width=True)
        if chart_type == "bar":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.bar(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.bar(df, y =y, x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.bar(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.bar(df, y =y, x =x, color=color_sort, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.bar(df, y ="{y}", x ="{x}", color="{color_sort}"), use_container_width=True)')
                st.plotly_chart(px.bar(df, y =y, x =x, color=color_sort), use_container_width=True)
        if chart_type == "scatter":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.scatter(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.scatter(df, y =y, x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.scatter(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.scatter(df, y =y, x =x, color=color_sort, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.scatter(df, y ="{y}", x ="{x}", color="{color_sort}"), use_container_width=True)')
                st.plotly_chart(px.scatter(df, y =y, x =x, color=color_sort), use_container_width=True)
    else:
        if chart_type == "line":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.line(df, y ="{y}", x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.line(df, y =y, x =x, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.line(df, y ="{y}", x ="{x}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.line(df, y =y, x =x, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.line(df, y ="{y}", x ="{x}"), use_container_width=True)')
                st.plotly_chart(px.line(df, y =y, x =x), use_container_width=True)
        if chart_type == "bar":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.bar(df, y ="{y}", x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.bar(df, y =y, x =x, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.bar(df, y ="{y}", x ="{x}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.bar(df, y =y, x =x, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.bar(df, y ="{y}", x ="{x}"), use_container_width=True)')
                st.plotly_chart(px.bar(df, y =y, x =x), use_container_width=True)
        if chart_type == "scatter":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.scatter(df, y ="{y}", x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.scatter(df, y =y, x =x, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.scatter(df, y ="{y}", x ="{x}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.scatter(df, y =y, x =x, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.scatter(df, y ="{y}", x ="{x}"), use_container_width=True)')
                st.plotly_chart(px.scatter(df, y =y, x =x), use_container_width=True)
if number_of_y_axis == 2:
    x = st.selectbox("X-axis", df.columns)
    y1 = st.selectbox("Y-axis 1", df.columns)
    y2 = st.selectbox("Y-axis 2", df.columns)
    if color:
        color_sort = st.selectbox("Color", df.columns)
        if chart_type == "line":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.line(df, y =[y1, y2], x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.line(df, y =[y1, y2], x =x, color=color_sort, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}"), use_container_width=True)')
                st.plotly_chart(px.line(df, y =[y1, y2], x =x, color=color_sort), use_container_width=True)
        if chart_type == "bar":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.bar(df, y =[y1, y2], x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.bar(df, y =[y1, y2], x =x, color=color_sort, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}"), use_container_width=True)')
                st.plotly_chart(px.bar(df, y =[y1, y2], x =x, color=color_sort), use_container_width=True)
        if chart_type == "scatter":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.scatter(df, y =[y1, y2], x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.scatter(df, y =[y1, y2], x =x, color=color_sort, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}"), use_container_width=True)')
                st.plotly_chart(px.scatter(df, y =[y1, y2], x =x, color=color_sort), use_container_width=True)
    else:
        if chart_type == "line":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.line(df, y =[y1, y2], x =x, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.line(df, y =[y1, y2], x =x, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}"], x ="{x}"), use_container_width=True)')
                st.plotly_chart(px.line(df, y =[y1, y2], x =x), use_container_width=True)
        if chart_type == "bar":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.bar(df, y =[y1, y2], x =x, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.bar(df, y =[y1, y2], x =x, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}"], x ="{x}"), use_container_width=True)')
                st.plotly_chart(px.bar(df, y =[y1, y2], x =x), use_container_width=True)
        if chart_type == "scatter":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.scatter(df, y =[y1, y2], x =x, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.scatter(df, y =[y1, y2], x =x, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}"], x ="{x}"), use_container_width=True)')
                st.plotly_chart(px.scatter(df, y =[y1, y2], x =x), use_container_width=True)
if number_of_y_axis == 3:
    x = st.selectbox("X-axis", df.columns)
    y1 = st.selectbox("Y-axis 1", df.columns)
    y2 = st.selectbox("Y-axis 2", df.columns)
    y3 = st.selectbox("Y-axis 3", df.columns)
    if color:
        color_sort = st.selectbox("Color", df.columns)
        if chart_type == "line":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.line(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.line(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}"), use_container_width=True)')
                st.plotly_chart(px.line(df, y =[y1, y2, y3], x =x, color=color_sort), use_container_width=True)
        if chart_type == "bar":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.bar(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.bar(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}"), use_container_width=True)')
                st.plotly_chart(px.bar(df, y =[y1, y2, y3], x =x, color=color_sort), use_container_width=True)
        if chart_type == "scatter":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.scatter(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.scatter(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}"), use_container_width=True)')
                st.plotly_chart(px.scatter(df, y =[y1, y2, y3], x =x, color=color_sort), use_container_width=True)
    else:
        if chart_type == "line":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.line(df, y =[y1, y2, y3], x =x, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.line(df, y =[y1, y2, y3], x =x, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}"), use_container_width=True)')
                st.plotly_chart(px.line(df, y =[y1, y2, y3], x =x), use_container_width=True)
        if chart_type == "bar":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.bar(df, y =[y1, y2, y3], x =x, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.bar(df, y =[y1, y2, y3], x =x, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}"), use_container_width=True)')
                st.plotly_chart(px.bar(df, y =[y1, y2, y3], x =x), use_container_width=True)
        if chart_type == "scatter":
            if log_y:
                if log_x:
                    st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                    st.plotly_chart(px.scatter(df, y =[y1, y2, y3], x =x, log_y=True, log_x=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", log_y=True), use_container_width=True)')
                    st.plotly_chart(px.scatter(df, y =[y1, y2, y3], x =x, log_y=True), use_container_width=True)
            else:
                st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}"), use_container_width=True)')
                st.plotly_chart(px.scatter(df, y =[y1, y2, y3], x =x), use_container_width=True)


            










