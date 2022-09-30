# print API and SECRET from the dotenv file
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
st.code(os.getenv('API'))
st.code(os.getenv('SECRET'))
