from logging import DEBUG
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from app.common.config import force_full_scroll, sleep_between_scroll_seconds
from app.common.logger import debug, info, is_enabled_for_level
from app.model.channel import Channel
from app.model.video_dto import VideoDto
from app.service.video_service import video_exists_by_video_id, save_videos


def scrape_channel(channel: Channel, scrapper) -> None:
    """
    Scrape the given channel. This means that the database will have the required information to download videos.
    :param channel: the channel to scrape
    :param scrapper:  the logic to be used
    """
    info(
        f"""Scrapping with config:
            | channel_name: {channel.name}
            | url: {channel.url}
            | provider: {channel.video_platform.name}
            | filter: {True if channel.filter is not None else False}
        """
    )

    ## Make sure the p save_videos(videos, channel.id, channel.video_platform.id)
    videos = scrapper(channel)
    info(f"Scrapped videos: {videos}")
    videos = [x for x in videos if x is not None]
    info(f"Saving filtered scrapped videos: {videos}")
    save_videos(videos)

def perform_scroll(driver, curr_page: int) -> tuple[bool, int]:
    """
    Perform an actual scrolling operation in the browser to be able to keep loading items
    :param curr_page: the current value of the page fetching
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
    return did_scroll, curr_page


def calculate_elements_in_page(driver, indexes, selector) -> tuple[int, int]:
    """
    Return the number of videos loaded in the current HTML
    :param driver: to perform the scrapping
    :param indexes: to determine what elements are calculated
    :param selector: to detect the markup of the video in the provider
    :return: the amount of videos to calculate
    """
    items = len(driver.find_elements(By.XPATH, selector))

    if indexes is None:
        return 0, items
    else:
        last_current_index = indexes[1]
        return last_current_index, items


def scrape_page(
    driver, channel, selector, mapper_for_channel_and_provider_function
) -> list[VideoDto]:
    """
    Scrape the page of the provider and just get the data we want
    :param driver: to perform the actual scrapping
    :param channel: we are scrapping videos for
    :param selector: that determines the element to scrape
    :param mapper_for_channel_and_provider_function: that will be used to scrape the information
    :return: all the scrapped elements
    """
    video_data = []
    video_urls = driver.find_elements(By.XPATH, selector)

    for provider_video in video_urls:
        parsed_data = mapper_for_channel_and_provider_function(provider_video, channel)
        video_data.append(parsed_data)

    if is_enabled_for_level(DEBUG):
        titles_str = "\n".join(str(video) for video in video_data)
        debug(f"Videos found are:\n{titles_str}")

    return video_data


def should_keep_fetching(indexes, last_video) -> bool:
    """
    Determine if we should try and keep advancing pages to scrape more data
    :param indexes: the current indexes being scrapped
    :param last_video: the last video that was detected
    :return: whether we should continue or not
    """
    if indexes[0] == 0:
        debug("This was the first page, so we must keep fetching")
        return True

    if force_full_scroll:
        debug(
            "We are configured to ignore all condition and just keep scrollin' scrollin' scrollin'"
        )
        return True

    if last_video is None or last_video.video_id is None:
        debug(
            "Cannot extract information from last video so we are going to assume it wasn't in the database and will keep scrollin' scrollin' scrollin'"
        )
        return True

    if not video_exists_by_video_id(last_video.video_id):
        return True
    else:
        info(
            f"Video {last_video} seems to exist into our database already so we are going to cut this short!"
        )

    return False
