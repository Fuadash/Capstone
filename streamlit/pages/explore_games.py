import streamlit as st
from src.services.data_loader import load_data
from src.ui.filters import render_sidebar_filters
from src.utils.filtering import apply_filters
from src.ui.tables import games_table

st.title("Explore Games")

for key, val in st.session_state.items():
    st.session_state[key] = val

df = load_data("../etl/data/processed/processed_data.csv")
filters = render_sidebar_filters(df)
filtered = apply_filters(df, filters)


# Game table
games_table(filtered)

st.info("Go to the **Game Details** page for live info.")