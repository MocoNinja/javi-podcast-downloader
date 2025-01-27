import sqlite3
from os import path
from app.config import ROOT_LOGGER as log

conn = None


def _load_database():
    global conn
    if conn is not None:
        return conn
    log.info("Creating connection to database")

    db = _get_database_path()
    log.info(f"Loaded database {db}")
    if not path.exists(db):
        log.fatal(f"The database file does not exist at: {db}")
        exit(1)
    conn = sqlite3.connect(db)
    return conn


"""
1) Menos hack -> ojo que al haber formalizado los módulos ni tan mal
2) Leer de config -> trivial ahora
"""


def _get_database_path(filename="database.db"):
    curr_dir_for_this_file = path.dirname(
        path.abspath(__file__)
    )  # Current directory of this file
    db_path = path.join(curr_dir_for_this_file, "..", "..", "resources", filename)
    return db_path


def _initialize():
    _load_database()


_initialize()
