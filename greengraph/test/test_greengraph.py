import pytest
from greengraph.greengraph import Greengraph, Map
from mock import patch, Mock
import geopy
import requests
import yaml
import os

# https://www.python.org/dev/peps/pep-0485/#proposed-implementation
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


@pytest.fixture(scope="module")
def graphobj():
    return Greengraph('New York', 'Chicago')

@pytest.fixture(scope="module")
def graphobjexpected():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'places.yaml')) as placesfixtures:
        placesfile = yaml.load(placesfixtures)
        return placesfile['New York']

@pytest.fixture(scope="module")
def geocodeexpected(graphobjexpected):
    lat = graphobjexpected['lat']
    long = graphobjexpected['long']
    return geopy.location.Location(graphobjexpected['fullname'], (lat,long, 0.0))

def test_Greengraph_init(graphobj):
    assert graphobj.start == 'New York'
    assert graphobj.end == 'Chicago'
    assert graphobj.end != 'Dog'
    assert graphobj.geocoder

def test_geolocate(graphobj,graphobjexpected,geocodeexpected):
    with patch.object(graphobj.geocoder, 'geocode') as mock_get:
        mock_get.return_value = [geocodeexpected]
        coords = graphobj.geolocate(graphobjexpected['name'])
        mock_get.assert_called_with(
            graphobjexpected['name'],
            exactly_one=False
        )
        assert coords
        assert type(coords) == tuple
        assert isclose(coords[0], graphobjexpected['lat'])
        assert isclose(coords[1], graphobjexpected['long'])


def test_location_sequence(graphobj):
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'location_sequence.yaml')) as fixtures_file:
        fixtures = yaml.load(fixtures_file)
        for fixture in fixtures:
            if (fixture['error']==False):
                sequence =  graphobj.location_sequence(fixture['start'],fixture['end'],fixture['steps'])
                expected = fixture['expected']
                assert (sequence == expected).all()
            elif (fixture['error']==True):
                with pytest.raises(ValueError):
                    graphobj.location_sequence(fixture['start'],fixture['end'],fixture['steps'])

def test_green_between(graphobj,graphobjexpected,geocodeexpected):
    with patch.object(graphobj,'location_sequence') as MockClass: #mock a function call
        MockClass.return_value =[[0., 0.], [1., 1.]]
        with patch.object(graphobj.geocoder, 'geocode') as mock_get:
            mock_get.return_value = [geocodeexpected]
            with patch.object(requests, 'get') as mock_get:
                mock_get.return_value = mock_response = Mock()
                expectedimage=file(os.path.join(os.path.dirname(__file__),'fixtures',graphobjexpected['image']),'rb').read()
                mock_response.content = expectedimage
                with patch.object(Map,'count_green') as MockMap: #mock the Map (API hidden) call
                    MockMap.return_value = 0
                    datapts = graphobj.green_between(2)
                    assert datapts==[0,0]
