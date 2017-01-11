#!/usr/bin/python3

# TODO:
# * handle exceptions for soup, request and urllib
# * handle http retvalues
# * urlretrieve somewhere else than /tmp
# * maybe have a definable output dir?
# * maybe try to figure out filenames from url? really tricky though

from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin
from urllib.request import urlretrieve, urlopen

def find_image_src_attributes(url):
    response = urlopen(url)
    soup = BeautifulSoup(response.read(), "html.parser")
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

if __name__ == "__main__":
    if len(sys.argv) != 2 or "-h" in sys.argv or "--help" in sys.argv:
        print ("Usage:\n  %s <url>" % sys.argv[0])
        sys.exit()
    fetch_images(sys.argv[1])

