import requests
from bs4 import BeautifulSoup
import config
from db_operations import populate_database

"""
Use Beautiful Soup to populate columns bike_name, price and url_bike of the database
"""


def scrap_bike(
    urls: list[str], headers: dict
) -> tuple[list[str], list[str], list[str]]:
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


def main() -> None:
    velos, prix, links = scrap_bike(config.URLS, config.HEADERS)
    populate_database(config.DB_PATH, velos, prix, links)


if __name__ == "__main__":
    main()
