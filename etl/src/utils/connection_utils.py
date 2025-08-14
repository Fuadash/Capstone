def get_connection_url(db_settings: dict) -> str:
    """
    Builds a PostgreSQL connection URL for SQLAlchemy.
    Takes in a DB settings dictionary
    """
    return (
        f"postgresql+psycopg2://{db_settings['user']}:{db_settings['password']}"
        f"@{db_settings['host']}:{db_settings['port']}/{db_settings['dbname']}"
    )