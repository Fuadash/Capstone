import streamlit as st
from src.services.data_loader import load_data
from src.ui.filters import render_sidebar_filters
from src.utils.filtering import apply_filters
from src.ui.tables import games_table
from src.services.load_env import load_env

config = load_env()

st.title("Explore Games")

# hacky solution
for key, val in st.session_state.items():
    if (key == "selected_game_name" or key == "selected_appid" or key=="search_text"):
        st.session_state[key] = val


DATA_PATH = config["DATA_PATH"]
df = load_data(DATA_PATH)
filters = render_sidebar_filters(df)
filtered = apply_filters(df, filters)

# Render table if rows exist
if not filtered.empty:
    games_table(filtered)
else:
    st.warning("No Games to Display")


st.info("Go to the **Game Details** page for live info.")
