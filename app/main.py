from app.scrapper import scrapper_youtube

from app.config import ROOT_LOGGER as log
from app.config import config

from app.video import save_video

from app.scrapper import scrape_youtube
from app.downloader import download_missing_videos_from_channel_and_provider


def main():
    # TODO: una cli de esas guapas con la librería esa famosa
    scrape_channel()
    download_videos()


def scrape_channel():
    log.info(
        f"""Scrapping with config:
            | url: {config.channel_url}
            | channel_id: {config.channel_id}
            | provider: {config.provider}
            | provider_id: {config.provider_id}
        """
    )

    # Todo: mejor flujo
    for _, item in scrape_youtube(config.channel_url, None).items():
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
