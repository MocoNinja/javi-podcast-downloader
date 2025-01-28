import datetime
from sys import exit
from time import sleep

from selenium.webdriver.common.keys import Keys
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from app.common.config import max_pages_to_scroll, force_scroll, scrapping_filter, channel_url, sleep_scrapper_seconds
from app.common.logger import ROOT_LOGGER as log
from app.video.video_dto import VideoDto
from app.video.video_provider import VideoProvider
from app.video_scrapper.video_scrapper import create_scrapper, ScrapperType

accept_btn_selector = "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[2]/div/div/button/span"

video_selector = '//*[@id="content"]'


def scrape_youtube():
    log.info(f"Scrapping {channel_url}...")
    driver = create_scrapper(ScrapperType.CHROME)

    driver.get(channel_url)
    data = {}
    try:
        _accept_button_click(driver)
        sleep(sleep_scrapper_seconds)
        data = _scrape_youtube_page(driver)
    except Exception as e:
        log.error(f"Error scrapping: {e}")
    finally:
        driver.close()
    return data



def _parse_pages(driver, max_pages_to_scroll, force_scroll, scroll_pause_time=0.25):
    body = driver.find_element(By.TAG_NAME, "body")
    curr_page = 1
    videos = []
    while curr_page < max_pages_to_scroll:
        log.info(f"Scrolling page {curr_page + 1} / {max_pages_to_scroll}...")
        scraped_page = scrape_youtube(driver)


        body.send_keys(Keys.CONTROL + Keys.END)

        if max_pages_to_scroll is not None:
            curr_page += 1
        sleep(scroll_pause_time)


def _accept_button_click(driver, error_on_failure=True):
    try:
        accept_btn = driver.find_element(By.XPATH, accept_btn_selector)
        accept_btn.click()
    except NoSuchElementException as e:
        log.error(f"Cannot find accept button: {e.msg}")
        if error_on_failure:
            raise Exception("Could not click accept button")


def _scrape_youtube_page(driver):
    video_data = {}
    videos = driver.find_elements(By.XPATH, video_selector)
    for video in videos:
        try:
            url, parsed_data = _parse_youtube_video_for_url(video)
            if parsed_data is not None:
                video_data[url] = parsed_data

        except Exception as e:
            log.error(f"Error accessing elements:", e)
    return video_data


def _parse_youtube_video_for_url(video):
    """
    Get the information for a youtube video from scrapping.
    Some information, like upload date, cannot be obtained in a reliable way through scrapping but yes with yt-ldp (as
    I guess it uses the API underneath. We might want to obtain some fields through that but here we obtain the key fields
    required for scrapping That is the url and title, so we can now if the video exists or not or maybe if we want to apply
    any kind of filter to that
    :param video:
    :return:
    """
    video_title_link = video.find_element(By.XPATH, ".//a[@id='video-title-link']")
    url = video_title_link.get_attribute("href")
    title = video_title_link.get_attribute("title")

    item = VideoDto(
        video_url=url,
        video_title=title,
        video_platform=VideoProvider.YOUTUBE,
        scrap_timestamp=datetime.UTC,
    )

    filtered_item = _filter_if_applies(item, scrapping_filter)

    return url, filtered_item


def _filter_if_applies(video, filter):
    if filter is None:
        log.debug("No filter to apply")
        return video

    pass_filter = filter.filter(video)

    if not pass_filter:
        log.debug(f"{video.video_title} did not match requested filter!")
        return None
    else:
        log.info(f"{video.video_title} did match requested filter!")
        return video
