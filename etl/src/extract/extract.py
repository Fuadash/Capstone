import sys
from sqlalchemy import Engine
from sqlalchemy import text


def extract(engine: Engine):
    """Extracts data from the database"""

    # Test the connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("PostgreSQL version:", result.scalar())


if __name__ == "__main__":
    extract(sys.argv)
