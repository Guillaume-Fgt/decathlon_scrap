from decathlon_scrap import config
import requests


def test_connection():
    "test if the request response is positive"
    path = config.URL
    headers = config.HEADERS
    page = requests.get(path, headers=headers)
    assert page.status_code == requests.codes.ok
