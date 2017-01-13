import os
import tempfile
from mock import patch, Mock
import image_fetch

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
attrs = {'read.return_value':html.encode('ISO-8859-1'), 'info.return_value':{'content-type':'text/html; charset=ISO-8859-1'}}
urlopen_mock_obj = Mock(**attrs)


@patch('image_fetch.urlopen')
def test_find_image_urls(mock_urlopen):
    mock_urlopen.return_value = urlopen_mock_obj

    expected = ['http://example.com/cat.gif',
                'http://example.com/dir/relative_cat.gif',
                'http://test.com/absolute_cat.gif']
    assert image_fetch._find_image_urls("http://example.com") == expected

def test_get_filename_for_url():
    tmpdir = tempfile.mkdtemp()
    handle, tmpfile = tempfile.mkstemp(dir=tmpdir)
    fn1 = image_fetch._get_filename_for_url("http://example.com/dir/file.ext", tmpdir)
    fn2 = image_fetch._get_filename_for_url("http://example.com/" + os.path.basename(tmpfile), tmpdir)
    fn3 = image_fetch._get_filename_for_url("http://example.com/dir/", tmpdir)
    fn4 = image_fetch._get_filename_for_url("http://example.com/file?query=cats", tmpdir)
    fn5 = image_fetch._get_filename_for_url("http://example.com/?query=cats", tmpdir)
    os.remove(tmpfile)
    os.rmdir(tmpdir)

    assert fn1 == tmpdir + "/file.ext"
    assert fn2 == tmpfile + "(2)"
    assert fn3 == tmpdir + "/unnamed"
    assert fn4 == tmpdir + "/file?query=cats"
    assert fn5 == tmpdir + "/query=cats"

