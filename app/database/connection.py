import sqlite3
from os import path
from pathlib import Path
from app.common.logger import ROOT_LOGGER as log
import os
import sys

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
    var = os.path.dirname(sys.modules["__main__"].__file__)
    var2 = Path(var).parent
    curr_dir_for_this_file = path.dirname(
        path.abspath(__file__)
    )  # Current directory of this file
    db_path = path.join(curr_dir_for_this_file, "..", "..", "resources", filename)
    return db_path


def _initialize():
    _load_database()


_initialize()
