#!/usr/bin/python3

# TODO:
# * refactor:
#     - component that takes url, produces list of image urls
#     - add a test for this
# * handle exceptions for soup and request, handle http retval
# * add cli with params (url, output dir)
# * fetch all the images, save on disk
# * write a file with urls

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

def find_image_src_attributes(url, session=requests.Session()):
    request = session.get(url)
    request.raise_for_status()
    soup = BeautifulSoup(request.text, "html.parser")
    elements = soup.find_all(name="img")
    return [elem["src"] for elem in elements]

def find_image_urls (url):
    image_urls = find_image_src_attributes(url)
    return [urljoin(url, image_url) for image_url in image_urls]

# Tests for pytest-3, require requests_mock
def test_find_image_src_attributes():
    import requests_mock
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount("mock", adapter)

    html = """<!DOCTYPE html>
              <html><body>
              <img src="cat.gif">
              <img src="mock://test.com/absolute_cat.gif">
              </body></html>"""
    expected = ["cat.gif",
                "mock://test.com/absolute_cat.gif"]
    adapter.register_uri("GET", "mock://test.com/index.html", text=html)
    assert find_image_src_attributes("mock://test.com/index.html", session) == expected
