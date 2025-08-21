import pandas as pd
import os


def transform(
    df: pd.DataFrame, output_csv: str = "data/processed/processed_data.csv"
) -> pd.DataFrame:
    # 0. Drop colummns
    df.drop(
        columns=[
            "Discount",
            "DLC count",
            "Header image",
            "Achievements",
            "Average playtime forever",
            "Average playtime two weeks",
            "Median playtime forever",
            "Median playtime two weeks",
            "Screenshots",
            "Movies",
            "Score rank",
            "User score",
            "Estimated owners",
            "About the game",
            "Reviews",
            "Website",
            "Support url",
            "Support email",
            "Metacritic url",
            "Publishers"
        ],
        inplace=True,
    )

    # 0.5. Clean nulls
    cleaned_df = clean_nulls(
        df=df,
        columns=[
            "AppID",
            "Name",
            "Release date",
            "Peak CCU",
            "Required age",
            "Price",
            "Supported languages",
            "Full audio languages",
            "Windows",
            "Mac",
            "Linux",
            "Metacritic score",
        ],
    )

    # 0.75 Remove games without supported languages
    cleaned_df = cleaned_df[cleaned_df["Supported languages"] != "[]"]

    # 1. Fix types from float back to int
    cleaned_df["AppID"] = cleaned_df["AppID"].astype("Int64")
    cleaned_df["Peak CCU"] = cleaned_df["Peak CCU"].astype("Int64")
    cleaned_df["Required age"] = cleaned_df["Required age"].astype("Int64")
    cleaned_df["Metacritic score"] = cleaned_df["Metacritic score"].astype("Int64")
    cleaned_df["Positive"] = cleaned_df["Positive"].astype("Int64")
    cleaned_df["Negative"] = cleaned_df["Negative"].astype("Int64")
    cleaned_df["Recommendations"] = cleaned_df["Recommendations"].astype("Int64")

    # 2 Drop Duplicates

    df_no_dupes = cleaned_df.drop_duplicates()

    # 3. Standardize dates/currencies/etc.
    df_no_dupes["Release date"] = pd.to_datetime(
        df_no_dupes["Release date"], errors="coerce"
    )
    df_no_dupes["Release date"] = df_no_dupes["Release date"].dt.strftime("%Y-%m-%d")

    # 4. Convert required age to boolean
    df_no_dupes["Age restricted"] = df_no_dupes["Required age"].apply(lambda x: x >= 12)
    df_no_dupes = df_no_dupes.drop(columns=["Required age"])

    # 5. Remove outlier game prices
    df_no_dupes = df_no_dupes.loc[df['Price'] <= 100]

    # 6. Enrichment
    enriched_df = enrich_reviews(df_no_dupes)

    enriched_df = enrich_platforms(enriched_df)

    enriched_df = enrich_tags(enriched_df)

    # Write data

    # Make sure directory exists
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # Save to CSV
    enriched_df.to_csv(output_csv, index=False)

    # 5.return data
    return enriched_df


def clean_nulls(df: pd.DataFrame, columns: [str]) -> pd.DataFrame:
    cleaned_df = df.dropna(subset=columns).copy()
    return cleaned_df


def enrich_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes the "Positive" and "Negative" fields of a dataframe,
    referring to the reviews of a game.
    Adds:
    - A "Positive %" column
    - "Sentiment" column with categories:
        Overwhelmingly Positive, Very Positive, Positive,
        Mixed, Negative, Mostly Negative, Very Negative,
        Overwhelmingly Negative
    """
    #df = df.copy()

    # Calculate Positive %
    df["Total"] = df["Positive"] + df["Negative"]
    df["Positive %"] = ((df["Positive"] / df["Total"]) * 100).round()
    df["Positive %"] = df["Positive %"].astype("Int64")
    df.loc[df["Total"] == 0, "Positive %"] = pd.NA

    # axis=1 applies function to each row
    df["Sentiment"] = df.apply(get_sentiment, axis=1)

    return df.drop(columns=["Total"])


def get_sentiment(row):
    pos_pct = row["Positive %"]
    total = row["Total"]

    # Handle no reviews
    if pd.isna(pos_pct):
        return "No Reviews"

    pos_pct = int(pos_pct)

    if 40 <= pos_pct <= 69:
        return "Mixed"
    if 70 <= pos_pct <= 79:
        return "Mostly Positive"
    if 20 <= pos_pct <= 39:
        return "Mostly Negative"

    if pos_pct >= 80:
        if total >= 500 and pos_pct >= 95:
            return "Overwhelmingly Positive"
        elif total >= 50:
            return "Very Positive"
        else:
            return "Positive"

    if pos_pct <= 19:
        if total >= 500:
            return "Overwhelmingly Negative"
        elif total >= 50:
            return "Very Negative"
        else:
            return "Negative"

    # should never reach this
    return "No Reviews"


def enrich_platforms(df: pd.DataFrame) -> pd.DataFrame:
    """
    Combines Windows, Mac, Linux into "Available platforms"
    Example: "Windows, Mac, Linux" or "Mac, Linux".
    """
    #df = df.copy()

    platforms = ["Windows", "Mac", "Linux"]
    df["Available platforms"] = df.apply(
        lambda row: ", ".join([p for p in platforms if row[p]]),
        axis=1
    )

    return df

def enrich_tags(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a placeholder tag to the DataFrame when the "Tags" column is null.
    """
    df = df.copy()
    df["Tags"] = df["Tags"].fillna("No user-submitted tags available")
    return df