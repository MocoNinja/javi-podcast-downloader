import logging
import app.common.constants as constants

LOG_LEVEL = logging.INFO

# TODO: un map to guapo que devuelva un struct o el equivalente oligofrénico que tenga python

channel_url = constants.URL_NOCHE_MACABRA
channel_id = constants.ID_NOCHE_MACABRA
destination_folder = constants.FOLDER_NOCHE_MACABRA
scrapping_filter = constants.FILTER_NOCHE_MACABRA

provider = constants.PROVIDER_YOUTUBE
provider_id = constants.PROVIDER_YOUTUBE_ID


sleep_between_download_videos_seconds = 2
sleep_scrapper_seconds = 5
sleep_between_scroll_seconds = 1.5

headless = True
# Scroll all pages even if there are repeated items
force_full_scroll: bool = True
