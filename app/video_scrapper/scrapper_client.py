from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from app.common.config import ScrapperType, headless
from app.common.logger import fatal, info, warning


def create_scrapper(scrapper_type: ScrapperType):
    info(f"Create scrapper of type {scrapper_type}")
    if scrapper_type == ScrapperType.CHROME:
        warning("WARNING! In my testing, I could see that Chrome works like 💩")
    driver_class, options_class = _get_driver_for_type(scrapper_type)
    options = options_class()

    _configure_options(headless, options)

    driver = driver_class(options=options)
    return driver


def _get_driver_for_type(scrapper_type: ScrapperType):
    if scrapper_type == ScrapperType.FIREFOX:
        return webdriver.Firefox, FirefoxOptions
    elif scrapper_type == ScrapperType.CHROME:
        return webdriver.Chrome, ChromeOptions
    else:
        fatal(f"Unhandled scrapper type {scrapper_type}")
        exit(1)


def _configure_options(headless_webdriver: bool, options: DesiredCapabilities):
    if headless_webdriver:
        options.add_argument("--headless")
