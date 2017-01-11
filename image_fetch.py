#!/usr/bin/python3

# TODO:
# * handle exceptions for soup, request and urllib
# * handle http retvalues
# * urlretrieve somewhere else than /tmp
# * maybe have a definable output dir?
# * maybe try to figure out filenames from url? really tricky though

from bs4 import BeautifulSoup
import requests
import sys
from urllib.parse import urljoin
from urllib.request import urlretrieve

def find_image_src_attributes(url, session=requests.Session()):
    request = session.get(url)
    request.raise_for_status()
    soup = BeautifulSoup(request.text, "html.parser")
    elements = soup.find_all(name="img")
    return [elem["src"] for elem in elements]

def find_image_urls (url):
    image_urls = find_image_src_attributes(url)
    return [urljoin(url, image_url) for image_url in image_urls]

def write_url_list(urls, filename):
    list_file = open(filename, 'w')
    for url in urls:
        list_file.write("%s\n" % url)

def fetch_images(url):
    urls = find_image_urls(url)
    write_url_list(urls, "testfile")
    for url in urls:
        filename, headers = urlretrieve(url)
        print (filename)

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

if __name__ == "__main__":
    if len(sys.argv) != 2 or "-h" in sys.argv or "--help" in sys.argv:
        print ("Usage:\n  %s <url>" % sys.argv[0])
        sys.exit()
    fetch_images(sys.argv[1])

