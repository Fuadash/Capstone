import plotly.express as px
import pandas as pd


def releases_per_year(df: pd.DataFrame):
    counts = df.groupby("Release Year").size().reset_index(name="count")
    return px.line(
        counts,
        x="Release Year",
        y="count",
        markers=True,
        title="Number of Games Released per Year",
    )


def avg_price_per_year(df: pd.DataFrame):
    avg = df.groupby("Release Year")["Price"].mean().reset_index()
    return px.line(
        avg,
        x="Release Year",
        y="Price",
        markers=True,
        title="Average Game Price per Year",
    )


def price_distribution(df: pd.DataFrame):
    return px.histogram(df, x="Price", nbins=10, title="Distribution of Game Prices")


def rating_distribution(df: pd.DataFrame):
    order = [
        "No Reviews",
        "Overwhelmingly Negative",
        "Very Negative",
        "Mostly Negative",
        "Negative",
        "Mixed",
        "Positive",
        "Mostly Positive",
        "Very Positive",
        "Overwhelmingly Positive",
    ]
    return px.bar(
        df,
        x="Sentiment",
        title="Distribution of Game Sentiment",
        category_orders={"Sentiment": order},
    )
