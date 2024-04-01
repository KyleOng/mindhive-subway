import sys
from pathlib import Path

# Add the parent directory of the current file to the system path
# This allows accessing methods defined in subdirectories of the parent directory.
sys.path.append(str(Path(__file__).parent.parent))

import logging
import sys
from datetime import datetime
from io import TextIOWrapper
from typing import List

from api import models
from api.db import Base, SessionLocal, engine
from lib.geocoding import geocoding_and_insert_coordinates
from scraper.chrome_driver import ChromeDriver, wait
from scraper.operating_hours_extractor import DAYS_OF_WEEK, OperatingHoursExtractor
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.orm import Session

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__package__)

URL = "https://subway.com.my/find-a-subway"
QUERY = "kuala lumpur"
FILE = "output.txt"


# Function to search for the input field and fill it with the search query
def search_input_field_and_fill(driver: WebDriver):
    search_address_input: WebElement = wait(
        driver,
        10,
        By.XPATH,
        "//input[@id='fp_searchAddress']",
        EC.visibility_of_element_located,
    )
    search_address_input.clear()
    search_address_input.send_keys(QUERY)


# Function to search for the input field button and click it
def search_input_field_button_and_click(driver: WebDriver):
    search_address_button: WebElement = wait(
        driver,
        10,
        By.XPATH,
        "//button[@id='fp_searchAddressBtn']",
        EC.element_to_be_clickable,
    )
    search_address_button.click()


# Function to process outlet operating hours
def process_outlet_operating_hours(
    text: str, db: Session, db_outlet: models.Outlet, file: TextIOWrapper
):
    text = text.replace(" ", "")
    extractor = OperatingHoursExtractor()

    operating_hours = extractor.extract_operating_hours_from_text(text)
    closing_day = extractor.extract_close_day_from_text(text)
    if closing_day != "" and closing_day in operating_hours.keys():
        operating_hours = {
            k: operating_hours[k] for k in operating_hours.keys() if k != closing_day
        }

    for day_of_week, operating_hour in operating_hours.items():
        start_time: datetime = operating_hour["start_time"]
        end_time: datetime = operating_hour["end_time"]
        start_time_str = datetime.strftime(start_time, "%I:%M %p")
        end_time_str = datetime.strftime(end_time, "%I:%M %p")
        file.write(day_of_week + " " + start_time_str + " - " + end_time_str + "\n")

        db_outlet_operating_hours = models.OperatingHour(
            outlet_id=db_outlet.id,
            day_of_week=DAYS_OF_WEEK.index(day_of_week),
            start_time=start_time,
            end_time=end_time,
        )
        db.add(db_outlet_operating_hours)
        db.commit()
        db.refresh(db_outlet_operating_hours)

    # fasting_operating_hours = extractor.extract_fasting_operating_hours_from_text(text)


# Function to extract name, address and info (contains operating hours which processed later)
def extract_name_address_info_from_left_panel(outlet: WebElement):
    left_panel = outlet.find_element(
        By.XPATH, ".//div[contains(@class, 'location_left')]"
    )
    outlet_name = left_panel.find_element(By.XPATH, "h4").text
    outlet_info = left_panel.find_element(
        By.XPATH, ".//div[contains(@class, 'infoboxcontent')]"
    )
    outlet_address = outlet_info.find_element(By.XPATH, ".//p[1]").text

    return outlet_name, outlet_address, outlet_info.text


# Function to extract waze link
def extract_waze_link_from_right_panel(outlet: WebElement):
    right_panel = outlet.find_element(
        By.XPATH, ".//div[contains(@class, 'location_right')]"
    )
    outlet_waze_link = (
        right_panel.find_element(
            By.XPATH, ".//a[contains(@href, 'waze')]"
        ).get_attribute("href")
        or ""
    )
    return outlet_waze_link


# Function to process outlets
def process_outlets(outlets: List[WebElement], db: Session, file: TextIOWrapper):
    for outlet in outlets:
        outlet_name, outlet_address, outlet_info = (
            extract_name_address_info_from_left_panel(outlet)
        )
        outlet_waze_link = extract_waze_link_from_right_panel(outlet)

        outlet_latitude, outlet_longitude = geocoding_and_insert_coordinates(
            outlet_address
        )

        file.write(outlet_name + "\n")
        file.write(outlet_waze_link + "\n")
        file.write(outlet_info + "\n")
        file.write(str(outlet_latitude) + ", " + str(outlet_longitude) + "\n")

        db_outlet = models.Outlet(
            name=outlet_name,
            address=outlet_address,
            waze_link=outlet_waze_link,
            latitude=outlet_latitude,
            longitude=outlet_longitude,
        )
        db.add(db_outlet)
        db.commit()
        db.refresh(db_outlet)

        process_outlet_operating_hours(outlet_info, db, db_outlet, file)
        logger.info(f"Outlet {db_outlet.name} with id {db_outlet.id} done")
        file.write("\n")


# Function to search for outlets and process them
def search_and_process_outlets(driver: WebDriver, db: Session, file: TextIOWrapper):
    # get outlets based on search query
    outlets: List[WebElement] = wait(
        driver,
        10,
        By.XPATH,
        "//div[contains(@class, 'fp_listitem') and not(contains(@style, 'display: none'))]",
        EC.visibility_of_all_elements_located,
    )
    process_outlets(outlets, db, file)


if __name__ == "__main__":
    # Tech debt: For time constraint, we truncate the tables
    # A better approach, would be check if outlet/operating hours exist in table before adding them.
    Base.metadata.drop_all(
        engine, tables=[models.OperatingHour.__table__, models.Outlet.__table__]
    )
    Base.metadata.create_all(
        engine, tables=[models.OperatingHour.__table__, models.Outlet.__table__]
    )

    with ChromeDriver() as driver, SessionLocal() as db, open(FILE, "w") as file:
        driver.get(URL)
        search_input_field_and_fill(driver)
        search_input_field_button_and_click(driver)
        search_and_process_outlets(driver, db, file)
