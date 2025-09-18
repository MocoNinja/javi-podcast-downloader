from os import path
from sqlite3 import Connection, connect

from app.common.logger import debug, fatal, info

_conn: Connection | None = None

"""
    Store the connection to the SQLite database that is used for persistent storage among the app.
"""


def get_connection():
    """
    Obtain the connection to the database
    :return: the connection item
    """
    global _conn
    if _conn is None:
        load_database()
    return _conn


def load_database() -> Connection:
    """
    Obtain a connection to the sqlite database if it was not done before, or just return it so it can be used.
    Failing to obtain a connection is a fatal error and the application is thus terminated.
    :return: the connection
    """
    global _conn
    if _conn is not None:
        return _conn
    debug("Creating connection to database")

    db = _get_database_path()
    info(f"Loaded database {db}")
    if not path.exists(db):
        fatal(
            f"The database file does not exist at: {db}. Cannot proceed with the application."
        )
        exit(1)
    _conn = connect(db)
    return _conn


def _get_database_path(filename="database.db"):
    """
    Obtain the actual path for the database file.
    :param filename: the filename
    :return: the path that consists on appending the arg filename to the expected resources folder
    """
    # var = os.path.dirname(sys.modules["__main__"].__file__)
    # var2 = Path(var).parent
    curr_dir_for_this_file = path.dirname(path.abspath(__file__))
    db_path = path.join(curr_dir_for_this_file, "..", "..", "resources", filename)
    return db_path
