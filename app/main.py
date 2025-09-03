from app.common.config import LOG_LEVEL
from app.common.context import _init_context, get_context
from app.common.logger import _init_root_logger, info
from app.database.connection import _load_database
from app.model.channel import Channel
from app.service.video_service import save_videos
from app.video_downloader.downloader import (
    download_missing_videos_from_channel_and_provider,
)
from app.video_scrapper.scrapper_youtube import scrape_youtube_videos


def _setup() -> None:
    """
    Ensure everything that needs to be configured is ready when starting the program.
    """
    _init_root_logger(LOG_LEVEL)
    _load_database()
    _init_context()


def main():
    _setup()
    ctx = get_context()
    scrape_channel(ctx.channels_to_scrape[0])


def scrape_channel(channel: Channel):
    info(
        f"""Scrapping with config:
            | channel_name: {channel.name}
            | url: {channel.url}
            | provider: {channel.video_platform.name}
            | filter: {True if channel.filter is not None else False}
        """
    )

    ## Make sure the p save_videos(videos, channel.id, channel.video_platform.id)
    videos = scrape_youtube_videos(channel).values()
    info(f"Saving scrapped videos: {videos}")
    save_videos(videos)



def download_videos(channel: Channel):
    info(
        f"""Downloading videos with config:
            | url: {channel.url}
            | channel_id: {channel.id}
            | provider: {channel.video_platform.name}
            | destination: {channel.destination_folder}
        """
    )
    download_missing_videos_from_channel_and_provider(channel)


if __name__ == "__main__":
    main()
