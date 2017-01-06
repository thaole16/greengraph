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
    newyork = placesfile['New York']
    with patch.object(requests, 'get') as mock_get:
        expectedimage = file(os.path.join(os.path.dirname(__file__),'fixtures',newyork['image']),'rb').read()
        mock_get.return_value = mock_response = Mock()
        mock_response.content = expectedimage
        default_map = Map(newyork['lat'],newyork['long'],size=(newyork['sizesquare'],newyork['sizesquare']))
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
    placesfile = yaml.load(open(os.path.join(os.path.dirname(__file__), 'fixtures', 'places.yaml')))
    newyorkexpected = placesfile['New York']
    greenar = newyork.green(1.1)
    expected = newyorkexpected['green']
    assert (greenar == expected).all()


def test_count_green(newyork):
    with patch.object(newyork,'green') as MockClass:
        placesfile = yaml.load(open(os.path.join(os.path.dirname(__file__), 'fixtures', 'places.yaml')))
        newyorkexpected = placesfile['New York']
        MockClass.return_value = newyorkexpected['green']
        assert newyork.count_green() == newyorkexpected['countgreen']

        MockClass.return_value = [[False, True], [False, True]]
        assert newyork.count_green() == 2


def test_show_green(newyork):
    expectedgreen = file(os.path.join(os.path.dirname(__file__),'fixtures','newyork2x2green.png'),'rb').read()
    assert newyork.show_green() == expectedgreen