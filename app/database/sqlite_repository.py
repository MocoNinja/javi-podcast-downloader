import logging
from sqlite3 import (
    Cursor,
    DataError,
    IntegrityError,
    InterfaceError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
)

from app.common.decorators import sql_logger
from app.database.connection import get_connection
from app.error.errors import DatabaseError, NonFatalDatabaseError

"""
    Wrapper to the raw sqlite3 methods to try and ease up queries.
"""


def _execute_query(query: str, params: tuple, commit: bool = False) -> Cursor:
    """Internal function to handle query execution and error handling."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if commit:
                conn.commit()
            return cursor

    except (DataError, ProgrammingError, InterfaceError) as e:
        err = DatabaseError(query, params, e, "error with query execution")
        logging.error(err)
        raise err

    except IntegrityError as e:
        err = NonFatalDatabaseError(
            query, params, e, "Error due to data integrity constraints"
        )
        logging.error(err)
        raise err

    except (
        OperationalError,
        InternalError,
        NotSupportedError,
        DatabaseError,
        Exception,
    ) as e:
        err = DatabaseError(query, params, e)
        logging.error(err)
        raise err


@sql_logger
def select_single(query: str, params: tuple) -> tuple:
    """
    Return a single element as a raw tuple
    :param query: to be performed
    :param params: to be used
    :return: the raw tuple
    """
    cursor = _execute_query(query, params)
    return cursor.fetchone()


@sql_logger
def select_multiple(query: str, params: tuple) -> list[tuple]:
    """
    Return several elements as a raw tuple
    :param query: to be performed
    :param params: to be used
    :return: the raw tuples
    """
    cursor = _execute_query(query, params)
    return cursor.fetchall()


@sql_logger
def insert(query: str, params: tuple) -> int:
    """
    Perform an insert query
    :param query: to be performed
    :param params: to be used
    :return: the count of affected items
    """
    cursor = _execute_query(query, params, commit=True)
    return cursor.rowcount


@sql_logger
def update(query: str, params: tuple) -> int:
    """
    Perform an update query
    :param query: to be performed
    :param params: to be used
    :return: the count of affected items
    """
    cursor = _execute_query(query, params, commit=True)
    return cursor.rowcount


@sql_logger
def delete(query: str, params: tuple) -> int:
    """
    Perform a delete query
    :param query: to be performed
    :param params: to be used
    :return: the count of affected items
    """
    cursor = _execute_query(query, params, commit=True)
    return cursor.rowcount
