import logging
import app.common.constants as constants

LOG_LEVEL = logging.INFO

# TODO: un map to guapo que devuelva un struct o el equivalente oligofrénico que tenga python

channel_url = constants.URL_DARKSOUL_HORROR
channel_id = constants.ID_DARKSOUL_HORROR
destination_folder = constants.FOLDER_DARKSOUL_HORROR
scrapping_filter = constants.FILTER_DARKSOUL_HORROR

provider = constants.PROVIDER_YOUTUBE
provider_id = constants.PROVIDER_YOUTUBE_ID


sleep_between_download_videos_seconds = 2

sleep_scrapper_seconds = 2

headless = True
# 0 means not scrolling
max_pages_to_scroll: int = 5
force_scroll_to_the_max: bool = False
## TODO: it would be nice to autodetect that we have scrolled to the bottom if the data is the same
