import re
from app.video.video_filter import VideoFilter

# TODO: pensar en algun enum que carge info de base de datos o alguna mierda?

URL_DARKSOUL_HORROR = "https://www.youtube.com/@DarksoulHorror/videos"
URL_BAGS_GARAGE = "https://www.youtube.com/@BagsGarage/videos"
URL_WILD_PROJECT = "https://www.youtube.com/@TheWildProject/videos"

ID_DARKSOUL_HORROR = 1
ID_BAGS_GARAGE = 2
ID_WILD_PROJECT = 3

FOLDER_DARKSOUL_HORROR = "darksoul_horror"
FOLDER_BAGS_GARAGE = "bags_garage"
FOLDER_WILD_PROJECT = "the_wild_project"

PROVIDER_YOUTUBE = "YOUTUBE"
PROVIDER_YOUTUBE_ID = 1

FILTER_DARKSOUL_HORROR = None
FILTER_BAGS_GARAGE = None
FILTER_WILD_PROJECT = VideoFilter(
    video_title=lambda video: re.match(r"The Wild Project #\d+ .+", video.video_title)
)
