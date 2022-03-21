import sqlite3
import config
from contextlib import contextmanager

"""module to handle all operations needed on the database"""


@contextmanager
def open_db(file_name: str):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    try:
        cursor = connection.cursor()
        yield cursor
    finally:
        connection.commit()
        connection.close()


def create_database(db_path: str) -> None:
    """Create a new database at the given path_db location with a bike table if it doesn't exist"""
    with open_db(db_path) as cursor:
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


def connect_database(db_path: str) -> tuple[sqlite3.Cursor, sqlite3.Connection]:
    """Create a connection to the database"""
    try:
        connection = sqlite3.connect(db_path)
    except sqlite3.OperationalError as e:
        print(f'{e}. Please check path "{db_path}" is correct')
        return
    connection.row_factory = sqlite3.Row
    return connection.cursor(), connection


def populate_database(db_path: str, bike: str, price: int, link: str) -> None:
    """populate a database with data providing from scrapping"""
    with open_db(db_path) as cursor:
        for ind, bike in enumerate(bike):
            cursor.execute(
                "INSERT INTO bike (bike_name, price, bike_link) VALUES (?, ?, ?)",
                (
                    bike,
                    price[ind],
                    link[ind],
                ),
            )


if __name__ == "__main__":
    create_database(config.DB_PATH)
