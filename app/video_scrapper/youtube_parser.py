from datetime import UTC, datetime

from selenium.webdriver.common.by import By

from app.common.context import get_context
from app.common.logger import debug, info
from app.model.video_dto import VideoDto
from app.model.video_filter import VideoFilterConfiguration
from app.model.video_platform import ConfiguredVideoProvider


def _parse_youtube_video_for_url(video, channel):
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
    url = _normalize_url(video_title_link.get_attribute("href"))
    title = video_title_link.get_attribute("title")

    ctx = get_context()
    provider = ctx.get_provider_for(ConfiguredVideoProvider.YOUTUBE)
    item = VideoDto(
        video_url=url,
        video_title=title,
        video_platform=provider,
        provider_id=provider.id,
        channel_id=channel.id,
        scrap_timestamp=datetime.now(UTC),
    )

    filtered_item = _filter_if_applies(item, channel.filter)

    return url, filtered_item


def _filter_if_applies(video, configured_filter: VideoFilterConfiguration):
    if configured_filter is None:
        return video

    pass_filter = configured_filter.filter(video)

    if not pass_filter:
        debug(f"{video.video_title} did not match requested filter!")
        return None
    else:
        info(f"{video.video_title} did match requested filter!")
        return video


def _normalize_url(url: str) -> str:
    """
    We have seen that the url sometimes needs some parsing. This method ensures that the result is normalized.
    :param url: the raw url
    :return:  the normalized url
    """

    # Some URLs come with some suffix, like this &pp=0gcJCcYJAYcqIYzv,that we want removed
    return url.split("&pp=", 2)[0]
