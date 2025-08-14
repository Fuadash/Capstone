import sys
from sqlalchemy import Engine
from sqlalchemy import text


def extract(engine: Engine):
    """Extracts data from the database"""

    #query = text('SELECT * FROM "main"."actor"')
    query = text('SELECT * FROM "de-2506-a"."fa_steam"')

    # Test the connection
    with engine.connect() as conn:
        result = conn.execute(query)

        # Fetch all rows
        rows = result.fetchall()

        # Optionally print them
        for row in rows:
            print(row)

    return rows


if __name__ == "__main__":
    extract(sys.argv)
