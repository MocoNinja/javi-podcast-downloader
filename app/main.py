from app.common.config import LOG_LEVEL
from app.common.context import _init_context, get_context
from app.common.logger import _init_root_logger, info
from app.database.connection import _load_database
from app.model.channel import Channel
from app.service.video_service import save_videos
from app.video_downloader.downloader import (
    download_missing_videos_from_channel_and_provider,
)
from app.video_scrapper.common_scrapper import scrape_channel
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
    channels_to_scrape = ctx.channels_to_scrape
    for channel in channels_to_scrape:
        scrape_channel(channel, scrape_youtube_videos)



if __name__ == "__main__":
    main()
