import pandas as pd


def transform(df: pd.DataFrame):
    # 1. Clean nulls
    cleaned_df = df.dropna()

    # 2. Clean names

    # 3. Standardize dates/currencies/etc.

    # 4.return data
    return cleaned_df
