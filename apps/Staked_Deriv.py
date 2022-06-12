
from itertools import accumulate
import pandas as pd
# from sqlalchemy import false
import streamlit as st
import plotly.express as px
import requests
from plotly.subplots import make_subplots
import plotly.graph_objects as go



def app():
    page = st.container()

    page.write("Convert CRV to cvxCRV. By staking cvxCRV, you're earning the usual rewards from veCRV (3crv governance fee distribution from Curve + any airdrop), plus a share of 10 percent of the Convex LPs' boosted CRV earnings, and CVX tokens on top of that.")
    df3 = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/267a1f10-c765-4c2e-bb28-0282629c75ed/data/latest')
    # st.write(df3)
    page.write('https://www.convexfinance.com/stake')
    # st.write(df3.columns)
    # st.plotly_chart(ggg)
    
    page.write("Pooled Value within the staking pool, denominated in the native staked asset (cvxCRV)")

    hhh = px.line(df3,x='DAYZ_CVXCRV_BAL',y='BALANCE_CVXCRV_BAL',render_mode="SVG")
    page.plotly_chart(hhh)
    page.write("Balance Staked in USD terms")

    iii = px.line(df3,x='DAYZ_CVXCRV_BAL',y='AMOUNT_USD_CVXCRV_BAL',render_mode="SVG")
    page.plotly_chart(iii)



    df0 = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/f5586f7c-486d-43b5-942b-40d35cb93022/data/latest')
    page.write("Daily USD value of rewards paid, sorted by rewards token")

    aaa = px.line(df0,x='DAYZ_REWARDS_PAID',y='SUM_AMT_USD_REWARDS_PAID', color='SYMBOL_REWARDS_PAID',render_mode="SVG")
    page.plotly_chart(aaa)
    page.write("Balance Claimed in Native Terms")

    aaa = px.line(df0,x='DAYZ_REWARDS_PAID',y='SUM_AMT_REWARDS_PAID', color='SYMBOL_REWARDS_PAID',render_mode="SVG")
    page.plotly_chart(aaa)



    page.write("Annualized Yield of rewards by token")


    df5 = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/7ab92869-7ee2-4a30-ac3f-ccd3722381f1/data/latest')

    # st.write(df5)
    nnn = px.line(df5,x='DAYZ',y='APY',color='SYMBOL_REWARDS_PAID',render_mode="SVG")
    page.plotly_chart(nnn)
    page.write("Yield, in basis points per day")

    df5['Daily_Gains_bps'] = df5['APY'] / 3.6524



    accumulated = (list(accumulate(df5['Daily_Gains_bps'])))

    df5['accumulated'] = accumulated


    ppp = px.line(df5,x='DAYZ',y='Daily_Gains_bps',color='SYMBOL_REWARDS_PAID',render_mode="SVG")
    page.plotly_chart(ppp)

    df5['moving_average_apy'] = df5.groupby('SYMBOL_REWARDS_PAID')['APY'].transform(lambda x: x.rolling(30, 1).mean())
    # page.write(df5)
    df5['moving_daily_average_gains'] = df5.groupby('SYMBOL_REWARDS_PAID')['Daily_Gains_bps'].transform(lambda x: x.rolling(30, 1).mean())
    ppp = px.line(df5,x='DAYZ',y='moving_average_apy',color='SYMBOL_REWARDS_PAID',render_mode="SVG")
    page.plotly_chart(ppp)
    ppp = px.bar(df5,x='DAYZ',y='moving_average_apy',color='SYMBOL_REWARDS_PAID')
    page.plotly_chart(ppp)
    ppp = px.line(df5,x='DAYZ',y='moving_daily_average_gains',color='SYMBOL_REWARDS_PAID',render_mode="SVG")
    page.plotly_chart(ppp)
    ppp = px.bar(df5,x='DAYZ',y='moving_daily_average_gains',color='SYMBOL_REWARDS_PAID')
    page.plotly_chart(ppp)
    page.write("Underlying Prices of Rewards Tokens")

    ppp = px.line(df5,x='DAYZ',y='TKN_PRICE_REWARDS_PAID',color='SYMBOL_REWARDS_PAID',render_mode="SVG")
    page.plotly_chart(ppp)


    # accumulated = (list(accumulate(df5['Daily_Gains_bps'])))
    df5 = df5.drop(columns=['RUN_AMT_REWARDS_PAID', 'RUN_AMT_USD_REWARDS_PAID', 'DAYZ_CVXCRV_BAL','RUN_AMT_STAKING', 'RUN_AMT_USD_STAKING','RUN_AMT_UNSTAKING' ])
    # df5['accumulated'] = accumulated
    df5 = df5.sort_values(by=['DAYZ'], ascending=True)
    # page.write(df5)

    df5['accumulated'] = df5['Daily_Gains_bps'].cumsum()
    df5 = df5.sort_values(by=['DAYZ'], ascending=True)
    # page.write(df5)
    # 'SYMBOL_REWARDS_PAID'
    page.write("Accumulated Yield, All tokens (basis points)")

    ppp = px.line(df5,x='DAYZ',y='accumulated',render_mode="SVG")
    page.plotly_chart(ppp)
    # df5['accumulated_isolated'] = df5.groupby('SYMBOL_REWARDS_PAID')['Daily_APY'].list(accumulate(df5['Daily_APY']))
    # page.write(df5)



    filterCRV = df5['SYMBOL_REWARDS_PAID']=='CRV'
    CRV_only = df5.where(filterCRV, inplace = False)
    CRV_only = CRV_only.dropna(how='all')




    CRV_only['Accumulated_CRV_daily_bps'] = CRV_only['Daily_Gains_bps'].cumsum()
    CRV_only['Accumulated_CRV_USD_REWARDS'] = CRV_only['SUM_AMT_USD_REWARDS_PAID'].cumsum()
    CRV_only['Accumulated_CRV_REWARDS'] = CRV_only['SUM_AMT_REWARDS_PAID'].cumsum()
    CRV_only['CRV_REWARDS_CUM_NOW_USD'] = CRV_only['TKN_PRICE_REWARDS_PAID']*CRV_only['Accumulated_CRV_REWARDS']
    CRV_only['CRV_CUM_Yield_bps'] = 1000 * CRV_only['Accumulated_CRV_REWARDS']/CRV_only['AMOUNT_USD_CVXCRV_BAL']

    # page.write(df5)
    # 'SYMBOL_REWARDS_PAID'
    page.write("Accumulated Yield, CRV (basis points)")

    ppp = px.line(CRV_only,x='DAYZ',y='Accumulated_CRV_daily_bps',render_mode="SVG")

    page.plotly_chart(ppp)
    page.write("Accumulated CRV, in USD terms")


    ppp = px.line(CRV_only,x='DAYZ',y='Accumulated_CRV_USD_REWARDS',render_mode="SVG")
    
    page.plotly_chart(ppp)
    page.write("Accumulated CRV, in Native terms")

    ppp = px.line(CRV_only,x='DAYZ',y='Accumulated_CRV_REWARDS',render_mode="SVG")
    
    page.plotly_chart(ppp)
    page.write("Accumulated CRV, in native terms multiplied by the current price (on each day)")

    # ppp = px.line(CRV_only,x='DAYZ',y='TKN_PRICE_REWARDS_PAID',render_mode="SVG")
    
    # page.plotly_chart(ppp)    
    ppp = px.line(CRV_only,x='DAYZ',y='CRV_REWARDS_CUM_NOW_USD',render_mode="SVG")
    
    page.plotly_chart(ppp)   

    # ppp = px.line(CRV_only,x='DAYZ',y='CRV_CUM_Yield_bps',render_mode="SVG")
    
    # page.plotly_chart(ppp)   

     
    # page.write(CRV_only)

    filterCVX = df5['SYMBOL_REWARDS_PAID']=='CVX'
    CVX_only = df5.where(filterCVX, inplace = False)
    CVX_only = CVX_only.dropna(how='all')

    CVX_only['Accumulated_CVX_daily_bps'] = CVX_only['Daily_Gains_bps'].cumsum()
    CVX_only['Accumulated_CVX_USD_REWARDS'] = CVX_only['SUM_AMT_USD_REWARDS_PAID'].cumsum()
    CVX_only['Accumulated_CVX_REWARDS'] = CVX_only['SUM_AMT_REWARDS_PAID'].cumsum()
    CVX_only['CVX_REWARDS_CUM_NOW_USD'] = CVX_only['TKN_PRICE_REWARDS_PAID']*CVX_only['Accumulated_CVX_REWARDS']
    CVX_only['CVX_CUM_Yield_bps'] = 1000 * CVX_only['Accumulated_CVX_REWARDS']/CVX_only['AMOUNT_USD_CVXCRV_BAL']

    # page.write(df5)
    # 'SYMBOL_REWARDS_PAID'
    page.write("Accumulated Yield, CVX (basis points)")

    ppp = px.line(CVX_only,x='DAYZ',y='Accumulated_CVX_daily_bps',render_mode="SVG")
    page.plotly_chart(ppp)
    page.write("Accumulated CVX, in USD terms")

    ppp = px.line(CVX_only,x='DAYZ',y='Accumulated_CVX_USD_REWARDS',render_mode="SVG")
    
    page.plotly_chart(ppp)
    page.write("Accumulated CVX, in Native terms")

    ppp = px.line(CVX_only,x='DAYZ',y='Accumulated_CVX_REWARDS',render_mode="SVG")
    
    page.plotly_chart(ppp)
    page.write("Accumulated CVX, in native terms multiplied by the current price (on each day)")

    # ppp = px.line(CVX_only,x='DAYZ',y='TKN_PRICE_REWARDS_PAID',render_mode="SVG")
    
    # page.plotly_chart(ppp)
    ppp = px.line(CVX_only,x='DAYZ',y='CVX_REWARDS_CUM_NOW_USD',render_mode="SVG")
    
    page.plotly_chart(ppp) 
    # ppp = px.line(CVX_only,x='DAYZ',y='CVX_CUM_Yield_bps',render_mode="SVG")
    
    # page.plotly_chart(ppp)   
  
    # page.write(CVX_only)
