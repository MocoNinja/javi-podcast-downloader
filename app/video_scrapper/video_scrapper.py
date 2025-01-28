from enum import Enum
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from app.common.logger import ROOT_LOGGER as log
from app.common.config import headless



class ScrapperType(Enum):
    FIREFOX = (1,)
    CHROME = 2


def create_scrapper(scrapper_type: ScrapperType):
    log.info(f"Create scrapper of type {scrapper_type}")
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
        raise Exception(f"Unhandled scrapper type {scrapper_type}")


def _configure_options(headless: bool, options: DesiredCapabilities):
    if headless:
        options.add_argument("--headless")
