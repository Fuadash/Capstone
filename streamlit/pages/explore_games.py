import streamlit as st
from src.services.data_loader import load_data
from src.ui.filters import render_sidebar_filters
from src.utils.filtering import apply_filters
from src.ui.tables import games_table

st.title("Explore Games")

df = load_data("../etl/data/processed/processed_data.csv")
filters = render_sidebar_filters(df)
filtered = apply_filters(df, filters)

# Render table if rows exist
if not filtered.empty:
    games_table(filtered)
else:
    st.warning("No Games to Display")


st.info("Go to the **Game Details** page for live info.")
