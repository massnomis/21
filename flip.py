
API_KEY = "48bd4a71-3872-4b90-a0a0-a8a879cfb113"
import requests
import json
import time
import streamlit as st
import pandas as pd
import plotly.express as px
SQL_QUERY = """

    SELECT
        date_trunc('hour',block_timestamp) as hour,
        sum(amount) as withdrawals,
  from_label
    FROM ethereum.udm_events
    WHERE 
        block_timestamp >= getdate() - interval '480 hours'
        and from_label_type = 'cex'
        and (to_label_type <> 'cex' OR to_label_type IS NULL)
        and symbol = 'CEL' 
    GROUP BY 1,3
    order by 1 desc
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
data = pd.DataFrame(data['results'], columns=data['columnLabels'])
st.write(data)
st.plotly_chart(px.bar(data, x="HOUR", y="WITHDRAWALS", color = 'FROM_LABEL'))

# def func():



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





#     SELECT
#         date_trunc('day',block_timestamp) as hour,
#         sum(amount) as deposits,
#   to_label
  
#     FROM ethereum.udm_events
#     WHERE 
#         block_timestamp >= getdate() - interval '4800 hours'
#         and to_label_type = 'cex'
#         and (from_label_type <> 'cex' OR from_label_type IS NULL)
#         and symbol = 'CEL' 
#     GROUP BY 1,3