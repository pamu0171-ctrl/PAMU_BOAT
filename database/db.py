
import sqlite3

from PAMU_BOAT.config import DB_PATH


def connect():

    return sqlite3.connect(DB_PATH)
