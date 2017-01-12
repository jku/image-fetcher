`image_fetch.py` downloads images from a web page. It does not follow links, just fetches whatever is in src attributes of every img-element in page.

Depends on core python modules (urllib, html). Tests also depend on mock and are compatible with pytest-3.

    usage: image_fetch.py [-h] [-l LISTFILE] [-d DIRECTORY] url

    Download images of a web page.

    positional arguments:
      url                   URL of the web page

    optional arguments:
      -h, --help            show this help message and exit
      -l LISTFILE, --listfile LISTFILE
                            filename to write list of urls to (default is to print
                            the list)
      -d DIRECTORY, --directory DIRECTORY
                            directory to download images to (default is current
                            directory)
