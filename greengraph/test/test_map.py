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

@pytest.fixture(scope="module", params=['New York','Fake'])
def places(request):
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'places.yaml')) as placesfixtures:
        placesfile = yaml.load(placesfixtures)
        return placesfile[request.param]

@pytest.fixture(scope="module")
def mapreturn(places):
    with patch.object(requests, 'get') as mock_get:
        expectedimage = file(os.path.join(os.path.dirname(__file__),'fixtures',places['image']),'rb').read()
        mock_get.return_value = mock_response = Mock()
        mock_response.content = expectedimage
        default_map = Map(places['lat'],places['long'],size=(places['sizesquare'],places['sizesquare']))
        mock_get.assert_called_with(
            "http://maps.googleapis.com/maps/api/staticmap?",
            params={
                'center': str(places['lat'])+','+str(places['long']),
                'zoom': 10,
                'maptype': 'satellite',
                'sensor': 'false',
                'size': str(places['sizesquare'])+'x'+str(places['sizesquare']),
                'style': 'feature:all|element:labels|visibility:off',
            }
        )
        return default_map

def test_Map_init(mapreturn):
    assert np.shape(np.array(mapreturn.pixels))==(2,2,3)

def test_green(mapreturn,places):
    greenar = mapreturn.green(1.1)
    expected = places['green']
    assert (greenar == expected).all()


def test_count_green(mapreturn,places):
    with patch.object(mapreturn,'green') as MockClass:
        MockClass.return_value = places['green']
        assert mapreturn.count_green() == places['countgreen']


def test_show_green(mapreturn,places):
    expectedgreen = file(os.path.join(os.path.dirname(__file__),'fixtures',places['greenimage']),'rb').read()
    assert mapreturn.show_green() == expectedgreen
