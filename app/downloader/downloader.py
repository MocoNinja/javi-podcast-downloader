from app.config import ROOT_LOGGER as log, channel_id, provider_id
from app.config import channel_id
from app.config import provider_id
from app.config import sleep_between_download_videos_seconds
from app.config import destination_folder

from app.video import get_not_already_downloaded_videos, set_video_as_downloaded
import yt_dlp as ytl_dlp
from os import path
from time import sleep

DOWNLOADER = None


def download_missing_videos_from_channel_and_provider():
    global DOWNLOADER
    videos_to_download = get_not_already_downloaded_videos(channel_id, provider_id)
    log.info(f"Found {len(videos_to_download)} video(s) to download...")
    log.debug(f"Videos to download are: {videos_to_download}")
    for video in videos_to_download:
        try:
            log.info(f"Downloading {video}...")
            DOWNLOADER.download(video[5])
        except Exception as e:
            log.error(
                f"""Could not download video {video}
                | Error: {e} 
                | Skipping update of download flag because of failure (duh...)
            """
            )
            continue
        log.info("Video downloaded! Updating download flag...")
        set_video_as_downloaded(video)
        # TODO: manejar algo o que!
        log.info("Done! Going to another lööp...")
        # Me está tirando 403 el puto yutub de los cojones mama vergas -> actualizar el paquete con pip install yt-dlp --upgrade
        sleep(sleep_between_download_videos_seconds)


def _setup():
    global DOWNLOADER
    if DOWNLOADER is not None:
        return
    log.info("Creating downloader...")
    config = _create_downloader_config()
    DOWNLOADER = ytl_dlp.YoutubeDL(config)


def _create_downloader_config():
    download_dir = _get_download_path()
    ydl_opts = {
        "format": "bestaudio/best",  # Download the best audio quality available
        "outtmpl": f"{download_dir}/%(title)s.%(ext)s",  # Output filename format
    }
    log.info(f"Created youtube downloader config: {ydl_opts}")
    return ydl_opts


def _get_download_path(root_download_folder="downloads"):
    curr_dir_for_this_file = path.dirname(path.abspath(__file__))
    dest_dir = path.join(
        curr_dir_for_this_file, "..", "..", root_download_folder, destination_folder
    )
    return dest_dir


_setup()
