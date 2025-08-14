import sys
from sqlalchemy import create_engine, text
from typing import Dict
from src.utils.connection_utils import get_connection_url


def extract(config: Dict[str, Dict[str, str]]):
    """Extracts data from the database"""
    # Choose source db
    source_db = config["source_database"]
    url = get_connection_url(source_db)

    # 3. Create SQLAlchemy engine
    engine = create_engine(url)

    # 4. Test the connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("PostgreSQL version:", result.scalar())


if __name__ == "__main__":
    extract(sys.argv)
