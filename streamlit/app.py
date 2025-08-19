import pandas as pd
import streamlit as st
import plotly.express as px
import requests


def get_live_game_info(appid: int):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=gb&lang=en"
    #url = f"https://store.steampowered.com/api/appdetails?appids=367520&cc=gb&lang=en"
    resp = requests.get(url)
    data = resp.json()
    if data[str(appid)]["success"]:
        return data[str(appid)]["data"]
    return None


def get_data() -> pd.DataFrame:
    df = pd.read_csv("../etl/data/processed/processed_data.csv")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Release date"] = pd.to_datetime(df["Release date"], errors="coerce")
    return df


df = get_data()

# FILTERS ----------------------

# Sidebar Filters
st.sidebar.header("Steam Games (April 2025)")

# Year filter
min_year = int(df["Release date"].dt.year.min())
max_year = int(df["Release date"].dt.year.max())
year_range = st.sidebar.slider("Release Year", min_year, max_year, (min_year, max_year))

# Price filter
min_price = float(df["Price"].min())
max_price = float(df["Price"].max())
price_range = st.sidebar.slider(
    "Price Range",
    min_price,
    max_price,
    (min_price, max_price),
    step=0.5,
    format="$%.2f",
)



# Tag filter
tag_options = df["Tags"].dropna().str.split(",").explode().str.strip().unique()
tag_filter = st.sidebar.multiselect("Tags", tag_options)

# Platform filter
platform_filter = st.sidebar.radio("Platform", ["All", "Windows", "Mac", "Linux"])

# Apply Filters --------
filtered_df = df.copy()

# year
filtered_df["Release Year"] = pd.to_datetime(
    filtered_df["Release date"], errors="coerce"
).dt.year
filtered_df = filtered_df[
    (filtered_df["Release Year"] >= year_range[0])
    & (filtered_df["Release Year"] <= year_range[1])
]

# price
filtered_df = filtered_df[
    (filtered_df["Price"] >= price_range[0]) & (filtered_df["Price"] <= price_range[1])
]

# tag
if tag_filter:
    filtered_df = filtered_df[
        filtered_df["Tags"].apply(lambda x: all(g in str(x) for g in tag_filter))
    ]

# platform
if platform_filter != "All":
    filtered_df = filtered_df[filtered_df[platform_filter] == True]

# --- Display Filtered Data ---
# Add the platforms in a field
st.subheader("Steam Store Games")
st.dataframe(
    filtered_df[["Name", "Release Year", "Price", "Developers", "Tags"]].head(500)
)

# After filtering we can display filtered data
game_name = st.sidebar.selectbox(
    "Select a Game",
    filtered_df["Name"].unique()
)

if game_name:
    game_row = filtered_df[filtered_df["Name"] == game_name].iloc[0]

    appid = int(game_row["AppID"])  

    st.write(f"Fetching live data for **{game_name}**...")
    ### UNCOMMENT BELOW FOR CAPSTONE
    # live_data = get_live_game_info(appid)

    # if live_data and "price_overview" in live_data:
    #     price_info = live_data["price_overview"]
    #     st.metric("Current Price", f"${price_info['final'] / 100:.2f}")
    #     st.metric("Discount", f"{price_info['discount_percent']}%")
    # else:
    #     st.warning("No live pricing info available for this game.")


# VISUALIZATIONS ------------------------------

# Releases each year
filtered_df["Release Year"] = pd.to_datetime(filtered_df["Release date"]).dt.year
release_counts = filtered_df.groupby("Release Year").size().reset_index(name="count")

fig1 = px.line(
    release_counts,
    x="Release Year",
    y="count",
    markers=True,
    title="Number of Games Released per Year",
)
st.plotly_chart(fig1, use_container_width=True)

# average game price per year
avg_price_per_year = filtered_df.groupby("Release Year")["Price"].mean().reset_index()

fig3 = px.line(
    avg_price_per_year,
    x="Release Year",
    y="Price",
    markers=True,
    title="Average Game Price per Year",
)
st.plotly_chart(fig3, use_container_width=True)

# game price distribution
fig4 = px.histogram(
    filtered_df,
    x="Price",
    nbins=10,
    title="Distribution of Game Prices",
)
st.plotly_chart(fig4, use_container_width=True)

# Price vs. Reviews, somehow
# Maybe review power (pos/neg reviews) across the years?
# top devs by number of games
# fit in the overwhelmingly positive etc. buckets

# STYLES ------
# Make sidebar wider
st.markdown(
    """
    <style>
    /* Sidebar width */
    [data-testid="stSidebar"] {
        min-width: 350px;
        max-width: 350px;
    }
    """,
    unsafe_allow_html=True
)
