from app.common.logger import debug
from app.database.sqlite_repository import (
    insert,
    select_multiple,
    select_single,
    update,
)
from app.error.errors import NonFatalDatabaseError, DatabaseError, FatalErrorException
from app.model.video import Video
from app.model.video_dto import VideoDto

_TABLE = "videos"

# <editor-fold desc="QUERIES -- INSERT">
_SQL_INSERT_VIDEO = f"""
    INSERT INTO {_TABLE}
            (title, downloaded, channel_id, video_id, video_url, video_platform_id)
        VALUES
            (?, ?, ?, ?, ?, ?)
"""
# </editor-fold>

# <editor-fold desc="QUERIES -- GET">
_SQL_GET_VIDEOS_BY_CHANNEL_PLATFORM_AND_DOWNLOADED_FLAG = f"""
    SELECT * FROM {_TABLE}
        WHERE channel_id = ?
            AND video_platform_id = ?
            AND downloaded = ?
"""

_SQL_CHECK_IF_VIDEO_WITH_ID_ALREADY_EXISTS = f"""
    SELECT id from {_TABLE}
       WHERE video_id = ?
LIMIT 1
"""
# </editor-fold>

# <editor-fold desc="QUERIES -- UPDATE">
_SQL_UPDATE_VIDEO_DOWNLOADED_FLAG = f"""
    UPDATE {_TABLE}
        SET downloaded = ?
        WHERE id = ?
"""
# </editor-fold>


def get_not_already_downloaded_videos(channel_id: int, source_id: int) -> list[Video]:
    """
    Find videos that have not been downloaded from channel and source
    :param channel_id: the channel
    :param source_id: the source
    :return:
    """
    downloaded_flag: int = 0
    return _fetch_videos(
        query=_SQL_GET_VIDEOS_BY_CHANNEL_PLATFORM_AND_DOWNLOADED_FLAG,
        params=(channel_id, source_id, downloaded_flag),
    )


def video_exists_by_video_id(video_id: int) -> bool:
    """
    Find id the given video exists in the database
    :param video_id:  the video to find
    :return: if we have it or not
    """
    result = select_single(
        query=_SQL_CHECK_IF_VIDEO_WITH_ID_ALREADY_EXISTS, params=(video_id,)
    )

    return result is not None


def save_video(video: VideoDto) -> None:
    """
    Insert  the given dto into database
    :param video: to save
    """
    _insert_video(query=_SQL_INSERT_VIDEO, video=video)


def save_videos(videos: list[VideoDto]) -> None:
    """
    Save the videos given in the list in individual transactions
    :param videos: to persist
    """
    for video in videos:
        save_video(video)


def set_video_as_downloaded(video: Video) -> None:
    """
    Mark the given video as downloaded in the database
    :param video: the downloaded
    """
    downloaded_status = 1
    updated_rows = _update_some_params(
        query=_SQL_UPDATE_VIDEO_DOWNLOADED_FLAG,
        params=(downloaded_status, video.id)
    )
    if updated_rows != 1:
        raise FatalErrorException(f"Expected flag was not updated for video: {video}")


def _fetch_videos(query: str, params: tuple) -> list[Video]:
    """
    Raw query to select multiple items
    :param query: the query
    :param params: the params
    :return:  the items mapped to VideoDto
    """
    mapped_results = []
    results = select_multiple(query, params)
    for result in results:
        if result[2] == 1:
            bool_result = True
        else:
            bool_result = False
        dto = Video(result[0], result[1], bool_result, result[3], result[5], result[6])
        mapped_results.append(dto)
    return mapped_results


def _insert_video(
    query: str,
    video: VideoDto,
) -> int | None:
    """
    Raw insert of a video dto
    :param query: to insert
    :param video: with the params
    :return: the amount of inserted items
    """
    try:
        return insert(
            query=query,
            params=(
                video.video_title,
                video.downloaded_flag,
                video.channel_id,
                video.video_id,
                video.video_url,
                video.provider_id,
            ),
        )
    except NonFatalDatabaseError as e:
        debug(
            f"Skipping dupe item {video.video_title}. Error: {e}. This is expected and we will continue."
        )


def _update_some_params(query: str, params: tuple) -> int:
    """
    Raw query that performs an update on several fields
    :param query: to update
    :param params: to set
    :return: the amount of updated items
    """
    return update(query=query, params=params)
