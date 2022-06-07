
from itertools import accumulate
import pandas as pd
import streamlit as st
import plotly.express as px
import requests
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import random

def app():   
    page = st.container()

    page.write('usdt perp')

    xyz2 = requests.get('https://ftxpremiums.com/assets/data/funding_data/USDT-PERP.json').json()

    xyz2 = pd.DataFrame(xyz2)

    xyz2['rate'] = xyz2['rate'].astype(float)
    xyz2['time'] =  pd.to_datetime(xyz2['time'], unit='s')
    xyz2 = xyz2.sort_values(by="time")






    xyz2['rate'] = xyz2['rate'] * 1000
    xyz2['accumulated']  = (list(accumulate(xyz2['rate'])))

    bbbbbb = px.scatter(xyz2,x='time',y='rate')
    page.plotly_chart(bbbbbb)
    bbbbbbb = px.scatter(xyz2,x='time',y='accumulated')
    page.plotly_chart(bbbbbbb)
    page.write('cusdt perp')
    xyz22 = requests.get('https://ftxpremiums.com/assets/data/funding_data/CUSDT-PERP.json').json()

    xyz22 = pd.DataFrame(xyz22)
    xyz22['rate'] = xyz22['rate'].astype(float)
    xyz22['time'] =  pd.to_datetime(xyz22['time'], unit='s')
    xyz22 = xyz22.sort_values(by="time")






    xyz22['rate'] = xyz22['rate'] * 1000
    xyz22['accumulated']  = (list(accumulate(xyz22['rate'])))

    bbbbbb = px.scatter(xyz22,x='time',y='rate')
    page.plotly_chart(bbbbbb)
    bbbbbbb = px.scatter(xyz22,x='time',y='accumulated')
    page.plotly_chart(bbbbbbb)

    gb = GridOptionsBuilder.from_dataframe(xyz2)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
        xyz2,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT', 
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=False,
        theme='blue', #Add theme color to the table
        enable_enterprise_modules=True,
        height=350, 
        width='100%',
        reload_data=True
    )

    data = grid_response['data']
    selected = grid_response['selected_rows'] 
    df = pd.DataFrame(selected) #`Pass the selected rows to a new dataframe df
    AgGrid(xyz2)
