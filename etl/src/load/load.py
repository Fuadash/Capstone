import pandas as pd
from sqlalchemy import Engine


# This creates the table and appends the data
def load(df: pd.DataFrame, engine: Engine, table_name: str, schema):
    """
    Imports data from a DataFrame into a database
    Is passed a DataFrame and an Engine
    Along with the target schema and table name
    """
    # Now append the data
    df.to_sql(
        name=table_name,
        con=engine,
        schema=schema,
        if_exists="replace",
        index=False,
        method="multi",
    )
