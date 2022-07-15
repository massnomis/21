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
    # gen_report(df=df)






    # #Example controlers
    # st.subheader("St-AgGrid example options")

    # sample_size = st.number_input("rows", min_value=10, value=30)
    # grid_height = st.number_input("Grid height", min_value=200, max_value=800, value=300)

    # return_mode = st.selectbox("Return Mode", list(DataReturnMode.__members__), index=1)
    # return_mode_value = DataReturnMode.__members__[return_mode]

    # update_mode = st.selectbox("Update Mode", list(GridUpdateMode.__members__), index=6)
    # update_mode_value = GridUpdateMode.__members__[update_mode]

    # #enterprise modules
    # enable_enterprise_modules = st.checkbox("Enable Enterprise Modules")
    # if enable_enterprise_modules:
    #     enable_sidebar =st.checkbox("Enable grid sidebar", value=False)
    # else:
    #     enable_sidebar = False

    # #features
    # fit_columns_on_grid_load = st.checkbox("Fit Grid Columns on Load")

    # enable_selection=st.checkbox("Enable row selection", value=True)
    # if enable_selection:
    #     st.subheader("Selection options")
    #     selection_mode = st.radio("Selection Mode", ['single','multiple'], index=1)

    #     use_checkbox = st.checkbox("Use check box for selection", value=True)
    #     if use_checkbox:
    #         groupSelectsChildren = st.checkbox("Group checkbox select children", value=True)
    #         groupSelectsFiltered = st.checkbox("Group checkbox includes filtered", value=True)

    #     if ((selection_mode == 'multiple') & (not use_checkbox)):
    #         rowMultiSelectWithClick = st.checkbox("Multiselect with click (instead of holding CTRL)", value=False)
    #         if not rowMultiSelectWithClick:
    #             suppressRowDeselection = st.checkbox("Suppress deselection (while holding CTRL)", value=False)
    #         else:
    #             suppressRowDeselection=False
    #     st.text("___")

    # enable_pagination = st.checkbox("Enable pagination", value=False)
    # if enable_pagination:
    #     st.subheader("Pagination options")
    #     paginationAutoSize = st.checkbox("Auto pagination size", value=True)
    #     if not paginationAutoSize:
    #         paginationPageSize = st.number_input("Page size", value=5, min_value=0, max_value=sample_size)
    #     st.text("___")

    # # df = fetch_data(sample_size)

    # #Infer basic colDefs from dataframe types
    # gb = GridOptionsBuilder.from_dataframe(df)

    # #customize gridOptions
    # # gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)

    # # gb.configure_column("date_tz_aware", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='yyyy-MM-dd HH:mm zzz', pivot=True)

    # # gb.configure_column("apple", type=["numericColumn","numberColumnFilter","customNumericFormat"], precision=2, aggFunc='sum')
    # # gb.configure_column("banana", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1, aggFunc='avg')
    # # gb.configure_column("chocolate", type=["numericColumn", "numberColumnFilter", "customCurrencyFormat"], custom_currency_symbol="R$", aggFunc='max')

    # #configures last row to use custom styles based on cell's value, injecting JsCode on components front end
    # cellsytle_jscode = JsCode("""
    # function(params) {
    #     if (params.value == 'A') {
    #         return {
    #             'color': 'white',
    #             'backgroundColor': 'darkred'
    #         }
    #     } else {
    #         return {
    #             'color': 'black',
    #             'backgroundColor': 'white'
    #         }
    #     }
    # };
    # """)

    # if enable_sidebar:
    #     gb.configure_side_bar()

    # if enable_selection:
    #     gb.configure_selection(selection_mode)
    #     if use_checkbox:
    #         gb.configure_selection(selection_mode, use_checkbox=True, groupSelectsChildren=groupSelectsChildren, groupSelectsFiltered=groupSelectsFiltered)
    #     if ((selection_mode == 'multiple') & (not use_checkbox)):
    #         gb.configure_selection(selection_mode, use_checkbox=False, rowMultiSelectWithClick=rowMultiSelectWithClick, suppressRowDeselection=suppressRowDeselection)

    # if enable_pagination:
    #     if paginationAutoSize:
    #         gb.configure_pagination(paginationAutoPageSize=True)
    #     else:
    #         gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=paginationPageSize)

    # gb.configure_grid_options(domLayout='normal')
    # gridOptions = gb.build()


    # grid_response = AgGrid(
    #     df, 
    #     gridOptions=gridOptions,
    #     height=grid_height, 
    #     width='100%',
    #     data_return_mode=return_mode_value, 
    #     update_mode=update_mode_value,
    #     fit_columns_on_grid_load=fit_columns_on_grid_load,
    #     allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
    #     enable_enterprise_modules=enable_enterprise_modules,
    #     )

    # df = grid_response['data']
    # selected = grid_response['selected_rows']
    # selected_df = pd.DataFrame(selected).apply(pd.to_numeric, errors='coerce')


    # with st.spinner("Displaying results..."):
        
        # st.subheader("grid selection:")
        # selected_df = pd.DataFrame(grid_response['selected_rows'])
        # st.write(selected_df)
        # convert_selected_into_df = st.checkbox("Convert selected rows into dataframe and chart again", value=False)
        # if convert_selected_into_df:
        #     df = selected_df
        #     def convert_df(df):
        #         return df.to_csv().encode('utf-8')


        #     csv = convert_df(df)

        #     st.download_button(
        #     "Press to Download",
        #     csv,
        #     "file.csv",
        #     "text/csv",
        #     key='download-csv'
        #     )
        #     # chart_type = st.selectbox("Chart type", ["scatter", "line", "bar"] ,key =2)

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


ace()

# st.set_page_config(layout="wide")

# variable = st.text_input("Enter your date_variable", "day")


