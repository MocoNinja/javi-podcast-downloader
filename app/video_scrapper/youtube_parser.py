from datetime import datetime, UTC

from app.video.video_dto import VideoDto
from app.video.video_provider import VideoProvider

from app.common.config import scrapping_filter
from app.common.logger import ROOT_LOGGER as log
from selenium.webdriver.common.by import By


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
        scrap_timestamp=datetime.now(UTC),
    )

    filtered_item = _filter_if_applies(item, scrapping_filter)

    return url, filtered_item


def _filter_if_applies(video, filter):
    if filter is None:
        return video

    pass_filter = filter.filter(video)

    if not pass_filter:
        log.debug(f"{video.video_title} did not match requested filter!")
        return None
    else:
        log.info(f"{video.video_title} did match requested filter!")
        return video
