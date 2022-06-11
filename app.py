import streamlit as st
from multiapp import MultiApp
from apps import Staked_Deriv, Paper,CVXCRV_prices, stables, stables_funding, home, stables_spot_funding,stables_spot_funding2

app = MultiApp()
st.set_page_config(layout="wide")
# page = st.container()
# Add all your application here


app.add_app("home", home.app)

app.add_app("Commercial Paper", Paper.app)
app.add_app("Staking and Staked Derivatives", Staked_Deriv.app)
app.add_app("Stablecoins, price variation and opportunities", stables.app)
app.add_app("Underlying interest rates of stablecoins, and of their derivatives", stables_funding.app)
app.add_app("Stables_spot_funding", stables_spot_funding.app)
app.add_app("Stables_spot_funding2", stables_spot_funding2.app)

app.add_app("CVXCRV_prices", CVXCRV_prices.app)
app.run()
