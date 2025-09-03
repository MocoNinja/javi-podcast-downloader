import logging

from app.video_scrapper.scrapper_type import ScrapperType

"""
    Several constants used for common configuration among the application.
"""

"""
    Log level for the app
"""
LOG_LEVEL = logging.DEBUG

"""
    The browser that the webdriver uses
"""
scrapper_type = ScrapperType.CHROME

"""
    Delay between downloading videos
"""
sleep_between_download_videos_seconds = 2

"""
    Delay between steps in the scrapping process
"""
sleep_scrapper_seconds = 5

"""
    Delay between scrolling the page to fetch new videos
"""
sleep_between_scroll_seconds = 1.5

"""
    If the webdriver should open a window or not
"""
headless = False

"""
    Scroll all pages even if there are repeated items
"""
force_full_scroll: bool = False
