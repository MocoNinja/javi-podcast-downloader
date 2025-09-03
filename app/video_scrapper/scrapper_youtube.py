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
from app.model.channel import Channel
from app.service.video_service import (
    check_if_video_exists_for_channel_id_source_id_by_video_id,
)
from app.video_scrapper.scrapper_client import create_scrapper
from app.video_scrapper.youtube_parser import _parse_youtube_video_for_url


def scrape_youtube_videos(channel: Channel):
    info(f"Scrapping {channel.url}...")
    driver = create_scrapper(scrapper_type)

    driver.get(channel.url)
    data = {}
    try:
        _accept_button_click(driver)
        sleep(sleep_scrapper_seconds)
        data = _load_initial_page(driver, channel)
        should_scrape_more_pages = _should_keep_scrapping(data, channel)
        if should_scrape_more_pages:
            _load_pages_until_end(driver, data, channel)
    except Exception as e:
        error(f"Error scrapping: {e}")
    finally:
        driver.close()
    return data


def _load_initial_page(driver, channel):
    video_selector = '//*[@id="contents"]/ytd-rich-item-renderer'
    initial_videos_by_url = _scrape_youtube_page(driver, video_selector, channel)
    info(f"Found {len(initial_videos_by_url)} videos in the first page")
    sleep(sleep_scrapper_seconds)
    if is_enabled_for_level(DEBUG):
        titles_str = "\n".join(
            str(initial_videos_by_url[video]) for video in initial_videos_by_url
        )
        debug(f"Videos found are:\n{titles_str}")

    return initial_videos_by_url


def _load_pages_until_end(driver, data, channel):
    body = driver.find_element(By.TAG_NAME, "body")
    curr_page = 1
    page_size = len(data)

    while _scroll(driver, body):
        info(f"Scrolled page {curr_page} -> {curr_page + 1}...")
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


def _scrape_youtube_page(driver, selector, channel):
    video_data = {}
    videos = driver.find_elements(By.XPATH, selector)
    for video in videos:
        try:
            url, parsed_data = _parse_youtube_video_for_url(video, channel)
            if parsed_data is not None:
                video_data[url] = parsed_data

        except Exception as e:
            error(f"Error accessing elements: {e}")

    return video_data


def _accept_button_click(driver, error_on_failure=True):
    accept_btn_selector = "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[2]/div/div/button/span"
    try:
        accept_btn = driver.find_element(By.XPATH, accept_btn_selector)
        accept_btn.click()
    except NoSuchElementException as e:
        error(f"Cannot find accept button: {e.message}")
        if error_on_failure:
            raise Exception("Could not click accept button")


def _scroll(
    driver,
    anchor,
):
    current_y = driver.execute_script("return window.scrollY;")
    anchor.send_keys(Keys.CONTROL + Keys.END)
    sleep(sleep_between_scroll_seconds)
    new_y = driver.execute_script("return window.scrollY;")
    did_scroll = current_y != new_y
    if not did_scroll:
        info("End of list reached!")
    return did_scroll


def _should_keep_scrapping(video_data: list, channel: Channel):
    should_keep_scrapping = True

    if force_full_scroll or len(video_data) == 0:
        debug(
            "Configured to scrape to the end or missing scrapped data, so I should keep scrollin' scrollin' scrollin'"
        )
        return should_keep_scrapping

    # In python, dicts are ordered
    last_inserted_video = video_data.popitem()[1]

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
