import streamlit as st
st.title("Hello, I hope this opened correctly: Let's get some dashboards up and running")

st.header("To Open and run a new dashboard we need to open a new terminal ")
st.subheader("Look down where it says 'requirements: bash'. This is an individual terminal instance")
st.write("Underneath is the terminal that is running this dashboard - 'instructions: python3' ")
st.markdown("Move your cursor and press the '+' to open a new terminal")
st.markdown(
'''
You can also use these shortcuts... to open a new terminal 
''')

st.markdown(
'''
PC: CTRL + SHIFT + '
''')

st.markdown(
'''
MAC: CMD + SHIFT + '
'''
)
st.title("Description")
st.markdown(
'''

Command to paste into new terminal
'''
)

st.write('Main APP / Presentation -only static data/charts')
st.code('streamlit run app.py')


st.write('Interactive app that gets biderectional for ETH/USDC on 7 chains, to showcase the difference in prices between pools and chains')
st.code('streamlit run bidirectional.py')


st.write('Simple Page showing a random wallets Convex staking and pending rewards')
st.code('streamlit run debank.py')


st.write('Fun App that shows cumalitive funding rates on FTX')
st.code('streamlit run funding_checker.py')


st.write(' Even more fun App that shows SPOT Lending Rates on FTX')
st.code('streamlit run lending_rates.py')

