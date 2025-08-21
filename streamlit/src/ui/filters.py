import streamlit as st
import pandas as pd
from ..utils.types import Filters

# Credit to stackoverflow https://stackoverflow.com/questions/74968179/session-state-is-reset-in-streamlit-multipage-app

def keep(key: str):
    """Commit widget value (_key) to permanent app state (key)."""
    st.session_state[key] = st.session_state["_" + key]


def unkeep(key: str):
    """Initialize widget value (_key) from permanent app state (key)."""
    st.session_state["_" + key] = st.session_state[key]


def render_sidebar_filters(df: pd.DataFrame) -> Filters:
    st.sidebar.header("Steam Games (April 2025)")

    min_year, max_year, min_price, max_price, sentiment_options, tag_options = (
        get_filter_bounds(df)
    )

    defaults = {
        "year_range": (min_year, max_year),
        "price_range": (min_price, max_price),
        "sentiment": [],
        "tags": [],
        "platform": "All",
        "nsfw": "No"
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
        unkeep(key)  # copy permanent -> temporary

    # Widgets bind to temporary (_key)
    st.sidebar.slider(
        "Release Year",
        min_value=min_year,
        max_value=max_year,
        key="_year_range",
        on_change=keep,
        args=["year_range"]
    )

    st.sidebar.slider(
        "Price Range",
        min_price,
        max_price,
        step=1.0,
        format="$%.2f",
        key="_price_range",
        on_change=keep,
        args=["price_range"]
    )

    st.sidebar.multiselect(
        "Review Sentiment",
        sentiment_options,
        key="_sentiment",
        on_change=keep,
        args=["sentiment"]
    )

    st.sidebar.multiselect(
        "Tags",
        tag_options,
        key="_tags",
        on_change=keep,
        args=["tags"]
    )

    st.sidebar.radio(
        "Platform",
        ["All", "Windows", "Mac", "Linux"],
        key="_platform",
        on_change=keep,
        args=["platform"]
    )

    st.sidebar.radio(
        "Display Age Restricted Content?",
        ["Yes", "No"],
        key="_nsfw",
        on_change=keep,
        args=["nsfw"]
    )

    # Return state
    return Filters(
        st.session_state["year_range"],
        st.session_state["price_range"],
        st.session_state["sentiment"],
        st.session_state["tags"],
        st.session_state["platform"],
        st.session_state["nsfw"]
    )


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
