import streamlit as st
st.set_page_config(layout="wide")
# st.markdown(f"""
# <iframe height="100%" width="100%" id="geckoterminal-embed" title="GeckoTerminal Embed" src="https://www.geckoterminal.com/bsc/pools/0x2477fb288c5b4118315714ad3c7fd7cc69b00bf9?embed=1&info=1&swaps=1" frameborder="0" allow="clipboard-write" allowfullscreen></iframe>
# """, unsafe_allow_html=True )st.markdown(f"""
# <iframe height="100%" width="100%" id="geckoterminal-embed" title="GeckoTerminal Embed" src="https://www.geckoterminal.com/bsc/pools/0x2477fb288c5b4118315714ad3c7fd7cc69b00bf9?embed=1&info=1&swaps=1" frameborder="0" allow="clipboard-write" allowfullscreen></iframe>
# """, unsafe_allow_html=True )
# html = '''<iframe height="100%" width="100%" id="geckoterminal-embed" title="GeckoTerminal Embed" src="https://www.geckoterminal.com/bsc/pools/0x2477fb288c5b4118315714ad3c7fd7cc69b00bf9?embed=1&info=1&swaps=1" frameborder="0" allow="clipboard-write" allowfullscreen></iframe>'''
st.components.v1.iframe('https://www.geckoterminal.com/bsc/pools/0x2477fb288c5b4118315714ad3c7fd7cc69b00bf91', width=1000, height=1000, scrolling=True)