import pandas as pd
import os
from sqlalchemy import Engine
from sqlalchemy import text


# TODO: Make it so that extract is passed a SQL query instead of making it
def extract(
    engine: Engine, output_csv: str = "data/raw/output.csv"
) -> pd.DataFrame:
    """
    Extracts data from the database, saves to CSV, and returns a DataFrame
    Takes a database engine and an output csv path
    """

    query = text('SELECT * FROM "de_2506_a"."fa_steam"')

    with engine.connect() as conn:
        # Load query results directly into a DataFrame
        df = pd.read_sql(query, conn)

    # Make sure directory exists
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # Save to CSV
    df.to_csv(output_csv, index=False)

    return df
