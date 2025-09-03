from app.database.sqlite_repository import select_multiple
from app.model.channel import Channel
from app.service.filter_service import get_filter_by_id
from app.service.video_platform_service import get_video_platform_by_id

_TABLE = "channels"

# <editor-fold desc="QUERIES -- GET">
_SQL_GET_ALL_CONFIGURED_CHANNELS = f"""
    SELECT * FROM {_TABLE} t 
"""
# </editor-fold>


def get_all_configured_channels() -> list[Channel]:
    """
    Return the configured channels in the database
    :return: the list of mapped entities
    """
    return _find_all(query=_SQL_GET_ALL_CONFIGURED_CHANNELS)


def _find_all(query: str) -> list[Channel]:
    """
    Raw fetch logic that performs the query and mapping to entities
    :param query: the fetch query
    :return: the mapped results
    """
    mapped_results = []
    results = select_multiple(query=query, params=())
    for result in results:
        filter_id = result[5]

        if filter_id is not None:
            filter_id = get_filter_by_id(filter_id)

        provider_id = result[3]
        provider = get_video_platform_by_id(provider_id)

        dto = Channel(result[0], result[1], result[2], provider, result[4], filter_id)
        mapped_results.append(dto)
    return mapped_results
