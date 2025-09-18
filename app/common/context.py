from dataclasses import dataclass

from app.common.logger import fatal
from app.error.errors import MissingItemException
from app.model.channel import Channel
from app.model.video_platform import ConfiguredVideoProvider, VideoPlatform
from app.service.channel_service import get_all_configured_channels
from app.service.video_platform_service import get_all_video_platforms

"""
    Context holder to avoid fetching information from database several times
"""


@dataclass
class _Context:
    """
    Class to hold the data and utility methods
    """

    video_providers: list[VideoPlatform]
    channels_to_scrape: list[Channel]

    def get_provider_for(self, provider: ConfiguredVideoProvider) -> VideoPlatform:
        item = next(
            filter(
                lambda configured_video_provider: configured_video_provider.id
                == provider.value,
                self.video_providers,
            ),
            None,
        )
        if item is None:
            raise MissingItemException
        return item

    def get_channel_by_name(self, channel_name: str) -> Channel:
        """
        Retrieve a channel by the name we have in the db. Fail if not found
        :param channel_name: to find the channel by
        :return: the whole channel
        """
        matching = next(
            filter(lambda c: c.name == channel_name, self.channels_to_scrape), None
        )
        if matching is None:
            raise MissingItemException(
                f"Channel with name '{channel_name}' was not found"
            )
        return matching

    def get_channel_by_id(self, channel_id: int) -> Channel:
        """
        Retrieve a channel by the id we have in the db. Fail if not found
        :param channel_id: to find the channel by
        :return: the whole channel
        """
        matching = next(
            filter(lambda c: c.id == channel_id, self.channels_to_scrape), None
        )
        if matching is None:
            raise MissingItemException(f"Channel with id '{channel_id}' was not found")
        return matching


"""
    Global context to be used after loading (needs to be loaded)
"""
context: _Context | None


def get_context() -> _Context:
    """
    Retrieve the *previously loaded* context
    :return:
    """
    if context is None:
        fatal("Cannot get context so we must terminate the application")
        exit(1)
    return context


def init_context() -> None:
    """
    Load the required configuration that is read from database into this context holder
    """
    global context
    video_providers = get_all_video_platforms()
    channels_to_scrape = get_all_configured_channels()
    context = _Context(video_providers, channels_to_scrape)
