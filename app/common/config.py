import logging
import app.common.constants as constants

LOG_LEVEL = logging.INFO

# TODO: un map to guapo que devuelva un struct o el equivalente oligofrénico que tenga python

channel_url = constants.URL_DARKSOUL_HORROR
channel_id = constants.ID_BAGS_GARAGE
destination_folder = constants.FOLDER_BAGS_GARAGE
scrapping_filter = constants.FILTER_BAGS_GARAGE

provider = constants.PROVIDER_YOUTUBE
provider_id = constants.PROVIDER_YOUTUBE_ID


sleep_between_download_videos_seconds = 2

sleep_scrapper_seconds = 2

headless = False
max_pages_to_scroll = 1
force_scroll = False