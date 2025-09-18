import datetime

from app.model.video_platform import VideoPlatform


class VideoDto:
    """
    The class to represent the information we want to model a video with, so we can scrap, store and download 'em
    """

    def __init__(
        self,
        video_url: str,
        video_title: str,
        video_platform: VideoPlatform,
        channel_id: int,
        provider_id: int,
        scrap_timestamp: datetime.datetime = None,
        video_upload_datetime: datetime.datetime = None,
        downloaded_flag=False,
    ):
        if video_platform is None:
            raise ValueError(f"Cannot parse video because platform is missing")
        try:
            self.video_id = video_url.split(video_platform.video_base_url)[1]
        except Exception as e:
            raise ValueError(f"Cannot parse video: {e}")
        self.video_url = video_url
        self.video_title = video_title
        self.video_platform = video_platform
        self.channel_id = channel_id
        self.provider_id = provider_id  # TODO: this is redundant if we store the entity
        self.downloaded_flag = downloaded_flag
        if scrap_timestamp is not None:
            self.scrap_timestamp = scrap_timestamp
        if video_upload_datetime is not None:
            self.video_upload_datetime = video_upload_datetime

    def __repr__(self):
        return f"Video(video_id={self.video_id}, video_title={self.video_title}, video_platform={self.video_platform.name})"
