from app.common.config import (
    channel_url,
    channel_id,
    provider,
    provider_id,
    scrapping_filter,
    destination_folder,
)
from app.common.logger import ROOT_LOGGER as log
from app.common import config
from app.video.video_service import save_video, save_videos
from app.video_downloader.downloader import (
    download_missing_videos_from_channel_and_provider,
)
from app.video_scrapper.scrapper_youtube import scrape_youtube_videos


def main():
    # TODO: una cli de esas guapas con la librería esa famosa
    scrape_channel()
    # download_videos()


def scrape_channel():
    log.info(
        f"""Scrapping with config:
            | url: {channel_url}
            | channel_id: {channel_id}
            | provider: {provider}
            | provider_id: {provider_id}
            | filter: {True if scrapping_filter is not None else False}
        """
    )

    videos = scrape_youtube_videos().values()
    log.info(f"Saving scrapped videos: {videos}")
    save_videos(videos, channel_id, provider_id)


def download_videos():
    log.info(
        f"""Downloading videos with config:
            | url: {channel_url}
            | channel_id: {channel_id}
            | provider: {provider}
            | provider_id: {provider_id}
            | destination: {destination_folder}
        """
    )
    download_missing_videos_from_channel_and_provider()


if __name__ == "__main__":
    main()
