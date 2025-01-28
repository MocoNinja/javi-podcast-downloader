from sqlite3 import IntegrityError

from app.common.decorators import sql_logger
from app.database.connection import conn
from app.video.video_dto import VideoDto

from app.common.logger import ROOT_LOGGER as log

_VIDEO_TABLE = "videos"

# <editor-fold desc="QUERIES -- INSERT">
_SQL_INSERT_VIDEO = f"""
    INSERT INTO {_VIDEO_TABLE}
            (title, downloaded, channel_id, video_id, video_url, video_platform_id)
        VALUES
            (?, ?, ?, ?, ?, ?)
"""
# </editor-fold>

# <editor-fold desc="QUERIES -- GET">
_SQL_GET_VIDEOS_BY_CHANNEL_PLATFORM_AND_DOWNLOADED_FLAG = f"""
    SELECT * FROM {_VIDEO_TABLE}
        WHERE channel_id = ?
            AND video_platform_id = ?
            AND downloaded = ?
"""
# </editor-fold>

# <editor-fold desc="QUERIES -- UPDATE">
_SQL_UPDATE_VIDEO_DOWNLOADED_FLAG = f"""
    UPDATE {_VIDEO_TABLE}
        SET downloaded = ?
        WHERE id = ?
"""
# </editor-fold>


def get_not_already_downloaded_videos(channel_id: int, source_id: int):
    return find_videos_by_channel_source_and_download_status(
        query=_SQL_GET_VIDEOS_BY_CHANNEL_PLATFORM_AND_DOWNLOADED_FLAG,
        channel_id=channel_id,
        source_id=source_id,
        downloaded_flag=0,
    )


def save_video(video: VideoDto, channel_id: int, provider_id: int):
    return insert_video(
        query=_SQL_INSERT_VIDEO,
        video_title=video.video_title,
        downloaded_flag=False,
        channel_id=channel_id,
        video_id=video.video_id,
        video_url=video.video_url,
        provider_id=provider_id,
    )


def set_video_as_downloaded(video: VideoDto):
    return update_video_downloaded_flag(
        query=_SQL_UPDATE_VIDEO_DOWNLOADED_FLAG, id=video[0], status=1
    )


@sql_logger
def find_videos_by_channel_source_and_download_status(
    query: str, channel_id: int, source_id: int, downloaded_flag: int
):
    params = (channel_id, source_id, 0)
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
    except Exception as e:
        log.error(
            f"Unexpected error when getting all videos by channel {channel_id} and source {source_id}: {e}"
        )
    return cursor.fetchall()


@sql_logger
def insert_video(
    query: str,
    video_title: str,
    downloaded_flag: int,
    channel_id: int,
    video_id: str,
    video_url: str,
    provider_id: int,
):
    params = (
        video_title,
        downloaded_flag,
        channel_id,
        video_id,
        video_url,
        provider_id,
    )
    try:
        conn.execute(query, params)
    except IntegrityError as e:
        log.warn(f"Skipping dupe item {video_title}. Error: {e}")
    except Exception as e:
        log.error(f"Unexpected error when saving video {video_title}: {e}")


@sql_logger
def update_video_downloaded_flag(query: str, id: str, status: int):
    # Recordar para el futuro que python es un hdlgp oligofrénico y si la query es un solo param, es (item[0],)
    sql_params = (status, id)
    conn.execute(query, sql_params)
    conn.commit()
