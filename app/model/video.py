from dataclasses import dataclass


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
