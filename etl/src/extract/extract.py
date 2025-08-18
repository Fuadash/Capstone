import pandas as pd
import os
from sqlalchemy import Engine
from sqlalchemy import text
from typing import Optional


# TODO: Make it so that extract is passed a SQL query instead of making it
def extract(
    engine: Optional[Engine] = None,
    output_csv: str = "data/raw/output.csv",
    input_csv: str = "data/raw/input.csv",
    query: str = 'SELECT * FROM "de_2506_a"."fa_steam"',
) -> pd.DataFrame:
    """
    Extracts data from the database, saves to CSV, and returns a DataFrame
    Takes a database engine and an output csv path
    If the engine is None, will look for data/raw/input.csv
    """

    try:
        if engine is not None:
            with engine.connect() as conn:
                df = pd.read_sql(text(query), conn)
        else:
            if not os.path.exists(input_csv):
                raise FileNotFoundError(f"Input CSV not found: {input_csv}")
            df = pd.read_csv(input_csv)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)

        # Save to CSV
        df.to_csv(output_csv, index=False)

        return df

    # TODO: log things properly
    except Exception as e:
        raise e
