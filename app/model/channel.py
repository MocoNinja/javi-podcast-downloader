from dataclasses import dataclass

from app.model.video_filter import VideoFilterConfiguration
from app.model.video_platform import VideoPlatform


@dataclass
class Channel:
    """
    The representation of a channel we want to scrape videos from
    """

    id: int
    name: str
    url: str
    video_platform: VideoPlatform
    destination_folder: str
    filter: VideoFilterConfiguration
