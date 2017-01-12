import image_fetch
from mock import patch, Mock

# Tests compatible with pytest-3

# Create a mock of urllib.urlopen() return value: it's an object
# with a read() function that returns the html.
html = """<!DOCTYPE html>
          <html>
          <body>
          <img src="cat.gif">
          <img src="dir/relative_cat.gif">
          <img src="http://test.com/absolute_cat.gif">
          </body>
          </html>"""
attrs = {'read.return_value':html}
urlopen_mock_obj = Mock(**attrs)


@patch('image_fetch.urlopen')
def test_find_image_urls(mock_urlopen):
    mock_urlopen.return_value = urlopen_mock_obj

    expected = ['http://example.com/cat.gif',
                'http://example.com/dir/relative_cat.gif',
                'http://test.com/absolute_cat.gif']
    assert image_fetch._find_image_urls("http://example.com") == expected

