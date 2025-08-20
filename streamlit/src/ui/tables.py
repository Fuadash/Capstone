import streamlit as st
import pandas as pd


def games_table(df: pd.DataFrame):
    st.subheader("Steam Store Games")
    st.dataframe(
        df[["Name", "Price", "Tags", "Release Year", "Developers", "Available platforms"]].head(500),
        use_container_width=True,
    )
