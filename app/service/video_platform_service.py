from app.common.logger import info
from app.database.sqlite_repository import select_multiple, select_single
from app.model.video_platform import VideoPlatform

_TABLE: str = "video_providers"

# <editor-fold desc="QUERIES -- GET">
_SQL_GET_ALL_VIDEO_PLATFORMS = f"""
    SELECT id, name, video_base_url, channel_url_pattern FROM {_TABLE} t
"""
_SQL_GET_VIDEO_PLATFORM_BY_ID = f"""
    SELECT id, name, video_base_url, channel_url_pattern FROM {_TABLE} t
        WHERE  t.id = ( ? )
"""

_SQL_GET_VIDEO_PLATFORM_BY_NAME = f"""
    SELECT id, name, video_base_url, channel_url_pattern FROM {_TABLE} t 
        WHERE  t.enun_name = ( ? )
"""
# </editor-fold>


def get_all_video_platforms() -> list[VideoPlatform]:
    """
    Return all the video platforms
    :return: a list with the mapped entities
    """
    return _fetch_video_platforms(_SQL_GET_ALL_VIDEO_PLATFORMS)


def get_video_platform_by_id(video_platform_id: int) -> VideoPlatform | None:
    """
    Return the video platform corresponding to the given id
    :param video_platform_id: the id
    :return: the mapped entity or None if not exists
    """
    return _fetch_single_video_platform_by_field(
        query=_SQL_GET_VIDEO_PLATFORM_BY_ID, field=video_platform_id
    )


def get_video_platform_by_name(video_platform_name: str) -> VideoPlatform | None:
    """
    Return the video platform corresponding to the given name
    :param video_platform_name: the name
    :return: the mapped entity or None if not exists
    """
    return _fetch_single_video_platform_by_field(
        query=_SQL_GET_VIDEO_PLATFORM_BY_NAME, field=video_platform_name
    )


def _fetch_single_video_platform_by_field(
    query: str, field: int | str
) -> VideoPlatform | None:
    """
    Fetch a single video platform and map it to the entity
    :param query: to fetch the data
    :param field: to filter the data by
    :return: the found mapped entity or None if not found
    """
    params = (field,)
    result = select_single(query=query, params=params)

    if result is None:
        info(f"Video platform with field '{field}' was not found.")
        return result

    return VideoPlatform(result[0], result[1], result[2], result[2])


def _fetch_video_platforms(sql: str) -> list[VideoPlatform]:
    """
    Fetch multiple video platforms and map it to entities
    :param sql: to perform
    :return: the list of mapped entities. Will be empty if no matches
    """
    raw_items = select_multiple(query=sql, params=())
    mapped_items = []
    for item in raw_items:
        mapped_items.append(VideoPlatform(item[0], item[1], item[2], item[3]))
    return mapped_items
