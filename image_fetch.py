#!/usr/bin/python3

# TODO:
# * handle exceptions for soup, request and urllib: most are fine
#   as is, but e.g. image download failure should not lead to exit
# * handle http retvalues
# * allow to specify a output directory other than working dir?

import sys, argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.request import urlretrieve, urlopen
from os.path import basename, exists, isdir

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
            print ("%s" % line)
        else:
            list_file.write("%s\n" % line)

def _get_filename_for_url (url, directory):
    """Makes up a filename for given url. Tries to make one that
       does not exist in directory yet"""
    base = basename(urlparse(url).path)
    if not base:
        base = "unnamed"
    base = directory + "/" + base

    count = 1
    filename = base
    while exists(filename):
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
            print ("Failed to retrieve %s: %s" % (url, e))

def main():
    parser = argparse.ArgumentParser(description='Download images of a web page.')
    parser.add_argument('-l', '--listfile', type=str, default=None,
                        help='filename to write list of urls to (default is to print the list)')
    parser.add_argument('-d', '--directory', type=str, default=None,
                        help='directory to download images to (default is current directory)')
    parser.add_argument("url", help="URL of the web page")
    args = parser.parse_args()

    if exists(args.directory) and not isdir(args.directory):
        print ("Error: '%s' exists and is not a directory." % args.directory)
        exit()
    if not exists(args.directory):
        os.mkdir (args.directory)

    fetch_images(args.url, args.listfile, args.directory)

if __name__ == "__main__":
    main()

