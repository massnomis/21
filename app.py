import streamlit as st
from multiapp import MultiApp
from apps import Staked_Deriv, Paper,CVXCRV_prices, stables, stables_funding, home, bidirectional, liquidity_checker, lending_funding_premiums
app = MultiApp()
st.set_page_config(layout="wide")
# page = st.container()
# Add all your application here
app.add_app("liquidity_checker", liquidity_checker.app)


app.add_app("home", home.app)

app.add_app("Paper", Paper.app)
app.add_app("Staked_Deriv", Staked_Deriv.app)
app.add_app("stables", stables.app)
app.add_app("stables_funding", stables_funding.app)
app.add_app("bidirectional", bidirectional.app)
app.add_app("CVXCRV_prices", CVXCRV_prices.app)

app.add_app("lending_funding_premiums", lending_funding_premiums.app)






app.run()