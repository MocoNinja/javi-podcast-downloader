import logging
from enum import Enum


class ScrapperType(Enum):
    FIREFOX = (1,)
    CHROME = 2


"""
    Several constants used for common configuration among the application.
"""

"""
    Log level for the app
"""
LOG_LEVEL = logging.INFO

"""
    The browser that the webdriver uses
"""
configured_scrapper_type = ScrapperType.CHROME

"""
    Delay between downloading videos
"""
sleep_between_download_videos_seconds = 2

"""
    Delay between steps in the scrapping process
"""
sleep_scrapper_seconds = 2

"""
    Delay between scrolling the page to fetch new videos
"""
sleep_between_scroll_seconds = 1.0

"""
    If the webdriver should open a window or not
"""
headless = True

"""
    Scroll all pages even if there are repeated items
"""
force_full_scroll: bool = False
