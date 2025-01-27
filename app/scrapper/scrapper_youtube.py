from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from app.scrapper.functions import accept_button_click
from app.video.video_dto import VideoDto
from app.video.video_provider import VideoProvider
from app.config import ROOT_LOGGER as log
from app.config import sleep_scrapper_seconds as DELAY

video_selector = '//*[@id="content"]'


def scrape_youtube(url, scroll=1000, headless=True):
    log.info(f"Scrapping {url}...")
    options = FirefoxOptions()
    if headless:
        options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    driver.get(url)
    data = {}
    try:
        data = _do(driver, scroll)
    except Exception as e:
        log.error(f"Error scrapping: {e}")

    driver.close()
    return data


def _do(driver, scroll):
    accept_button_click(driver)
    sleep(DELAY)
    if scroll is not None:
        _bruteforce_scroll(driver, pages=scroll)
        sleep(DELAY)
    payload = _scrape_data(driver)
    return payload


# Debería intentar ver algo más listo que escrapee una "pagina" y pare cuando ya tenga elementos
# De momento que antes de empezar baje al final y escrapee todas como un campeon
# Esto va a ser mejor porque tampoco sabemos cuando parar y a infinito cualquier numero que pongamos se quedara corto
# Pero bueno, hay que intentar que esto me baje los cripipastas y que no sea una víctima más en mi sótano digital...
def _bruteforce_scroll(driver, pages=50, scroll_pause_time=0.25):
    body = driver.find_element(By.TAG_NAME, "body")
    for page in range(0, pages):
        log(f"Scrolling page {page + 1} / {pages}...")
        body.send_keys(Keys.CONTROL + Keys.END)
        sleep(scroll_pause_time)


def _scrape_data(driver):
    video_data = {}
    videos = driver.find_elements(By.XPATH, video_selector)
    for video in videos:
        try:
            video_title_link = video.find_element(
                By.XPATH, ".//a[@id='video-title-link']"
            )
            url = video_title_link.get_attribute("href")
            title = video_title_link.get_attribute("title")
            # video_meta_block = video.find_element(By.XPATH, ".//ytd-video-meta-block")
            # TODO: hacerlo con una lambda confiruable o algo
            # if not  bool(re.match(r"The Wild Project #\d+ .+", title)):
            # print(f"{title} no matchea regex, pasando...")
            #    continue
            # print(f"{title} matchea regex, guardando...")
            item = VideoDto(url, title, VideoProvider.YOUTUBE)
            video_data[url] = item

        except Exception as e:
            log.error(f"Error accessing elements:", e)
    return video_data
