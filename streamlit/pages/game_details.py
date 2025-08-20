import streamlit as st
from src.services.data_loader import load_data
from src.services.steam_client import get_live_game_info
from src.ui.layout import load_css
import pandas as pd

st.title("Game Details")

df = load_data("../etl/data/processed/processed_data.csv")
filtered = df["Name"]
load_css()

# Text input with session logic
search = st.text_input(
    label="Search for a game", value=st.session_state.get("search_text", "")
)
if search:
    st.session_state["search_text"] = search
    filtered = filtered[filtered.str.contains(search, case=False)]

options = filtered.unique()[:99]

# If a game was selected before it will prepopulate radio button based on session
default_game = st.session_state.get("selected_game_name")
if default_game in options:
    default_index = list(options).index(default_game)
else:
    default_index = 0

# Create radio button
with st.container():
    game_name = st.radio(
        label="Select a game",
        options=options,
        key="selected_game_name",
    )

# Use session_state to store selection
if game_name:
    row = df.loc[df["Name"] == game_name].iloc[0]
    #st.session_state["selected_game_name"] = row["Name"]
    st.session_state["selected_appid"] = int(row["AppID"])

appid = st.session_state.get("selected_appid")
if not appid:
    st.warning("Pick a game to view live data.")
    st.stop()


data = get_live_game_info(appid, cc="gb", lang="en") or {}
if data:
    st.write(f"Live data for **{st.session_state['selected_game_name']}**")
    st.image(data.get("header_image"))
else:
    st.write(f"Fetching live data for **{st.session_state['selected_game_name']}**...")

tab_overview, tab_pricing, tab_reviews = st.tabs(["Overview", "Pricing", "Reviews"])

with tab_overview:
    st.subheader("Description")
    st.write(data.get("short_description", "—"))
    st.subheader("Developers")
    st.write(", ".join(data.get("developers", [])) or "—")

    notes = row["Notes"] if "Notes" in row and pd.notna(row["Notes"]) else ""
    if str(notes).strip():
        st.subheader("Sensitive Content")
        st.write(notes)

with tab_pricing:
    is_free = data.get("is_free") or {}
    if is_free:
        st.info("This game is Free-to-Play!")
    else:
        price = data.get("price_overview") or {}
        if price:
            st.metric("Current Price", f"£{price['final']/100:.2f}")
            st.metric("Discount", f"{price.get('discount_percent', 0)}%")
        else:
            st.info("No live pricing available.")

with tab_reviews:
    rec = data.get("recommendations", {})
    meta = data.get("metacritic", {})
    if rec:
        st.write(f"Total Steam reviews: {rec.get('total', 0):,}")
    if meta:
        st.write(f"Metacritic: {meta.get('score')} / 100")
    if not (rec or meta):
        st.info("No review data available.")
