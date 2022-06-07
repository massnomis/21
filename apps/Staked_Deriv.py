
from itertools import accumulate
import pandas as pd
import streamlit as st
import plotly.express as px
import requests


def app():
    page = st.container()

    df3 = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/267a1f10-c765-4c2e-bb28-0282629c75ed/data/latest')
    # st.write(df3)
    # st.write(df3.columns)
    # st.plotly_chart(ggg)
    hhh = px.bar(df3,x='DAYZ_CVXCRV_BAL',y='BALANCE_CVXCRV_BAL')
    page.plotly_chart(hhh)
    iii = px.bar(df3,x='DAYZ_CVXCRV_BAL',y='AMOUNT_USD_CVXCRV_BAL')
    page.plotly_chart(iii)
    jjj = px.bar(df3,x='DAYZ_CVXCRV_BAL',y='PRICE_CVXCRV_BAL')
    page.plotly_chart(jjj)





    df0 = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/f5586f7c-486d-43b5-942b-40d35cb93022/data/latest')
    # st.write(df0)
    # st.write(df0.columns)
    aaa = px.bar(df0,x='DAYZ_REWARDS_PAID',y='SUM_AMT_USD_REWARDS_PAID', color='SYMBOL_REWARDS_PAID')
    page.plotly_chart(aaa)

    aaa = px.bar(df0,x='DAYZ_REWARDS_PAID',y='SUM_AMT_REWARDS_PAID', color='SYMBOL_REWARDS_PAID')
    page.plotly_chart(aaa)



    df4 = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/e67ea397-b602-49b4-9e04-007960d14e78/data/latest')
    # st.write(df4)

    lll = px.scatter(df4,x='DAYZ',y=['PRICE_CVXCRV','PRICE_CRV'])
    page.plotly_chart(lll)
    # llal = px.line(df4,x='DAYZ',y=['PRICE_CVXCRV','PRICE_CRV'])
    # st.plotly_chart(llal)
    mmm = px.scatter(df4,x='DAYZ',y='BPS_SPREAD')
    page.plotly_chart(mmm)




    # df5 = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/7ab92869-7ee2-4a30-ac3f-ccd3722381f1/data/latest')

    # # st.write(df5)
    # nnn = px.bar(df5,x='DAYZ',y='APY',color='SYMBOL_REWARDS_PAID')
    # st.plotly_chart(nnn)

    # df5['APY2'] = df5['APY'] / 365
    # accumulated = (list(accumulate(df5['APY2'])))

    # df5['accumulated'] = accumulated


    # ppp = px.scatter(df5,x='DAYZ',y='APY2',color='SYMBOL_REWARDS_PAID')
    # st.plotly_chart(ppp)



    xyz = requests.get('https://ftxpremiums.com/assets/data/funding_data/CRV-PERP.json').json()

    xyz = pd.DataFrame(xyz)
    xyz['rate'] = xyz['rate'].astype(float)
    xyz['time'] =  pd.to_datetime(xyz['time'], unit='s')
    xyz = xyz.sort_values(by="time")




    xyz = pd.DataFrame(xyz)
    # print(xyz)
    # print(xyz.columns)
    xyz['rate'] = xyz['rate'] * 1000

    xyz['accumulated'] = (list(accumulate(xyz['rate'])))


    bbbbbb = px.scatter(xyz,x='time',y='rate')
    page.plotly_chart(bbbbbb)
    bbbbbbb = px.scatter(xyz,x='time',y='accumulated')
    page.plotly_chart(bbbbbbb)
    # st.write(xyz)
    page.markdown('https://llama.airforce/#/votium/overview')
    xyz2 = requests.get('https://ftxpremiums.com/assets/data/funding_data/CVX-PERP.json').json()

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
    # st.write(xyz)



