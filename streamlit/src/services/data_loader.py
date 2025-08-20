import pandas as pd
import streamlit as st

# oh the things that had to be done to make this efficient
@st.cache_data(ttl=3600, show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Release date"] = pd.to_datetime(df["Release date"], errors="coerce")
    df["Release Year"] = df["Release date"].dt.year

    def safe_split(x):
        if pd.isna(x):  # if NaN
            return []
        return [t.strip() for t in str(x).split(",") if t.strip()]

    df["TagList"] = df["Tags"].apply(safe_split)

    return df.sort_values(by="Positive", ascending=False)
