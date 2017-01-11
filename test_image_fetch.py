import image_fetch
from mock import patch, Mock

@patch('image_fetch.urlopen')
def test_find_image_src_attributes(mock_urlopen):
    a = Mock()
    a.read.side_effect = ["""<!DOCTYPE html>
              <html><body>
              <img src="cat.gif">
              <img src="dir/relative_cat.gif">
              <img src="http://test.com/absolute_cat.gif">
              </body></html>"""]
    mock_urlopen.return_value = a

    expected = ['cat.gif', 'dir/relative_cat.gif', 'http://test.com/absolute_cat.gif']
    assert image_fetch.find_image_src_attributes("http://example.com") == expected

