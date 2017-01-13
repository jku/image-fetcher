#!/usr/bin/python3

import argparse
import os
import sys
from urllib.parse import urljoin, urlparse
from urllib.request import urlretrieve, urlopen
from urllib.error import URLError
from html.parser import HTMLParser

class ImgSrcParser(HTMLParser):
    """Collects src-attribute values of all img-elements
       into the image_srcs set when parsing."""
    def __init__(self):
        HTMLParser.__init__(self)
        self.image_srcs = set()

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            try:
                self.image_srcs.add(dict(attrs)["src"])
            except KeyError as e:
                # No src attribute
                pass

def _get_charset(message):
    """Return charset, given a http.client.HTTPMessage"""
    if not message["content-type"] or not "charset=" in message["content-type"]:
        # utter guesswork
        return "utf-8"
    charset = message["content-type"].split("charset=")[1]
    return charset.split(";")[0]

def _find_image_urls(url):
    """Return list of absolute urls for img elements found
       in the content of the given url"""
    try:
        response = urlopen(url)
        charset = _get_charset(response.info())
        html = response.read().decode(charset)

        parser = ImgSrcParser()
        parser.feed(html)

        # Use the (possibly redirected) baseurl, in case url is not absolute already
        return [urljoin(response.geturl(), img_url) for img_url in parser.image_srcs]
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
    parsed_url = urlparse(url)
    base = os.path.basename(parsed_url.path)
    if base and parsed_url.query:
        base += "?"
    base += parsed_url.query

    if not base:
        base = "unnamed"

    # limit filename length to stay under common filesystem limits
    base = directory + "/" + base[-249:]

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
    retrieved_urls = []
    for url in urls:
        try:
            urlretrieve(url, _get_filename_for_url(url, directory))
            retrieved_urls.append(url)
        except Exception as e:
            # whatever the failure, we want to continue with next file
            print("Failed to retrieve %s: %s" % (url, e), file=sys.stderr)

    _write_list_to_file(retrieved_urls, listfile)

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

