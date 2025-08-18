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
            "User score"
        ],
        inplace=True,
    )

    # 1. Clean nulls
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

    # 2. Clean names

    # 3. Standardize dates/currencies/etc.

    # 4. Convert required age to boolean

    # Write data

    # Make sure directory exists
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # Save to CSV
    cleaned_df.to_csv(output_csv, index=False)

    # 5.return data
    return cleaned_df


def clean_nulls(df: pd.DataFrame, columns: [str]) -> pd.DataFrame:
    cleaned_df = df.dropna(subset=columns)
    return cleaned_df
