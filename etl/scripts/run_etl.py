import os
import sys
from config.env_config import setup_env
from src.extract.extract import extract
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

    # Pass the engine to the extract function which pulls data from database
    data = extract(engine)
    print(
        f"ETL pipeline run successfully in "
        f"{os.getenv('ENV', 'error')} environment!"
    )


if __name__ == "__main__":
    main()
