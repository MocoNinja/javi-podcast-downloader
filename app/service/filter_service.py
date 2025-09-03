import logging

from app.database.sqlite_repository import select_single
from app.model.video_filter import VideoFilterConfiguration

_TABLE: str = "video_filters"

# <editor-fold desc="QUERIES -- GET">
_SQL_GET_FILTER_BY_ID = f"""
    SELECT id, video_title_regex FROM {_TABLE} t 
        WHERE  t.id = ( ? )
"""
# </editor-fold>


def get_filter_by_id(filter_id: int) -> VideoFilterConfiguration | None:
    """
    Find the configured filter in database with the given id
    :param filter_id: the id in the database
    :return: the filter entity or None if not found
    """
    return _find_single_with_params(query=_SQL_GET_FILTER_BY_ID, filter_field=filter_id)


def _find_single_with_params(
    query: str, filter_field: int | str
) -> VideoFilterConfiguration | None:
    """
    Raw logic to fetch a single item of filters by a param
    :param query: the fetch query
    :param filter_field: the field to create params from
    :return: the mapped item
    """
    params = (filter_field,)
    result = select_single(query=query, params=params)

    if result is None:
        logging.info(f"Filter with id '{filter_field}' was not found.")
        return result

    return VideoFilterConfiguration(result[0], result[1])
