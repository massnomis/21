import streamlit as st
from multiapp import MultiApp
from apps import Staked_Deriv, Paper,CVXCRV_prices, stables, stables_funding, home, stables_spot_funding,stables_spot_funding2

app = MultiApp()
st.set_page_config(layout="wide")
# page = st.container()
# Add all your application here


app.add_app("home", home.app)

app.add_app("Paper", Paper.app)
app.add_app("Staked_Deriv", Staked_Deriv.app)
app.add_app("stables", stables.app)
app.add_app("stables_funding", stables_funding.app)
app.add_app("stables_spot_funding", stables_spot_funding.app)
app.add_app("stables_spot_funding2", stables_spot_funding2.app)

app.add_app("CVXCRV_prices", CVXCRV_prices.app)








app.run()