import os
import sys
from config.env_config import setup_env
from src.extract.extract import extract
from src.transform.transform import transform
from src.load.load import load
from config.db_config import load_db_config
from src.utils.connection_utils import get_connection_url
from sqlalchemy import create_engine


def main():
    # Get the argument from the run_etl command and set up the environment
    setup_env(sys.argv)

    # Load the db config (fills config with environment variables)
    config = load_db_config()

    # Choose source db, then create the connection url
    source_db = config["source_database"]
    url = get_connection_url(source_db)

    # Create SQLAlchemy engine from the url
    engine = create_engine(url)

    # Pass the engine (or dont) to the extract function which pulls data from database
    print("Running extract function...")
    data = extract(input_csv="data/raw/input.csv",
                   output_csv="data/raw/output.csv")

    # Print data for testing purposes
    # Also print number of nulls to compare later
    # TODO: Actually use logging framework
    print(data)
    print(f'DataFrame contains {data.isna().sum().sum()} null values')

    # Pass data to transform function
    transformed_data = transform(data)

    # Print number of nulls to compare after cleaning
    print(f'Transformed DataFrame contains {transformed_data.isna().sum().sum()} null values')

    # Pass everything into the load function
    load(
        df=transformed_data,
        engine=engine,
        schema="de_2506_a",
        table_name="fa_steam_final"
    )

    print(
        f"ETL pipeline run successfully in "
        f"{os.getenv('ENV', 'error')} environment!"
    )


if __name__ == "__main__":
    main()
