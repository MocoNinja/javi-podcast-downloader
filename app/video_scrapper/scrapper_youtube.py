from logging import DEBUG
from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from app.common.config import (
    force_full_scroll,
    scrapper_type,
    sleep_between_scroll_seconds,
    sleep_scrapper_seconds,
)
from app.common.logger import debug, error, info, is_enabled_for_level
from app.error.errors import ScrappingError
from app.model.channel import Channel
from app.model.video_dto import VideoDto
from app.video_scrapper.scrapper_client import create_scrapper
from app.video_scrapper.youtube_parser import _parse_youtube_video_for_url



def scrape_youtube_videos(channel: Channel):
    info(f"Scrapping {channel.url}...")
    driver = create_scrapper(scrapper_type)

    driver.get(channel.url)
    curr_page = 1
    data = []
    try:
        _accept_button_click(driver)
        sleep(sleep_scrapper_seconds)
        indexes = _calculate_elements_in_page(driver, None)
        while _should_keep_fetching(indexes):
            new_videos = _load_page(driver, channel, indexes)
            actual_videos = len([x for x in new_videos if x is not None])
            info(f"Read {len(new_videos)} and scrapped {actual_videos} from page {curr_page}")
            data.extend(new_videos)
            scrolled, curr_page = _perform_scroll(driver, curr_page)
            if not scrolled:
                info("We reached end of scrolling, so we ended the process!")
                break
            indexes = _calculate_elements_in_page(driver, indexes)
    except (ScrappingError, Exception) as e:
        error(f"Error scrapping channel {channel} from youtube: {e}")
    finally:
        driver.close()
    return data

def _should_keep_fetching(indexes) -> bool:
    if indexes[0] == 0:
        debug("This was the first page, so we must keep fetching")
        return True
    if force_full_scroll:
        debug("We are configured to keep scrollin' scrollin' scrollin'")
        return True

    # If the last video of the page is in the database, we can assume that everything further will also be there and therefore we can exit before
    last_video_index = indexes[1]

    return False



def _load_page(driver, channel, indexes):
    selector_for_new_videos = f'//*[@id="contents"]/ytd-rich-item-renderer[position() > {indexes[0]} and position() <=  {indexes[1]}]'
    videos = _scrape_youtube_page(driver, selector_for_new_videos, channel)
    if is_enabled_for_level(DEBUG):
        titles_str = "\n".join(str(video) for video in videos)
        debug(f"Videos found are:\n{titles_str}")
    return videos


"""

def _load_initial_page(driver, channel):
    video_selector = '//*[@id="contents"]/ytd-rich-item-renderer'
    initial_videos_by_url = _scrape_youtube_page(driver, video_selector, channel)
    info(f"Found {len(initial_videos_by_url)} videos in the first page")
    sleep(sleep_scrapper_seconds)

    return initial_videos_by_url
def _load_pages_until_end(driver, data, channel, indexes):
    curr_page = indexes[0]
    page_size = indexes[1] - indexes[0]

    while _perform_scroll(driver):
        info(f"Scrolled page {curr_page} -> {curr_page + 1}...")
        count = _calculate_elements_in_page(driver, indexes)
        start_index_for_new_page = page_size * curr_page
        end_index_for_new_page = start_index_for_new_page + page_size
        selector_for_new_videos = f'//*[@id="contents"]/ytd-rich-item-renderer[position() > {start_index_for_new_page} and position() <=  {end_index_for_new_page}]'

        new_videos = _scrape_youtube_page(driver, selector_for_new_videos, channel)
        should_scrape_more_pages = _should_keep_scrapping(new_videos, channel)
        data.update(new_videos)

        curr_page += 1

        info(f"Found {len(new_videos)} video(s)...")
        if is_enabled_for_level(DEBUG):
            titles_str = "\n".join(str(new_videos[video]) for video in new_videos)
            debug(f"Videos found are:\n{titles_str}")
        if not should_scrape_more_pages:
            info("Aborting scrapping....")
            break
"""


"""
def _should_keep_scrapping(video_data: list, channel: Channel):
    should_keep_scrapping = True

    if force_full_scroll or len(video_data) == 0:
        debug(
            "Configured to scrape to the end or missing scrapped data, so I should keep scrollin' scrollin' scrollin'"
        )
        return should_keep_scrapping

    # In python, dicts are ordered
    last_inserted_video = video_data.popitem()[1]

    if last_inserted_video is None:
        return should_keep_scrapping

    ## TODO: esto hay que pensarlo mejor
    if check_if_video_exists_for_channel_id_source_id_by_video_id(
        channel.id,
        channel.video_platform.id,
        video_id=last_inserted_video.video_id,
    ):
        info(
            f"Last video {last_inserted_video} seems to exist into database!! This in theory means that we should not scrape anymore"
        )
        should_keep_scrapping = False
    return should_keep_scrapping

"""
def _scrape_youtube_page(driver, selector, channel) -> list[VideoDto]:
    video_data = []
    video_urls = driver.find_elements(By.XPATH, selector)
    for video in video_urls:
        try:
            parsed_data = _parse_youtube_video_for_url(video, channel)
            video_data.append(parsed_data)
        except Exception as e:
            error(f"Error accessing elements: {e}")

    return video_data


def _calculate_elements_in_page(
    driver, indexes, selector='//*[@id="contents"]/ytd-rich-item-renderer'
) -> tuple[int | None]:
    """
    Return the number of videos loaded in the current HTML
    :param driver: to perform the scrapping
    :param selector: to detect the markup of the youtube video
    :return: the amount of videos to calculate
    """
    items = len(driver.find_elements(By.XPATH, selector))
    if indexes is None:
        return (0, items)
    else:
        last_current_index = indexes[1]
        return (last_current_index, items)


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


def _perform_scroll(driver, curr_page: int) -> tuple[bool, int]:
    """
    Perform an actual scrolling operation in the browser to be able to keep loading items
    :param driver: to perform the scrapping
    :return: if it was possible to scroll or not because there is no more data to scroll
    """
    anchor = driver.find_element(By.TAG_NAME, "body")
    current_y = driver.execute_script("return window.scrollY;")
    anchor.send_keys(Keys.CONTROL + Keys.END)
    sleep(sleep_between_scroll_seconds)
    new_y = driver.execute_script("return window.scrollY;")
    did_scroll = current_y != new_y
    if not did_scroll:
        info(f"End of list reached at page {curr_page}!")
    else:
        info(f"Scrolled from page {curr_page} -> {curr_page + 1}")
        curr_page = curr_page + 1
    return (did_scroll, curr_page)
