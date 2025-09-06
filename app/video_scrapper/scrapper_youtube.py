from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from app.common.config import configured_scrapper_type, sleep_scrapper_seconds
from app.common.logger import error, info
from app.error.errors import ScrappingError
from app.model.channel import Channel
from app.model.video_dto import VideoDto
from app.video_scrapper.common_scrapper import (
    calculate_elements_in_page,
    perform_scroll,
    scrape_page,
    should_keep_fetching,
)
from app.video_scrapper.scrapper_client import create_scrapper
from app.video_scrapper.youtube_parser import _parse_youtube_video_for_url

"""
    The fixed selector to find videos in a youtube page
"""
SELECTOR = '//*[@id="contents"]/ytd-rich-item-renderer'


def scrape_youtube_videos(channel: Channel) -> list[VideoDto]:
    """
    Get the list of videos for a channel
    :param channel: the channel we want to scrape for videos
    :return: the scrapped videos, if any
    """
    info(f"Scrapping {channel.url}...")

    driver = create_scrapper(configured_scrapper_type)
    driver.get(channel.url)

    data = []
    current_page = 1
    should_keep_scrapping = True
    video_indexes_to_scrape = None

    try:
        # For youtube, we must click a button to continue...
        _accept_button_click(driver)

        sleep(sleep_scrapper_seconds)

        # ...And after the configured delay, we can begin scrapping the shit out of the data
        while should_keep_scrapping:
            video_indexes_to_scrape = calculate_elements_in_page(
                driver, video_indexes_to_scrape, SELECTOR
            )
            selector_for_new_videos = f'//*[@id="contents"]/ytd-rich-item-renderer[position() > {video_indexes_to_scrape[0]} and position() <=  {video_indexes_to_scrape[1]}]'

            scrapping_result = scrape_page(
                driver, channel, selector_for_new_videos, _parse_youtube_video_for_url
            )
            scrapped_videos = [x for x in scrapping_result if x is not None]
            info(
                f"Read {len(scrapping_result)} and scrapped {len(scrapped_videos)} from page {current_page}"
            )

            data.extend(scrapped_videos)

            scrolled, current_page = perform_scroll(driver, current_page)

            if not scrolled:
                info("We reached end of scrolling, so we ended the process!")
                break

            if len(scrapped_videos) > 0:
                last_scrapped_video = scrapped_videos[-1]
                should_keep_scrapping = should_keep_fetching(
                    video_indexes_to_scrape, last_scrapped_video
                )

    except (ScrappingError, Exception) as e:
        error(f"Error scrapping channel {channel} from youtube: {e}")
    finally:
        driver.close()

    # ... so we can finally use it :)
    return data


def _accept_button_click(driver, error_on_failure=True) -> None:
    """
    In youtube, a button must be clicked before accessing the channel.
    This method contains the logic to continue to the page
    :param driver: to perform the scrapping
    :param error_on_failure: if an error finding / clicking the button should result in an error
    """
    accept_btn_selector = "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[2]/div/div/button/span"
    try:
        accept_btn = driver.find_element(By.XPATH, accept_btn_selector)
        accept_btn.click()
    except NoSuchElementException as e:
        error(f"Cannot find accept button: {e.message}")
        if error_on_failure:
            raise ScrappingError("Could not click accept button", e)
