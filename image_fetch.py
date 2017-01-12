#!/usr/bin/python3

# TODO:
# * handle exceptions for soup, request and urllib: most are fine
#   as is, but e.g. image download failure should not lead to exit
# * handle http retvalues
# * decide filenames for images - try to decipher from uri or just
#   use "001" etc as name?
# * allow to specify a output directory other than working dir?

import sys, argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urlretrieve, urlopen

def _find_image_urls (url):
    """Return list of absolute urls for img elements found
       in the content of the given url"""
    response = urlopen(url)
    soup = BeautifulSoup(response.read(), "html.parser")
    elements = soup.find_all(name="img")
    image_urls = [elem["src"] for elem in elements]
    return [urljoin(url, image_url) for image_url in image_urls]

def _write_list_to_file(lines, filename):
    """Write the list of strings to given file"""
    if filename is not None:
        list_file = open(filename, 'w')

    for line in lines:
        if filename is None:
            print ("%s\n" % line)
        else:
            list_file.write("%s\n" % line)

def fetch_images(url, listfile):
    """Download all images found in the HTML content of given url,
       write the image URLs to a file"""
    urls = _find_image_urls(url)
    _write_list_to_file(urls, listfile)
    for url in urls:
        filename, headers = urlretrieve(url)
        print (filename)

def main():
    parser = argparse.ArgumentParser(description='Download images of a web page.')
    parser.add_argument('-l', '--listfile', type=str, default=None,
                        help='filename to write list of urls to (default is to print the list)')
    parser.add_argument("url", help="URL of the web page")
    args = parser.parse_args()

    fetch_images(args.url, args.listfile)

if __name__ == "__main__":
    main()

