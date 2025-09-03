from dataclasses import dataclass
from re import match

from app.model.video_dto import VideoDto


class _InnerVideoFilter:
    """
    Raw filter logic
    """

    def __init__(self, **criteria):
        self.criteria = criteria

    def perform_video_filter(self, video_dto: VideoDto) -> bool:
        evaluation = True
        for key, condition in self.criteria.items():
            dto_value = getattr(video_dto, key, None)
            if dto_value is not None:
                filter_result = condition(video_dto)
                evaluation = evaluation and filter_result

        return evaluation


@dataclass
class VideoFilterConfiguration:
    """
    The representation of a configured filter for videos
    """

    id: int
    video_title_regex: str

    def _filter_by_video_title_lambda(self):
        return lambda video: match(self.video_title_regex, video.video_title)

    def filter(self, video_dto: VideoDto) -> bool:
        configured_actual_filter = _InnerVideoFilter(
            video_title=self._filter_by_video_title_lambda()
        )
        return configured_actual_filter.perform_video_filter(video_dto)
