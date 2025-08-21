import streamlit as st
import pandas as pd


def games_table(df: pd.DataFrame):
    df = df.copy().rename(columns={'Price': 'Price ($)'})

    # Format Price: 0 -> "FREE"
    df["Price ($)"] = df["Price ($)"].apply(
        lambda x: "FREE" if x == 0 else f"${x:.2f}"
    )

    st.subheader("Steam Store Games")
    st.dataframe(
        df[["Name", "Price ($)", "Tags", "Sentiment", "Peak CCU", "Release Year", "Developers", "Available platforms"]].head(500),
        use_container_width=True,
        hide_index=True,
    )
