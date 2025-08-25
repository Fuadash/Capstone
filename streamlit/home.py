import streamlit as st
from src.services.data_loader import load_data
from src.ui.layout import load_css
from src.services.load_env import load_env

config = load_env()

st.set_page_config(
    page_title="Steam Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)
load_css()

# hacky solution
for key, val in st.session_state.items():
    if (key == "selected_game_name" or key == "selected_appid" or key=="search_text"):
        st.session_state[key] = val

st.title("Steam Explorer")
st.write(
    "Use the pages on the left: **Explore Games**, "
    "**Trends**, and **Game Details**."
)
st.image("assets/store_home_share.jpg", width=1300)

# Loads and caches immediately
DATA_PATH = config["DATA_PATH"]
_ = load_data(DATA_PATH)

for k, v in st.session_state.items():
    st.session_state[k] = v
