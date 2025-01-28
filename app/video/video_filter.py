from app.video.video_dto import VideoDto


class VideoFilter:
    def __init__(self, **criteria):
        self.criteria = criteria

    def filter(self, dto: VideoDto):
        evaluation = True
        for key, condition in self.criteria.items():
            dto_value = getattr(dto, key, None)
            if dto_value is not None:
                filter_result = condition(dto)
                evaluation = evaluation and filter_result

        return evaluation
