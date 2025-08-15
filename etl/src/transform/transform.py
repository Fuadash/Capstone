import pandas as pd
import os


def transform(
    df: pd.DataFrame, output_csv: str = "data/processed/processed_data.csv"
) -> pd.DataFrame:
    # 1. Clean nulls
    cleaned_df = df.dropna()

    # 2. Clean names

    # 3. Standardize dates/currencies/etc.

    # 4. Write data

    # Make sure directory exists
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # Save to CSV
    df.to_csv(output_csv, index=False)

    # 5.return data
    return cleaned_df
