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
    fig = px.line(
        avg,
        x="Release Year",
        y="Price",
        markers=True,
        title="Average Game Price per Year",
    )
    return fig


def price_distribution(df: pd.DataFrame):
    fig = px.histogram(
        df,
        x="Price",
        nbins=20,
        title="Distribution of Game Prices",
        labels={
            "Price": "Price ($)",
        },
    )
    if not df.empty and not df["Price"].empty:
        fig.update_traces(
            xbins=dict(start=0, end=df["Price"].max(), size=5)
        )
    else:
        fig.update_traces(
            xbins=dict(start=0, end=0, size=1)
        )
    num_bins = len(fig.data[0].x)  # number of bins
    colors = [px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i in range(num_bins)]
    fig.data[0].marker.color = colors
    return fig


def rating_distribution(df: pd.DataFrame):
    counts = df.groupby("Sentiment").size().reset_index(name="count")
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

    fig = px.bar(
        counts,
        x="Sentiment",
        y="count",
        title="Distribution of Game Sentiment",
        category_orders={"Sentiment": order},
        color='Sentiment',
        color_continuous_scale='Plotly',
        labels={
            "Sentiment": "Review Sentiment",
        },
    )
    return fig
