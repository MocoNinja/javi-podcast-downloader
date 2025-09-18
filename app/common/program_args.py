from argparse import *

"""
    Custom configuration of the app via commandline arguments
"""

_APP_NAME = "javi_podcast_downloader"


parser: ArgumentParser | None = None

def _add_help():
    """
    Adds a basic help message to the parser.
    """
    # The help message is automatically generated based on the added arguments,
    # so no explicit function is needed here.
    # We can, however, set a custom description.
    parser.description = "A command-line tool to scrape and download podcasts."

def _add_optional_flags():
    """
    Adds optional flags.
        * Channel id -> if specified, the single channel id to act upon
    """
    parser.add_argument(
        '--channel-id', '-id',
        type=int,
        help='Specifies the channel ID to process.'
    )


def _add_mandatory_flags_mutually_exclusive():
    """
    Adds mandatory flags that are mutually exclusive.
        * Scrape -> if set, the mode will be to scrape
        * Download -> if set, the mode will be to download
    """
    mandatory_group = parser.add_mutually_exclusive_group(required=True)
    mandatory_group.add_argument(
        '--scrape', '-s',
        action='store_true',
        help='Scrapes the configured channels and providers for new episodes.'
    )

    mandatory_group.add_argument(
        '--download', '-d',
        action='store_true',
        help='Downloads episodes based on the scraped data.'
    )


def setup_args():
    global  parser
    if parser is not None:
        return parser
    parser = ArgumentParser(prog=_APP_NAME)
    _add_help()
    _add_mandatory_flags_mutually_exclusive()
    _add_optional_flags()
    return parser

