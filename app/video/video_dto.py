from app.video import VideoProvider


class VideoDto:
    def __init__(self, video_url: str, video_title: str, video_platform: VideoProvider):
        self.video_id = self._parse_video_id(video_url, video_platform)
        self.video_url = video_url
        self.video_title = video_title
        self.video_platform = video_platform

    def _parse_video_id(self, url: str, platform: VideoProvider) -> str:
        try:
            return url.split(platform.value)[1]
        except Exception as e:
            raise ValueError(f"Cannot parse video: {e}")

    def __repr__(self):
        return f"Video(video_id={self.video_id}, video_title={self.video_title}, video_platform={self.video_platform.name})"
