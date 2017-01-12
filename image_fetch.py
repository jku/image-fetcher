#!/usr/bin/python3

import argparse
import os
import sys
from urllib.parse import urljoin, urlparse
from urllib.request import urlretrieve, urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup

def _find_image_urls(url):
    """Return list of absolute urls for img elements found
       in the content of the given url"""
    try:
        response = urlopen(url)
        soup = BeautifulSoup(response.read(), "html.parser")
        elements = soup.find_all(name="img")
        image_urls = [elem["src"] for elem in elements]
        return [urljoin(url, image_url) for image_url in image_urls]
    except (URLError, ValueError) as e:
        print("Failed to fetch '%s': %s" % (url, e), file=sys.stderr)
        return []

def _write_list_to_file(lines, filename):
    """Write the list of strings to given file"""
    if filename is not None:
        list_file = open(filename, 'w')

    for line in lines:
        if filename is None:
            print("%s" % line)
        else:
            list_file.write("%s\n" % line)

def _get_filename_for_url(url, directory):
    """Makes up a filename for given url. Tries to make one that
       does not exist in directory yet"""
    base = os.path.basename(urlparse(url).path)
    if not base:
        base = "unnamed"
    base = directory + "/" + base

    count = 1
    filename = base
    while os.path.exists(filename):
        count += 1
        filename = base + "(" + str(count) + ")"
    return filename


def fetch_images(url, listfile, directory):
    """Download all images found in the HTML content of given url into
       given directory, write the image URLs to a file. Will overwrite
       listfile if it exists, but tries not to overwrite image files."""
    urls = _find_image_urls(url)
    _write_list_to_file(urls, listfile)
    for url in urls:
        try:
            urlretrieve(url, _get_filename_for_url(url, directory))
        except Exception as e:
            # whatever the failure, we want to continue with next file
            print("Failed to retrieve %s: %s" % (url, e), file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description='Download images of a web page.')
    parser.add_argument('-l', '--listfile', type=str, default=None,
                        help='filename to write list of urls to (default is to print the list)')
    parser.add_argument('-d', '--directory', type=str, default=os.getcwd(),
                        help='directory to download images to (default is current directory)')
    parser.add_argument("url", help="URL of the web page")
    args = parser.parse_args()

    if os.path.exists(args.directory) and not os.path.isdir(args.directory):
        print("Error: '%s' exists and is not a directory." % args.directory, file=sys.stderr)
        exit()
    if not os.path.exists(args.directory):
        os.mkdir(args.directory)

    try:
        fetch_images(args.url, args.listfile, args.directory)
    except Exception as e:
        # oops, this is definitely fatal
        print("Error: %s" % e, file=sys.stderr)

if __name__ == "__main__":
    main()

