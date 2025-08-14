import os
import sys
from config.env_config import setup_env
from src.extract.extract import extract
from config.db_config import load_db_config


def main():
    # Get the argument from the run_etl command and set up the environment
    setup_env(sys.argv)
    # Load the db config
    config = load_db_config()
    # Pass the db config to the extract function which will then pull data from the database
    data = extract(config)
    print(
        f"ETL pipeline run successfully in "
        f"{os.getenv('ENV', 'error')} environment!"
    )


if __name__ == "__main__":
    main()
