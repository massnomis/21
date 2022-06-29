
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
SQL_QUERY = """select * from flipside_prod_db.aave.market_stats where RESERVE_NAME = '""" + reserve_name + """' order by block_hour desc"""

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
st.write(df.head())
see_full = st.checkbox("See full data")
if see_full:
    st.write(df)
st.write(df.columns)

df = df.fillna('null')

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
