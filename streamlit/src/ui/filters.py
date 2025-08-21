import streamlit as st
import pandas as pd
from ..utils.types import Filters


def render_sidebar_filters(df: pd.DataFrame) -> Filters:
    st.sidebar.header("Steam Games (April 2025)")

    min_year, max_year, min_price, max_price, sentiment_options, tag_options = (
        get_filter_bounds(df)
    )

    year_range = st.sidebar.slider(
        "Release Year", min_value=min_year, max_value=max_year, value=()
    )

    price_range = st.sidebar.slider(
        "Price Range",
        min_price,
        max_price,
        value=(min_price, max_price),
        step=1.0,
        format="$%.2f",
    )

    sentiment = st.sidebar.multiselect(
        "Review Sentiment", sentiment_options, key="render_sentiment"
    )

    tags = st.sidebar.multiselect("Tags", tag_options, key="render_tags")

    platform = st.sidebar.radio(
        "Platform", ["All", "Windows", "Mac", "Linux"], key="render_platform"
    )

    nsfw = st.sidebar.radio(
        "Display Age Restricted Content?", ["Yes", "No"], key="render_nsfw"
    )

    return Filters(year_range, price_range, sentiment, tags, platform, nsfw)


@st.cache_data
def get_filter_bounds(df: pd.DataFrame):
    """Cache values."""
    min_year, max_year = int(df["Release Year"].min()), int(df["Release Year"].max())
    min_price, max_price = float(df["Price"].min()), float(df["Price"].max())
    tag_options = df["Tags"].dropna().str.split(",").explode().str.strip().unique()
    sentiment_options = df["Sentiment"].unique()
    order = [
        "Overwhelmingly Positive",
        "Very Positive",
        "Mostly Positive",
        "Positive",
        "Mixed",
        "Negative",
        "Mostly Negative",
        "Very Negative",
        "Overwhelmingly Negative",
        "No Reviews"
    ]
    return (
        min_year,
        max_year,
        min_price,
        max_price,
        sorted(
            sentiment_options,
            key=lambda x: order.index(x) if x in order else len(order),
        ),
        sorted(tag_options),
    )
