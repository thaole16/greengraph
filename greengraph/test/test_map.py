from greengraph.greengraph import Map
import numpy as np
import pytest
from mock import patch
from mock import Mock
import requests

import yaml
import os

# https://www.python.org/dev/peps/pep-0485/#proposed-implementation
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


@pytest.fixture(scope="module")
def newyork():
    placesfile = yaml.load(open(os.path.join(os.path.dirname(__file__),'fixtures', 'places.yaml')))
    newyork = placesfile[0]
    with patch.object(requests, 'get') as mock_get:
        expectedimage = file(os.path.join(os.path.dirname(__file__),'fixtures',newyork['image']),'rb').read()
        mock_get.return_value = mock_response = Mock()
        mock_response.content = expectedimage
        default_map = Map(newyork['lat'],newyork['long'],size=(newyork['sizesquare'],newyork['sizesquare']))
        #call = mock_get.mock_calls
        #assert "http://maps.googleapis.com/maps/api/staticmap?" in call
        mock_get.assert_called_with(
            "http://maps.googleapis.com/maps/api/staticmap?",
            params={
                'center': str(newyork['lat'])+','+str(newyork['long']),
                'zoom': 10,
                'maptype': 'satellite',
                'sensor': 'false',
                'size': str(newyork['sizesquare'])+'x'+str(newyork['sizesquare']),
                'style': 'feature:all|element:labels|visibility:off',
            }
        )
        return default_map

def test_Map_init(newyork):
    assert np.shape(np.array(newyork.pixels))==(2,2,3)


def test_green(newyork):
    greenar = newyork.green(1.1)
    expected = [[False, False], [False, False]]
    assert (greenar == expected).all()


def test_count_green(newyork):
    with patch.object(newyork,'green') as MockClass:
        MockClass.return_value =[[False, False], [False, False]]
        assert newyork.count_green() == 0

        MockClass.return_value = [[False, True], [False, True]]
        assert newyork.count_green() == 2


def test_show_green(newyork):
    expected = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x02\x08\x06\x00\x00\x00r\xb6\r$\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00\tpHYs\x00\x00\x0fa\x00\x00\x0fa\x01\xa8?\xa7i\x00\x00\x00\x14IDAT\x08\x99cd``\xf8\xcf\xc0\xc0\xc0\xc0\xc4\x00\x05\x00\x0e(\x01\x03\xb68\xca\xd3\x00\x00\x00\x00IEND\xaeB`\x82'
    assert newyork.show_green() == expected