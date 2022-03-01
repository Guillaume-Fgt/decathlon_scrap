import sqlite3
import requests
from bs4 import BeautifulSoup
import config

"""
Use Beautiful Soup to populate columns bike_name, price and url_bike of the database
"""


def scrap_prices_bike():
    urls = [config.URL]
    headers = config.HEADERS
    velos_list = []
    prix_velos_list = []
    links_velo_list = []
    for url in urls:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "lxml")
        velos = soup("h2", "svelte-gtybwu")
        prix_list = soup("div", "prc__active-price")
        links_list = soup("a", "dpb-product-model-link svelte-gtybwu")
        [velos_list.append(velo.contents[0].capitalize()) for velo in velos]
        [prix_velos_list.append(prix["content"]) for prix in prix_list]
        [
            links_velo_list.append("https://www.decathlon.fr" + links["href"])
            for links in links_list
        ]
    return (velos_list, prix_velos_list, links_velo_list)


def populate_db():
    velos, prix, links = scrap_prices_bike()

    path = config.DB_PATH
    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    for ind, velo in enumerate(velos):
        cursor.execute(
            "INSERT INTO bike (bike_name, price, bike_link) VALUES (?, ?, ?)",
            (
                velo,
                prix[ind],
                links[ind],
            ),
        )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    populate_db()
