import pandas as pd
from .types import Filters


def apply_filters(df: pd.DataFrame, f: Filters) -> pd.DataFrame:
    output = df

    # Year filter
    output = output[
        (output["Release Year"] >= f.year_range[0])
        & (output["Release Year"] <= f.year_range[1])
    ]

    # Price filter
    output = output[
        (output["Price"] >= f.price_range[0])
        & (output["Price"] <= f.price_range[1])
    ]

    # Sentiment filter
    if f.sentiment:
        output = output[output["Sentiment"].isin(f.sentiment)]

    # Tag filter
    if f.tags:
        tag_set = set(f.tags)
        output = output[output["TagList"].apply(lambda tags: tag_set.issubset(tags))]

    # Platform filter
    if f.platform != "All":
        output = output[output[f.platform] == True]

    # NSFW content filter
    if f.nsfw == "No" and "Age restricted" in output.columns:
        output = output[output["Age restricted"] != True]

    return output
