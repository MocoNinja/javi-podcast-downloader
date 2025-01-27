from sqlite3 import IntegrityError

from app.video.video_dto import VideoDto
from app.database import conn

from app.config import ROOT_LOGGER as log

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
    params = (channel_id, source_id, 0)
    # TODO: hacer un decorador de esto wapo simplemente por sacarse la chorra
    log.debug(
        f"""Getting videos that are not already downloaded
        | SQL: {_SQL_GET_VIDEOS_BY_CHANNEL_PLATFORM_AND_DOWNLOADED_FLAG}
        | PARAMS: {params}
    """
    )

    cursor = conn.cursor()

    try:
        cursor.execute(_SQL_GET_VIDEOS_BY_CHANNEL_PLATFORM_AND_DOWNLOADED_FLAG, params)
    except Exception as e:
        log.error(
            f"Unexpected error when getting all videos by channel {channel_id} and source {source_id}: {e}"
        )
    return cursor.fetchall()


def save_video(video: VideoDto, channel_id: int, provider_id: int):
    params = (
        video.video_title,
        False,
        channel_id,
        video.video_id,
        video.video_url,
        provider_id,
    )
    log.debug(
        f"""Saving video
        | SQL: {_SQL_INSERT_VIDEO}
        | PARAMS: {params}
    """
    )
    try:
        conn.execute(_SQL_INSERT_VIDEO, params)
    except IntegrityError as e:
        log.warn(f"Skipping dupe item {video}. Error: {e}")
    except Exception as e:
        log.error(f"Unexpected error when saving video {video}: {e}")


def set_video_as_downloaded(video: VideoDto):
    sql_params = (
        1,
        video[0],
    )  # Recordar para el futuro que python es un hdlgp oligofrénico y si la query es un solo param, es (item[0],)
    conn.execute(_SQL_UPDATE_VIDEO_DOWNLOADED_FLAG, sql_params)
    conn.commit()
