import plotly.express as px
import pandas as pd


def releases_per_year(df: pd.DataFrame):
    # Count number of games released by year
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
    # Stops fig from exploding if it has no values
    # Might be redundant
    if not df.empty and not df["Price"].empty:
        fig.update_traces(
            xbins=dict(start=0, end=df["Price"].max(), size=5)
        )
    else:
        fig.update_traces(
            xbins=dict(start=0, end=0, size=1)
        )
    
    # Colours
    num_bins = len(fig.data[0].x)  # number of bins
    colors = [px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i in range(num_bins)]
    fig.data[0].marker.color = colors
    return fig


def rating_distribution(df: pd.DataFrame):
    counts = df.groupby("Sentiment").size().reset_index(name="count")
    # Sets the order for the figure
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

def score_by_genre(df: pd.DataFrame):
    # Drop rows without tags or score
    df = df.dropna(subset=["Tags", "Positive %"])

    # Split tags into lists then explodes them into separate rows
    df["Tags"] = df["Tags"].str.split(",")
    exploded = df.explode("Tags")
    exploded["Tags"] = exploded["Tags"].str.strip()  # remove extra spaces

    # Find top 10 most common tags
    top_tags = exploded["Tags"].value_counts().nlargest(10).index

    # Filter to top tags only
    filtered = exploded[exploded["Tags"].isin(top_tags)]

    # Compute average Positive % for each tag
    avg_scores = (
        filtered.groupby("Tags")["Positive %"]
        .mean()
        .reset_index()
        .sort_values("Positive %", ascending=False)
    )

    # Plot bar chart
    fig = px.bar(
        avg_scores,
        x="Tags",
        y="Positive %",
        title="Average Positive % of Most Common Genres",
        labels={
            "Tags": "Genre",
            "Positive %": "Average Positive %",
        },
        color="Positive %",
        color_continuous_scale="Blues",
    )
    return fig
