import sqlite3
from decathlon_scrap import config

"""
Create a new database with a bike table if it doesn't exist.

Parameters:
database_name : the name of the database file. It will be created in the data folder.
"""


def create_db(path_db):
    path = path_db
    conn = None
    try:
        conn = sqlite3.connect(path)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS bike (
                        id INTEGER PRIMARY KEY,
                        bike_name TEXT,
                        price INTEGER,
                        bike_link TEXT,
                        XXS TEXT,
                        XS TEXT,
                        S TEXT,
                        M TEXT,
                        L TEXT,
                        XL TEXT
                    )              
                """
            )
            conn.commit()
            conn.close()


if __name__ == "__main__":

    create_db(config.DB_PATH)
