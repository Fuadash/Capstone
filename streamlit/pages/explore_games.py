import streamlit as st
from src.services.data_loader import load_data
from src.ui.filters import render_sidebar_filters
from src.utils.filtering import apply_filters
from src.ui.tables import games_table

st.title("Explore Games")

df = load_data("../etl/data/processed/processed_data.csv")
filters = render_sidebar_filters(df)
filtered = apply_filters(df, filters)

# Game table
games_table(filtered)

# Selection widget ( sessionstores selection for other pages)
game_name = st.selectbox(
    "Select a game",
    filtered["Name"].unique(),
    key="explore_selected_game",
    index=filtered["Name"].unique().tolist().index(
        st.session_state.get("selected_game_name", filtered["Name"].iloc[0])
    )
)
if game_name:
    row = filtered.loc[filtered["Name"] == game_name].iloc[0]
    st.session_state["selected_appid"] = int(row["AppID"])
    st.session_state["selected_game_name"] = row["Name"]
    st.info("Go to **Game Details** page for live info.")
