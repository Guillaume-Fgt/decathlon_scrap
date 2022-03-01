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

"""Use selenium to populate availability columns of the database"""

# DB Path
path = config.DB_PATH
# Obtain availability status using selenium (because click button)
def selenium_avalaiblility(urls_bike):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    options = Options()
    options.headless = True  # don't show browser
    ser = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(options=options, service=ser)
    for i, urls in enumerate(urls_bike):
        st.sidebar.write(f":wrench: Processing url n°{i+1}/{len(urls_bike)}")
        url = urls
        driver.get(url)

        if i == 0:  # cookie alert on first loop
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
            )
            cookie_accept = driver.find_element(
                by="id", value="didomi-notice-agree-button"
            )
            cookie_accept.click()
        time.sleep(4)
        try:
            WebDriverWait(driver, 40).until(  # search for button to click)
                EC.element_to_be_clickable((By.CLASS_NAME, "svelte-1cr01ag"))
            )
            command_button = driver.find_element(
                by="class name", value="svelte-1cr01ag"
            )
            command_button.click()
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
                                "En stock (" + str(size.text.splitlines()[1]) + ")"
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
    connection.commit()
    connection.close()
    driver.quit()


def generate_url_list():
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    urls = cursor.execute(
        """
        SELECT bike_link
        FROM bike 
    """
    )

    list_urls = []
    [list_urls.append(url["bike_link"]) for url in urls]
    connection.close()
    return list_urls


if __name__ == "__main__":
    list_urls = generate_url_list()
    selenium_avalaiblility(list_urls)
