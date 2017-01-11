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

url = "https://www.google.fi/search?q=cats"

try:
    request = requests.get(url)
    print(request.status_code)
    soup = BeautifulSoup(request.text, "html.parser")
    image_urls = [elem["src"] for elem in soup.find_all(name="img")]
    print(image_urls)
except Exception as e:
    print(e)

