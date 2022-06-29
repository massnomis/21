
API_KEY = "48bd4a71-3872-4b90-a0a0-a8a879cfb113"
import requests
import json
import time
import streamlit as st
import pandas as pd
import plotly.express as px
SQL_QUERY ="""
select * from flipside_prod_db.aave.liquidations order by block_timestamp desc
"""

API_KEY = st.text_input("Enter your API key", API_KEY )
SQL_QUERY = st.text_input("Enter your SQL query", SQL_QUERY)
TTL_MINUTES = 15

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


query = create_query()
token = query.get('token')
data = get_query_results(token)

# print(data['columnLabels'])
# for row in data['results']:
#     print(row)
# return data
df = pd.DataFrame(data['results'], columns=data['columnLabels'])
st.write(df)
st.write(df.columns)
df = df.fillna('null')

chart_type = st.selectbox("Chart type", ["line", "bar", "scatter"])


number_of_y_axis = st.number_input("Number of y values to plot", value=1, min_value=1, max_value=3)

color = st.checkbox("Color sort?")
if number_of_y_axis == 1:
    x = st.selectbox("X axis", df.columns)
    y = st.selectbox("Y axis", df.columns)
    if color:
        color_sort = st.selectbox("Color by", df.columns)
        if chart_type == "line":
            st.plotly_chart(px.line(df, y =y, x =x, color=color_sort))
        if chart_type == "bar":
            st.plotly_chart(px.bar(df, y =y, x =x, color=color_sort))
        if chart_type == "scatter":
            st.plotly_chart(px.scatter(df, y =y, x =x, color=color_sort))
    else:
        if chart_type == "line":
            st.plotly_chart(px.line(df, y =y, x =x))
        if chart_type == "bar":
            st.plotly_chart(px.bar(df, y =y, x =x))
        if chart_type == "scatter":
            st.plotly_chart(px.scatter(df, y =y, x =x))
if number_of_y_axis == 2:
    x = st.selectbox("X axis", df.columns)
    y1 = st.selectbox("Y axis 1", df.columns)
    y2 = st.selectbox("Y axis 2", df.columns)
    if color:
        color_sort = st.selectbox("Color by", df.columns)
        if chart_type == "line":
            st.plotly_chart(px.line(df, y =[y1, y2], x =x, color=color_sort))
        if chart_type == "bar":
            st.plotly_chart(px.bar(df, y =[y1, y2], x =x, color=color_sort))
        if chart_type == "scatter":
            st.plotly_chart(px.scatter(df, y =[y1, y2], x =x, color=color_sort))
    else:
        if chart_type == "line":
            st.plotly_chart(px.line(df, y =[y1, y2], x =x))
        if chart_type == "bar":
            st.plotly_chart(px.bar(df, y =[y1, y2], x =x))
        if chart_type == "scatter":
            st.plotly_chart(px.scatter(df, y =[y1, y2], x =x))
if number_of_y_axis == 3: 
    x = st.selectbox("X axis", df.columns)
    y1 = st.selectbox("Y axis 1", df.columns)
    y2 = st.selectbox("Y axis 2", df.columns)
    y3 = st.selectbox("Y axis 3", df.columns)
    if color:
        color_sort = st.selectbox("Color by", df.columns)
        if chart_type == "line":
            st.plotly_chart(px.line(df, y =[y1, y2, y3], x =x, color=color_sort))
        if chart_type == "bar":
            st.plotly_chart(px.bar(df, y =[y1, y2, y3], x =x, color=color_sort))
        if chart_type == "scatter":
            st.plotly_chart(px.scatter(df, y =[y1, y2, y3], x =x, color=color_sort))
    else:
        if chart_type == "line":
            st.plotly_chart(px.line(df, y =[y1, y2, y3], x =x))
        if chart_type == "bar":
            st.plotly_chart(px.bar(df, y =[y1, y2, y3], x =x))
        if chart_type == "scatter":
            st.plotly_chart(px.scatter(df, y =[y1, y2, y3], x =x))



    # st.write(data.head())
    # st.write(data.columns())
    # st.plotly_chart(px.bar(data, x="HOUR", y="DEPOSITS", color = 'TO_LABEL'))
    # st.plotly_chart(px.line(data, x="DAYZ", y="ETH_SPENT_FEES_NATIVE"))
    # http://localhost:3000, http://localhost:3001



    #     SELECT
    #         date_trunc('day',block_timestamp) as hour,
    #         sum(amount) as withdrawals,
    #   from_label
    #     FROM ethereum.udm_events
    #     WHERE 
    #         block_timestamp >= getdate() - interval '4800 hours'
#         and from_label_type = 'cex'
#         and (to_label_type <> 'cex' OR to_label_type IS NULL)
#         and symbol = 'CEL' 
#     GROUP BY 1,3





