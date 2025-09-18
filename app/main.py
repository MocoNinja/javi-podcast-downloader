from argparse import Namespace

from app.common.config import LOG_LEVEL
from app.common.context import init_context, get_context, _Context
from app.common.logger import init_root_logger, info
from app.common.program_args import setup_args
from app.database.connection import load_database
from app.video_downloader.downloader import download_channel
from app.video_scrapper.common_scrapper import scrape_channel
from app.video_scrapper.scrapper_youtube import scrape_youtube_videos



def main(ctx: _Context, args: Namespace):
    channel_id = args.channel_id
    scrape_mode = args.scrape
    download_mode = args.download
    info(f"Determining execution mode from arguments 'channel_id': '{channel_id}' | 'scrape_mode': '{scrape_mode}' | 'download_mode: '{download_mode}'")
    channels_to_handle = []

    if args.channel_id is None:
        info("No channel specified, so will act upon all channels")
        channels_to_handle = ctx.channels_to_scrape
    else:
       info(f"Specified channel with id '{channel_id}'")
       channels_to_handle.append(ctx.get_channel_by_id(channel_id))

    info(f"Selected channels to act upon: {channels_to_handle}")

    if scrape_mode:
        _perform_scrape(channels_to_handle)

    if download_mode:
        _perform_download(channels_to_handle)





def _perform_scrape(channels_to_scrape):
    for channel in channels_to_scrape:
        scrape_channel(channel, scrape_youtube_videos)

def _perform_download(channels_to_download):
    for channel in channels_to_download:
        download_channel(channel)


if __name__ == "__main__":
    """
    Ensure everything that needs to be configured is ready when starting the program.
    """
    init_root_logger(LOG_LEVEL)
    load_database()
    init_context()
    args = setup_args()
    ctx =  get_context()
    main(ctx, args.parse_args())
