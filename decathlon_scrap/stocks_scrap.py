from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import sqlite3
import time
import streamlit as st
import config
from db_operations import open_db
from contextlib import contextmanager

"""Use selenium to populate availability columns of the database"""


def generate_url_list() -> list[str]:
    """return a list of all urls existing in the bike database"""
    with open_db(config.DB_PATH) as cursor:
        urls = cursor.execute(
            """
            SELECT bike_link
            FROM bike 
        """
        )
        list_urls = [url["bike_link"] for url in urls]
    return list_urls


def find_and_click_button(
    driver: webdriver, timeout: int, locator: By, webelement: str
) -> None:
    """locate a button on a webpage using html tags and click on it"""
    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((locator, webelement))
    )
    cookie_accept = driver.find_element(locator, webelement)
    cookie_accept.click()


@contextmanager
def selenium_driver():
    options = Options()
    options.headless = True  # don't show browser
    ser = Service(GeckoDriverManager().install())
    try:
        driver = webdriver.Firefox(options=options, service=ser)
        yield driver
    finally:
        driver.quit()


def selenium_avalaiblility(urls_bike: list[str]) -> None:
    """Obtain availability status using selenium (because click button)"""
    with selenium_driver() as driver:
        with open_db(config.DB_PATH) as cursor:
            for i, url in enumerate(urls_bike):
                st.sidebar.write(f":wrench: Processing url n°{i+1}/{len(urls_bike)}")

                driver.get(url)

                if i == 0:  # cookie alert on first loop
                    find_and_click_button(
                        driver, 30, By.ID, "didomi-notice-agree-button"
                    )
                time.sleep(4)
                try:
                    find_and_click_button(driver, 40, By.CLASS_NAME, "svelte-1cr01ag")
                    time.sleep(2)
                    sizes = driver.find_elements(by="class name", value="size-option")
                    # only some sizes are found for each bike. To keep consistency, we use a dict with all sizes
                    dict_size = {
                        "2XS": "N/A",
                        "XS": "N/A",
                        "S": "N/A",
                        "M": "N/A",
                        "L": "N/A",
                        "XL": "N/A",
                    }

                    for size in sizes:
                        for key, value in dict_size.items():
                            if key == size.text.splitlines()[0]:
                                if size.text.splitlines()[
                                    1
                                ].isdigit():  # sometimes, a number of bike is provide. Change it to filter in Streamlit later
                                    dict_size[key] = (
                                        "En stock ("
                                        + str(size.text.splitlines()[1])
                                        + ")"
                                    )
                                else:
                                    dict_size[key] = size.text.splitlines()[1]
                    for key, value in dict_size.items():
                        cursor.execute(
                            """
                            UPDATE bike SET (XXS, XS, S, M, L ,XL) = (?,?,?,?,?,?)
                            WHERE bike_link LIKE ?
                        """,
                            (
                                dict_size["2XS"],
                                dict_size["XS"],
                                dict_size["S"],
                                dict_size["M"],
                                dict_size["L"],
                                dict_size["XL"],
                                url,
                            ),
                        )
                except:  # some bike don't have a button to click. Only a unique size exists (like for child bike)
                    cursor.execute(
                        """
                        UPDATE bike SET (XXS, XS, S, M, L ,XL) = (?,?,?,?,?,?)
                        WHERE bike_link LIKE ?
                    """,
                        (
                            "Taille unique",
                            "Taille unique",
                            "Taille unique",
                            "Taille unique",
                            "Taille unique",
                            "Taille unique",
                            url,
                        ),
                    )


def main() -> None:
    list_urls = generate_url_list()
    selenium_avalaiblility(list_urls)


if __name__ == "__main__":
    main()
