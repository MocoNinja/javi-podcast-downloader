from dataclasses import dataclass
from enum import Enum


class ConfiguredVideoProvider(Enum):
    """
    Simple enum for handled providers for better semantics
    """

    YOUTUBE = 1


@dataclass
class VideoPlatform:
    """
    The representation of the sources we want to fetch and download videos from
    """

    id: int
    name: ConfiguredVideoProvider
    video_base_url: str
    channel_url_pattern: str
