import streamlit as st
from src.services.data_loader import load_data
from src.services.steam_client import get_live_game_info
from src.ui.layout import load_css
import pandas as pd

st.title("Game Details")

# Load data and css
df = load_data("../etl/data/processed/processed_data.csv")
load_css()
filtered = df["Name"]

# Text input with session logic
search = st.text_input(
    label="Search for a game",
    key="search_text",
)

# Filter down names based on text input
if search:
    filtered = filtered[filtered.str.contains(search, case=False)]

options = filtered.unique()[:55]
for r in options:
    print(repr(r))

# Protects against filters which exclude a currently selected game
if st.session_state.get("selected_game_name") not in options:
    st.session_state["selected_game_name"] = options[0] if len(options) > 0 else None

# Display radio options based on options
if len(options) > 0:
    game_name = st.radio(
        "Select a game",
        options=options,
        key="selected_game_name"
    )
else:
    st.write("No games found.")
    st.stop()

# Get AppID based on current selection, put it in session
# TODO: Maybe redunant? Using sessions here may be overengineered
if game_name:
    match = df.loc[df["Name"] == game_name]
    if not match.empty:
        st.session_state["selected_appid"] = int(match.iloc[0]["AppID"])

# Pull the AppID from the session
# TODO: Maybe redundant? See above
appid = st.session_state.get("selected_appid")
if not appid:
    st.warning("Pick a game to view live data.")
    st.stop()

# Make API request and write it to data
data = get_live_game_info(appid, cc="gb", lang="en") or {}
if data:
    st.write(f"Live data for **{data.get("name", {})}**")
    st.image(data.get("header_image"))
else:
    st.write(f"Fetching live data for **{st.session_state['selected_game_name']}**...")

# Render the pages

tab_overview, tab_pricing, tab_reviews = st.tabs(["Overview", "Pricing", "Reviews"])

with tab_overview:
    st.subheader("Description")
    st.write(data.get("short_description", "—"))

    st.subheader("Developers")
    st.write(", ".join(data.get("developers", [])) or "—")

    # look up the row only if a game is selected
    selected = st.session_state.get("selected_game_name")
    if selected:
        match = df.loc[df["Name"] == selected]
        if not match.empty:
            notes = match.iloc[0]["Notes"]
            if pd.notna(notes) and str(notes).strip():
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
    # get data from API req
    reviews = data.get("reviews", {})
    meta = data.get("metacritic", {})
    # Show values from API
    if reviews or meta:
        st.subheader("Critic Reviews")
    if reviews:
        st.write(reviews.replace("<br>", "\n"))
    if meta:
        st.write(f"Metacritic: {meta.get('score')} / 100")
    # Show values from dataframe if exists
    selected = st.session_state.get("selected_game_name")
    if selected:
        match = df.loc[df["Name"] == selected]
        if not match.empty:
            st.subheader("User Reviews")
            positive = match.iloc[0]["Positive"]
            positive_percent = match.iloc[0]["Positive %"]
            sentiment = match.iloc[0]["Sentiment"]
            if pd.notna(positive) and positive > 0:
                st.write(f"No. of recommendations from users: {int(positive)}")
            if pd.notna(positive_percent):
                st.write(f"Percentage positive reviews: {int(positive_percent)}%")
            if pd.notna(sentiment):
                st.write(f"Overall sentiment from users: {sentiment}")
    if not (meta or reviews or selected):
        st.info("No review data available.")
