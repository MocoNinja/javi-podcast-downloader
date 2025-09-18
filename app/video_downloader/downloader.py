from os import path
from time import sleep

import yt_dlp as ytl_dlp

from app.common.config import sleep_between_download_videos_seconds
from app.common.logger import debug, error, info
from app.model.channel import Channel
from app.service.video_service import (
    get_not_already_downloaded_videos,
    set_video_as_downloaded,
)


def download_channel(channel: Channel):
    downloader = _setup_downloader_for_channel(channel)
    videos_to_download = get_not_already_downloaded_videos(
        channel.id, channel.video_platform.id
    )
    info(f"Found {len(videos_to_download)} video(s) to download...")
    debug(f"Videos to download are: {videos_to_download}")
    for video in videos_to_download:
        try:
            info(
                f"Downloading and parsing '{video.name}' from '{channel.name}' at '{video.url}..."
            )
            ## TODO: aqui hay un porrón de información todo wapa que igual me mola guardar en la tabla de videos...
            ## Además parece que tarda siempre lo mismo asi que por el precio me lo jamo todo
            info_dict = downloader.extract_info(video.url, download=True)
            upload_time = info_dict.get("upload_date")
            info(f"Info Found | Upload: {upload_time}")
        except Exception as e:
            error(
                f"""Could not download video {video}
                | Error: {e} 
                | Skipping update of download flag because of failure (duh...)
            """
            )
            continue
        info("Video downloaded! Updating download flag...")
        set_video_as_downloaded(video)
        info("Done! Going to another lööp...")
        # Me está tirando 403 el puto yutub de los cojones mama vergas -> actualizar el paquete con pip install yt-dlp --upgrade
        sleep(sleep_between_download_videos_seconds)


def _setup_downloader_for_channel(channel: Channel) -> ytl_dlp.YoutubeDL:
    """
    For the given channel, prepare all that is necessary to download the videos with yt-dlp
    :param channel: to download videos from
    :return: the configuration to perform the actual download
    """
    download_dir = _get_download_path_for_channel(channel)
    ytl_dlp_opts = {
        "quiet": True,
        "format": "bestaudio",
        "outtmpl": f"{download_dir}/%(upload_date)s_%(title)s.%(ext)s",
        "keepvideo": False,
    }
    info(
        f"Created youtube downloader for channel '{channel.name}' with config: {ytl_dlp_opts}"
    )

    return ytl_dlp.YoutubeDL(ytl_dlp_opts)


def _get_download_path_for_channel(
    channel: Channel, root_download_folder: str = "downloads"
):
    """
    Assemble the download path for the videos based on a channel configuration and a root download folder
    :param channel: to get the configuration from database
    :param root_download_folder: to use a custom path or the default one of 'downloads'
    :return: a sketchy hardcoded path that I'll probably want to change in a future #TODO
    """
    curr_dir_for_this_file = path.dirname(path.abspath(__file__))
    dest_dir = path.join(
        curr_dir_for_this_file,
        "..",
        "..",
        root_download_folder,
        channel.destination_folder,
    )
    return dest_dir
