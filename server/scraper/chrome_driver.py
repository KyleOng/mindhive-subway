import logging
from typing import Callable

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger(__package__)


class ChromeDriver:
    def __init__(self) -> None:
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--window-size=1920,1080")

    def __enter__(self) -> webdriver.Chrome:
        self.driver = webdriver.Chrome(options=self.chrome_options)
        logger.info("driver started")
        return self.driver

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.driver.close()
        logger.info("driver stopped")

        if exc_type:
            logger.error("%s %s %s" % (exc_type, exc_value, exc_traceback))


# Wait until the specified condition is met on the WebDriver.
def wait(
    driver: WebDriver,
    timeout: int,
    by: str,
    value: str,
    expected_conditions_function: Callable,
):
    return WebDriverWait(driver, timeout).until(
        expected_conditions_function((by, value))
    )
