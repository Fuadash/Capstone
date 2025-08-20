import streamlit as st
from src.services.data_loader import load_data
from src.ui.layout import load_css

st.set_page_config(
    page_title="Steam Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)
load_css()

st.title("Steam Explorer")
st.write(
    "Use the pages on the left: **Explore Games**, "
    "**Trends**, and **Game Details**."
)

# Loads and caches immediately
_ = load_data("../etl/data/processed/processed_data.csv")

for k, v in st.session_state.items():
    st.session_state[k] = v