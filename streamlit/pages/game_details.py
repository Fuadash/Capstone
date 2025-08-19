import streamlit as st
from src.services.data_loader import load_data
from src.services.steam_client import get_live_game_info

st.title("Game Details")

df = load_data("../etl/data/processed/processed_data.csv")

# Use session_state to store selection
game_name = st.selectbox(
    "Select a game",
    df["Name"].unique(),
    key="details_selected_game",
    index=df["Name"].unique().tolist().index(
        st.session_state.get("selected_game_name", df["Name"].iloc[0])
    )
)

if game_name:
    row = df.loc[df["Name"] == game_name].iloc[0]
    st.session_state["selected_game_name"] = row["Name"]
    st.session_state["selected_appid"] = int(row["AppID"])

appid = st.session_state.get("selected_appid")
if not appid:
    st.warning("Pick a game to view live data.")
    st.stop()

st.write(
    f"Fetching live data for **{st.session_state['selected_game_name']}** …"
)
data = get_live_game_info(appid, cc="gb", lang="en") or {}

tab_overview, tab_pricing, tab_reviews = st.tabs(["Overview", "Pricing", "Reviews"])

with tab_overview:
    st.subheader("Description")
    st.write(data.get("short_description", "—"))
    st.subheader("Developers")
    st.write(", ".join(data.get("developers", [])) or "—")

with tab_pricing:
    price = data.get("price_overview") or {}
    if price:
        st.metric("Current Price", f"${price['final']/100:.2f}")
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
