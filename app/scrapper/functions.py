from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from app.config import ROOT_LOGGER as log

accept_btn_selector = "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[2]/div/div/button/span"


def accept_button_click(driver, error_on_failure=True):
    try:
        accept_btn = driver.find_element(By.XPATH, accept_btn_selector)
        accept_btn.click()
    except NoSuchElementException as e:
        log.error(f"Cannot find accept button: {e.msg}")
        if error_on_failure:
            raise Exception("Could not click accept button")
