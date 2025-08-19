import streamlit as st
import pandas as pd
from ..utils.types import Filters


def render_sidebar_filters(df: pd.DataFrame) -> Filters:
    st.sidebar.header("Steam Games (April 2025)")

    min_year, max_year, min_price, max_price, tag_options = get_filter_bounds(df)

    year_range = st.sidebar.slider(
        "Release Year", min_year, max_year, (min_year, max_year)
    )

    price_range = st.sidebar.slider(
        "Price Range",
        min_price,
        max_price,
        (min_price, max_price),
        step=0.5,
        format="$%.2f",
    )

    tags = st.sidebar.multiselect("Tags", tag_options)

    platform = st.sidebar.radio("Platform", ["All", "Windows", "Mac", "Linux"])

    return Filters(year_range, price_range, tags, platform)

@st.cache_data
def get_filter_bounds(df: pd.DataFrame):
    """Cache min/max values."""
    min_year, max_year = int(df["Release Year"].min()), int(df["Release Year"].max())
    min_price, max_price = float(df["Price"].min()), float(df["Price"].max())
    tag_options = (
        df["Tags"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .unique()
    )
    return min_year, max_year, min_price, max_price, sorted(tag_options)