# SUM_AMT_REWARDS_PAID
# SUM_AMT_USD_REWARDS_PAID
    filter3CRV = df5['SYMBOL_REWARDS_PAID']=="3Crv"
    tCRV_only = df5.where(filter3CRV, inplace = False)
    tCRV_only = tCRV_only.dropna(how='all')
    tCRV_only['Accumulated_3CRV_daily_bps'] = tCRV_only['Daily_Gains_bps'].cumsum()
    tCRV_only['Accumulated_3CRV_USD_REWARDS'] = tCRV_only['SUM_AMT_USD_REWARDS_PAID'].cumsum()
    tCRV_only['Accumulated_3CRV_REWARDS'] = tCRV_only['SUM_AMT_REWARDS_PAID'].cumsum()
    tCRV_only['3CRV_REWARDS_CUM_NOW_USD'] = tCRV_only['TKN_PRICE_REWARDS_PAID']*tCRV_only['Accumulated_3CRV_REWARDS']
    tCRV_only['3CRV_CUM_Yield_bps'] = 1000 * tCRV_only['Accumulated_3CRV_REWARDS']/tCRV_only['AMOUNT_USD_CVXCRV_BAL']

    # page.write(df5)

    # 'SYMBOL_REWARDS_PAID'
    page.write("Accumulated Yield, 3CRV (basis points)")

    ppp = px.line(tCRV_only,x='DAYZ',y='Accumulated_3CRV_daily_bps',render_mode="SVG")
    page.plotly_chart(ppp)
    page.write("Accumulated 3CRV, in USD terms")

    ppp = px.line(tCRV_only,x='DAYZ',y='Accumulated_3CRV_USD_REWARDS',render_mode="SVG")
    
    page.plotly_chart(ppp)
    page.write("Accumulated 3CRV, in Native terms")

    ppp = px.line(tCRV_only,x='DAYZ',y='Accumulated_3CRV_REWARDS',render_mode="SVG")
    
    page.plotly_chart(ppp)
    # ppp = px.line(tCRV_only,x='DAYZ',y='TKN_PRICE_REWARDS_PAID',render_mode="SVG")
    
    # page.plotly_chart(ppp)
    page.write("Accumulated CVX, in native terms multiplied by the current price (on each day)")

    ppp = px.line(tCRV_only,x='DAYZ',y='3CRV_REWARDS_CUM_NOW_USD',render_mode="SVG")
    
    page.plotly_chart(ppp)   
    # page.write(tCRV_only)

    # ppp = px.line(tCRV_only,x='DAYZ',y='3CRV_CUM_Yield_bps',render_mode="SVG")
    
    # page.plotly_chart(ppp)   
  




