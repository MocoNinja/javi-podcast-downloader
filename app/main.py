from app.common.logger import ROOT_LOGGER as log
from app.common import config
from app.video.video_service import save_video
from app.video_downloader.downloader import (
    download_missing_videos_from_channel_and_provider,
)
from app.video_scrapper.scrapper_youtube import scrape_youtube


def main():
    # TODO: una cli de esas guapas con la librería esa famosa
    scrape_channel()
    # download_videos()


def scrape_channel():
    log.info(
        f"""Scrapping with config:
            | url: {config.channel_url}
            | channel_id: {config.channel_id}
            | provider: {config.provider}
            | provider_id: {config.provider_id}
            | filter: {True if config.scrapping_filter is not None else False}
        """
    )

    # Todo: mejor flujo
    for _, item in scrape_youtube().items():
        log.info(f"Saving scrapped video: {item}")
        save_video(item, config.channel_id, config.provider_id)


def download_videos():
    log.info(
        f"""Downloading videos with config:
            | url: {config.channel_url}
            | channel_id: {config.channel_id}
            | provider: {config.provider}
            | provider_id: {config.provider_id}
            | destination: {config.destination_folder}
        """
    )
    download_missing_videos_from_channel_and_provider()


if __name__ == "__main__":
    main()
