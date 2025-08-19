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
            "Estimated owners",
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

    # Write data

    # Make sure directory exists
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # Save to CSV
    df_no_dupes.to_csv(output_csv, index=False)

    # 5.return data
    return df_no_dupes


def clean_nulls(df: pd.DataFrame, columns: [str]) -> pd.DataFrame:
    cleaned_df = df.dropna(subset=columns).copy()
    return cleaned_df
