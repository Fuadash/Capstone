import pandas as pd
from sqlalchemy import Engine


# This creates the table and appends the data
def load(
    df: pd.DataFrame, engine: Engine, table_name: str, schema: str, size: int = 10000
):
    """
    Imports data from a DataFrame into a database
    Is passed a DataFrame and an Engine
    Along with the target schema and table name
    """
    # Reduce the df size to not cause issues
    df_small = df.head(size).copy()

    print(len(df))
    print(len(df_small))

    df_small.reset_index(inplace=True)

    # Now append the data
    df_small.to_sql(
        name=table_name,
        con=engine,
        schema=schema,
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=1000,
    )
