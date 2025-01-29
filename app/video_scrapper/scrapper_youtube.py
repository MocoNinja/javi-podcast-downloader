import datetime
from logging import DEBUG
from sys import exit
from time import sleep

from selenium.webdriver.common.keys import Keys
from selenium.common import NoSuchElementException

from app.common.config import (
    channel_url,
    sleep_scrapper_seconds,
    max_pages_to_scroll,
    provider_id,
    channel_id,
    force_scroll_to_the_max,
)
from app.common.logger import ROOT_LOGGER as log
from app.video.video_service import (
    _check_if_video_exists_for_channel_id_source_id_by_video_id,
    check_if_video_exists_for_channel_id_source_id_by_video_id,
)
from app.video_scrapper.scrapper_client import create_scrapper, ScrapperType
from app.video_scrapper.youtube_parser import _parse_youtube_video_for_url
from selenium.webdriver.common.by import By


def scrape_youtube():
    log.info(f"Scrapping {channel_url}...")
    driver = create_scrapper(ScrapperType.FIREFOX)

    driver.get(channel_url)
    data = {}
    try:
        _accept_button_click(driver)
        sleep(sleep_scrapper_seconds)
        data = _load_initial_page(driver)
        _scrape_following_pages(driver, data)
    except Exception as e:
        log.error(f"Error scrapping: {e}")
    finally:
        driver.close()
    return data


def _load_initial_page(driver):
    video_selector = '//*[@id="contents"]/ytd-rich-item-renderer'
    result = _scrape_youtube_page(driver, video_selector)
    initial_videos_by_url = result[0]
    log.debug(f"Found {len(initial_videos_by_url)} initial videos")
    if log.isEnabledFor(DEBUG):
        titles_str = "\n".join(
            str(initial_videos_by_url[video]) for video in initial_videos_by_url
        )
        log.debug(f"Videos found are:\n{titles_str}")

    return initial_videos_by_url


def _scrape_following_pages(driver, data, scroll_pause_time=1):
    body = driver.find_element(By.TAG_NAME, "body")
    curr_page = 1
    page_size = len(data)
    while curr_page <= max_pages_to_scroll:
        log.info(f"Scrolling page {curr_page} / {max_pages_to_scroll}...")
        start_index_for_new_page = page_size * curr_page
        end_index_for_new_page = start_index_for_new_page + page_size
        curr_page = _scroll(body, curr_page)
        sleep(scroll_pause_time)
        selector = f'//*[@id="contents"]/ytd-rich-item-renderer[position() > {start_index_for_new_page} and position() <=  {end_index_for_new_page}]'
        result = _scrape_youtube_page(driver, selector)
        new_videos = result[0]
        data.update(new_videos)
        should_scrape_more_pages = result[1]
        log.debug(f"Found {len(new_videos)} initial videos")
        if log.isEnabledFor(DEBUG):
            titles_str = "\n".join(str(new_videos[video]) for video in new_videos)
            log.debug(f"Videos found are:\n{titles_str}")
        if not should_scrape_more_pages:
            log.info("Aborting scrapping....")
            break


def _scrape_youtube_page(driver, selector):
    video_data = {}
    videos = driver.find_elements(By.XPATH, selector)
    for video in videos:
        try:
            url, parsed_data = _parse_youtube_video_for_url(video)
            if parsed_data is not None:
                video_data[url] = parsed_data

        except Exception as e:
            log.error(f"Error accessing elements:", e)

    # In python, dicts are ordered
    last_inserted_video = video_data.popitem()[1]

    should_scrape_one_more = True
    if (
        not force_scroll_to_the_max
        and check_if_video_exists_for_channel_id_source_id_by_video_id(
            channel_id=channel_id,
            source_id=provider_id,
            video_id=last_inserted_video.video_id,
        )
    ):
        log.info(
            f"Last video {last_inserted_video} seems to exist into database!! This in theory means that we should not scrape anymore"
        )
        should_scrape_one_more = False
    return video_data, should_scrape_one_more


def _accept_button_click(driver, error_on_failure=True):
    accept_btn_selector = "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[2]/div/div/button/span"
    try:
        accept_btn = driver.find_element(By.XPATH, accept_btn_selector)
        accept_btn.click()
    except NoSuchElementException as e:
        log.error(f"Cannot find accept button: {e.msg}")
        if error_on_failure:
            raise Exception("Could not click accept button")


def _scroll(anchor, page):
    anchor.send_keys(Keys.CONTROL + Keys.END)
    page += 1
    return page
