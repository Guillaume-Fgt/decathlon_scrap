from decathlon_scrap import create_db
import os
import sqlite3


def test_create_db():
    """test if db is created"""
    path = "decathlon_scrap/data/app_test.db"
    create_db.create_db(path)
    assert os.path.isfile(path) == True
    os.remove(path)


def test_connect_db():
    "test if connection to newly created db is ok"
    path = "decathlon_scrap/data/app_test.db"
    create_db.create_db(path)
    conn = sqlite3.connect(path)
    assert isinstance(conn, sqlite3.Connection) == True
    conn.close()
    os.remove(path)
