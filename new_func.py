import streamlit as st
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES
import requests
import json
import time
import streamlit as st
import pandas as pd
import plotly.express as px
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
copy_this_ex = """select * from aave.liquidations limit 543"""

st.code(copy_this_ex)
# content = """ """ 
API_KEY = "48bd4a71-3872-4b90-a0a0-a8a879cfb113"
API_KEY = st.text_input("Enter your API key", API_KEY )
def ace():
    poly = "https://node-api.flipsidecrypto.com/api/v2/queries/b6937d3a-152f-4261-ac26-64bf84a31744/data/latest"
    to_read = st.text_input("Enter your api", poly )

    df = pd.read_json(
        to_read,
        convert_dates=["TIMESTAMP_NTZ"],
    )
    
    def convert_df(df):
        return df.to_csv().encode('utf-8')


    csv = convert_df(df)

    st.download_button(
    "Press to Download",
    csv,
    "file.csv",
    "text/csv",
    key='download-csv'
    )
    see_full = st.checkbox("See full data")
    if see_full:
        st.write(df)
    # df = df.fillna('null')


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
        gen_report(df=df)


    chart_type = st.selectbox("Chart type", ["line", "bar", "scatter", "violin", "box", "area"])


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
            if chart_type == "violin":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.violin(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True, log_x=True, box=True, hover_data=df.columns), use_container_width=True)')
                        st.plotly_chart(px.violin(df, y =y, x =x, color=color_sort, log_y=True, log_x=True, box=True, hover_data=df.columns), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.violin(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True, box=True, hover_data=df.columns), use_container_width=True)')
                        st.plotly_chart(px.violin(df, y =y, x =x, color=color_sort, log_y=True, box=True, hover_data=df.columns), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.violin(df, y ="{y}", x ="{x}", color="{color_sort}", box=True, hover_data=df.columns), use_container_width=True)')
                    st.plotly_chart(px.violin(df, y =y, x =x, color=color_sort, box=True, hover_data=df.columns), use_container_width=True)
            if chart_type == "box":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.box(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                        st.plotly_chart(px.box(df, y =y, x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.box(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                        st.plotly_chart(px.box(df, y =y, x =x, color=color_sort, log_y=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.box(df, y ="{y}", x ="{x}", color="{color_sort}"), use_container_width=True)')
                    st.plotly_chart(px.box(df, y =y, x =x, color=color_sort), use_container_width=True)
            if chart_type == "area":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.area(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                        st.plotly_chart(px.area(df, y =y, x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.area(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                        st.plotly_chart(px.area(df, y =y, x =x, color=color_sort, log_y=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.area(df, y ="{y}", x ="{x}", color="{color_sort}"), use_container_width=True)')
                    st.plotly_chart(px.area(df, y =y, x =x, color=color_sort), use_container_width=True)
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
            if chart_type == "violin":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.violin(df, y ="{y}", x ="{x}", log_y=True, log_x=True, box=True, hover_data=df.columns), use_container_width=True)')
                        st.plotly_chart(px.violin(df, y =y, x =x, log_y=True, log_x=True, box=True, hover_data=df.columns), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.violin(df, y ="{y}", x ="{x}", log_y=True, box=True, hover_data=df.columns), use_container_width=True)')
                        st.plotly_chart(px.violin(df, y =y, x =x, log_y=True, box=True, hover_data=df.columns), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.violin(df, y ="{y}", x ="{x}", box=True, hover_data=df.columns), use_container_width=True)')
                    st.plotly_chart(px.violin(df, y =y, x =x, box=True, hover_data=df.columns), use_container_width=True)
            if chart_type == "box":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.box(df, y ="{y}", x ="{x}", log_y=True, log_x=True, hover_data=df.columns), use_container_width=True)')
                        st.plotly_chart(px.box(df, y =y, x =x, log_y=True, log_x=True, hover_data=df.columns), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.box(df, y ="{y}", x ="{x}", log_y=True, hover_data=df.columns), use_container_width=True)')
                        st.plotly_chart(px.box(df, y =y, x =x, log_y=True, hover_data=df.columns), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.box(df, y ="{y}", x ="{x}", hover_data=df.columns), use_container_width=True)')
                    st.plotly_chart(px.box(df, y =y, x =x, hover_data=df.columns), use_container_width=True)
            if chart_type == "area":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.area(df, y ="{y}", x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                        st.plotly_chart(px.area(df, y =y, x =x, log_y=True, log_x=True), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.area(df, y ="{y}", x ="{x}", log_y=True), use_container_width=True)')
                        st.plotly_chart(px.area(df, y =y, x =x, log_y=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.area(df, y ="{y}", x ="{x}"), use_container_width=True)')
                    st.plotly_chart(px.area(df, y =y, x =x), use_container_width=True)
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
            if chart_type == "violin":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.violin(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True, box=True, hover_data=df.columns), use_container_width=True)')
                        st.plotly_chart(px.violin(df, y =[y1, y2], x =x, color=color_sort, log_y=True, log_x=True, box=True, hover_data=df.columns), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.violin(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True, box=True, hover_data=df.columns), use_container_width=True)')
                        st.plotly_chart(px.violin(df, y =[y1, y2], x =x, color=color_sort, log_y=True, box=True, hover_data=df.columns), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.violin(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", box=True, hover_data=df.columns), use_container_width=True)')
                    st.plotly_chart(px.violin(df, y =[y1, y2], x =x, color=color_sort, box=True, hover_data=df.columns), use_container_width=True)
            if chart_type == "box":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.box(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True, box=True, hover_data=df.columns), use_container_width=True)')
                        st.plotly_chart(px.box(df, y =[y1, y2], x =x, color=color_sort, log_y=True, log_x=True, box=True, hover_data=df.columns), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.box(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True, box=True, hover_data=df.columns), use_container_width=True)')
                        st.plotly_chart(px.box(df, y =[y1, y2], x =x, color=color_sort, log_y=True, box=True, hover_data=df.columns), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.box(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", box=True, hover_data=df.columns), use_container_width=True)')
                    st.plotly_chart(px.box(df, y =[y1, y2], x =x, color=color_sort, box=True, hover_data=df.columns), use_container_width=True)
            if chart_type == "area":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.area(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                        st.plotly_chart(px.area(df, y =[y1, y2], x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.area(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                        st.plotly_chart(px.area(df, y =[y1, y2], x =x, color=color_sort, log_y=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.area(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}"), use_container_width=True)')
                    st.plotly_chart(px.area(df, y =[y1, y2], x =x, color=color_sort), use_container_width=True)
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
            if chart_type == "violin":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.violin(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True, log_x=True, box=True, hover_data=df.columns), use_container_width=True)')
                        st.plotly_chart(px.violin(df, y =[y1, y2], x =x, log_y=True, log_x=True, box=True, hover_data=df.columns), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.violin(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True, box=True, hover_data=df.columns), use_container_width=True)')
                        st.plotly_chart(px.violin(df, y =[y1, y2], x =x, log_y=True, box=True, hover_data=df.columns), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.violin(df, y =["{y1}", "{y2}"], x ="{x}", box=True, hover_data=df.columns), use_container_width=True)')
                    st.plotly_chart(px.violin(df, y =[y1, y2], x =x, box=True, hover_data=df.columns), use_container_width=True)
            if chart_type == "area":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.area(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                        st.plotly_chart(px.area(df, y =[y1, y2], x =x, log_y=True, log_x=True), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.area(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True), use_container_width=True)')
                        st.plotly_chart(px.area(df, y =[y1, y2], x =x, log_y=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.area(df, y =["{y1}", "{y2}"], x ="{x}"), use_container_width=True)')
                    st.plotly_chart(px.area(df, y =[y1, y2], x =x), use_container_width=True)
            if chart_type == "box":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.box(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                        st.plotly_chart(px.box(df, y =[y1, y2], x =x, log_y=True, log_x=True), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.box(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True), use_container_width=True)')
                        st.plotly_chart(px.box(df, y =[y1, y2], x =x, log_y=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.box(df, y =["{y1}", "{y2}"], x ="{x}"), use_container_width=True)')
                    st.plotly_chart(px.box(df, y =[y1, y2], x =x), use_container_width=True)
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
            if chart_type == "violin":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.violin(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True, box=True, hover_data=df.columns), use_container_width=True)')
                        st.plotly_chart(px.violin(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True, log_x=True, box=True, hover_data=df.columns), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.violin(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True, box=True, hover_data=df.columns), use_container_width=True)')
                        st.plotly_chart(px.violin(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True, box=True, hover_data=df.columns), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.violin(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", box=True, hover_data=df.columns), use_container_width=True)')
                    st.plotly_chart(px.violin(df, y =[y1, y2, y3], x =x, color=color_sort), use_container_width=True, box=True, hover_data=df.columns)
            if chart_type == "area":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.area(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                        st.plotly_chart(px.area(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.area(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                        st.plotly_chart(px.area(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.area(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}"), use_container_width=True)')
                    st.plotly_chart(px.area(df, y =[y1, y2, y3], x =x, color=color_sort), use_container_width=True)
            if chart_type == "box":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.box(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                        st.plotly_chart(px.box(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.box(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                        st.plotly_chart(px.box(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.box(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}"), use_container_width=True)')
                    st.plotly_chart(px.box(df, y =[y1, y2, y3], x =x, color=color_sort), use_container_width=True)
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
            if chart_type == "violin":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.violin(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True, box=True, hover_data=df.columns), use_container_width=True)')
                        st.plotly_chart(px.violin(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True, log_x=True, box=True, hover_data=df.columns), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.violin(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True, box=True, hover_data=df.columns), use_container_width=True)')
                        st.plotly_chart(px.violin(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True, box=True, hover_data=df.columns), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.violin(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", box=True, hover_data=df.columns), use_container_width=True)')
                    st.plotly_chart(px.violin(df, y =[y1, y2, y3], x =x, color=color_sort, box=True, hover_data=df.columns), use_container_width=True)
            if chart_type == "area":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.area(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                        st.plotly_chart(px.area(df, y =[y1, y2, y3], x =x, log_y=True, log_x=True), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.area(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", log_y=True), use_container_width=True)')
                        st.plotly_chart(px.area(df, y =[y1, y2, y3], x =x, log_y=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.area(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}"), use_container_width=True)')
                    st.plotly_chart(px.area(df, y =[y1, y2, y3], x =x), use_container_width=True)
            if chart_type == "box":
                if log_y:
                    if log_x:
                        st.code(f'st.plotly_chart(px.box(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                        st.plotly_chart(px.box(df, y =[y1, y2, y3], x =x, log_y=True, log_x=True), use_container_width=True)
                    else:
                        st.code(f'st.plotly_chart(px.box(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", log_y=True), use_container_width=True)')
                        st.plotly_chart(px.box(df, y =[y1, y2, y3], x =x, log_y=True), use_container_width=True)
                else:
                    st.code(f'st.plotly_chart(px.box(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}"), use_container_width=True)')
                    st.plotly_chart(px.box(df, y =[y1, y2, y3], x =x), use_container_width=True)

ace()

# st.set_page_config(layout="wide")

# variable = st.text_input("Enter your date_variable", "day")


