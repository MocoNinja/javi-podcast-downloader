from dataclasses import dataclass

from app.model.video_filter import VideoFilterConfiguration
from app.model.video_platform import VideoPlatform


@dataclass
class Video:
    """
    The representation of a video we want to download
    """
    id: int
    name: str
    downloaded: bool
    channel_id: int
    url: str
    video_provider_id: int
