import pandas as pd
import streamlit as st
import plotly.express as px


def get_data() -> pd.DataFrame:
    df = pd.read_csv("../etl/data/live/games.csv")
    return df


df = get_data()

#st.dataframe(df)

# Releases each year
df["year_release"] = pd.to_datetime(df["date_release"]).dt.year
release_counts = df.groupby("year_release").size().reset_index(name="count")

fig1 = px.line(
    release_counts,
    x="year_release",
    y="count",
    markers=True,
    title="Number of Games Released per Year",
)
st.plotly_chart(fig1, use_container_width=True)

# Games at each rating distribution
rating_counts = df["rating"].value_counts().reset_index()
rating_counts.columns = ["rating", "count"]

fig2 = px.bar(
    rating_counts, x="rating", y="count", title="Distribution of Game Ratings"
)
st.plotly_chart(fig2, use_container_width=True)

# Price vs. Reviews, somehow
