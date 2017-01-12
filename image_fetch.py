#!/usr/bin/python3

# TODO:
# * handle exceptions for soup, request and urllib: most are fine
#   as is, but e.g. image download failure should not lead to exit
# * handle http retvalues
# * decide filenames for images - try to decipher from uri or just
#   use "001" etc as name?
# * decide filename for the url list?
# * allow to specify a output directory other than working dir?
# * use proper options handling

from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin
from urllib.request import urlretrieve, urlopen

def _find_image_src_attributes(url):
    response = urlopen(url)
    soup = BeautifulSoup(response.read(), "html.parser")
    elements = soup.find_all(name="img")
    return [elem["src"] for elem in elements]

def _find_image_urls (url):
    """Return list of absolute urls for img elements found
       in the content of the given url"""
    image_urls = _find_image_src_attributes(url)
    return [urljoin(url, image_url) for image_url in image_urls]

def _write_list_to_file(lines, filename):
    """Write the list of strings to given file"""
    list_file = open(filename, 'w')
    for line in lines:
        list_file.write("%s\n" % line)

def fetch_images(url):
    """Download all images found in the HTML content of given url,
       write the image URLs to a file"""
    urls = _find_image_urls(url)
    _write_list_to_file(urls, "testfile")
    for url in urls:
        filename, headers = urlretrieve(url)
        print (filename)

if __name__ == "__main__":
    if len(sys.argv) != 2 or "-h" in sys.argv or "--help" in sys.argv:
        print ("Usage:\n  %s <url>" % sys.argv[0])
        sys.exit()
    fetch_images(sys.argv[1])

