import functools
import re
from app.common.logger import ROOT_LOGGER as log


def sql_logger(func):
    """Decorator to log a query at debug (TODO? Config?)
    :param func: the query that will be logged. MUST HAVE "query" FIELD
    :return:
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        name = func.__name__
        sql = kwargs.get("query", None)
        params = {key: value for key, value in kwargs.items() if key != "query"}
        # Clean format for logging
        if name is not None and sql is not None:
            sql = re.sub(r"\s+", " ", sql.strip())
            name = name.strip()

            log.debug(
                f"""Query: {name}
                        -> SQL: {sql}
                        -> Params: {params}
                    """
            )
        return func(*args, **kwargs)

    return wrapper
