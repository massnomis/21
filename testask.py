import requests
import json
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

import requests
import json
import time
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
API_KEY = "48bd4a71-3872-4b90-a0a0-a8a879cfb113"
reserve_name = pd.read_csv('download-1b921f5f-164b-4202-bf85-467b7dde828d.csv')
reserve_name = st.selectbox("reserve_name", reserve_name, index = 6)
st.write(reserve_name)
SQL_QUERY = """select * from flipside_prod_db.aave.market_stats
 where RESERVE_NAME = '""" 
+ reserve_name + """' order by block_hour desc""" 

API_KEY = st.text_input("Enter your API key", API_KEY )
SQL_QUERY = st.text_input("Enter your SQL query", SQL_QUERY)
TTL_MINUTES = 15
st.code(SQL_QUERY)

def create_query():
    r = requests.post(
        'https://node-api.flipsidecrypto.com/queries', 
        data=json.dumps({
            "sql": SQL_QUERY,
            "ttlMinutes": TTL_MINUTES
        }),
        headers={"Accept": "application/json", "Content-Type": "application/json", "x-api-key": API_KEY},
    )
    if r.status_code != 200:
        raise Exception("Error creating query, got response: " + r.text + "with status code: " + str(r.status_code))
    
    return json.loads(r.text)    


def get_query_results(token):
    r = requests.get(
        'https://node-api.flipsidecrypto.com/queries/' + token, 
        headers={"Accept": "application/json", "Content-Type": "application/json", "x-api-key": API_KEY}
    )
    if r.status_code != 200:
        raise Exception("Error getting query results, got response: " + r.text + "with status code: " + str(r.status_code))
    
    data = json.loads(r.text)
    if data['status'] == 'running':
        time.sleep(10)
        return get_query_results(token)

    return data
# run_query = st.button("Run query")
# if run_query:

query = create_query()
token = query.get('token')
data = get_query_results(token)

# print(data['columnLabels'])
# for row in data['results']:
#     print(row)
# return data
# placeholder = st.empty()
# with placeholder:
df = pd.DataFrame(data['results'], columns=data['columnLabels'])
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
    y = st.selectbox("Y axis", df.columns, index = 16)
    if color:
        color_sort = st.selectbox("Color by", df.columns)
        if chart_type == "line":
            st.plotly_chart(px.line(df, y =y, x =x, color=color_sort), use_container_width=True)
        if chart_type == "bar":
            st.plotly_chart(px.bar(df, y =y, x =x, color=color_sort), use_container_width=True)
        if chart_type == "scatter":
            st.plotly_chart(px.scatter(df, y =y, x =x, color=color_sort), use_container_width=True)
    else:
        if chart_type == "line":
            st.plotly_chart(px.line(df, y =y, x =x), use_container_width=True)
        if chart_type == "bar":
            st.plotly_chart(px.bar(df, y =y, x =x), use_container_width=True)
        if chart_type == "scatter":
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


i
# names_lending = 'BTC/USD'
# df2 = requests.get(f"https://ftx.com/api/markets/{names_lending}/orderbook?depth=100").json()
# # st.write(df2)
# df2 = pd.DataFrame(df2)
# df2 = df2['result']
# asks = df2['asks']
# bids = df2['bids']
# asks = pd.DataFrame(asks)
# bids = pd.DataFrame(bids)
# asks = asks.rename(columns={0: "price", 1: "size"})
# bids = bids.rename(columns={0: "price", 1: "size"})
# st.write(bids, asks)