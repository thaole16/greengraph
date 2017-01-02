import pytest
from greengraph.greengraph import Greengraph, Map
from mock import patch, Mock
import geopy
import requests

# https://www.python.org/dev/peps/pep-0485/#proposed-implementation
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


@pytest.fixture(scope="module")
def graphobj():
    return Greengraph('New York', 'Chicago')

def test_Greengraph_init(graphobj):
    assert graphobj.start == 'New York'
    assert graphobj.end == 'Chicago'
    assert graphobj.end != 'Dog'
    assert graphobj.geocoder

def test_geolocate(graphobj):
    with patch.object(graphobj.geocoder, 'geocode') as mock_get:
        mock_get.return_value = [geopy.location.Location('New York, NY, USA', (40.7127837, -74.0059413, 0.0))]
        coords = graphobj.geolocate('New York')
        mock_get.assert_called_with(
            'New York',
            exactly_one=False
        )
        assert coords
        assert type(coords) == tuple
        assert isclose(coords[0], 40.7127837)
        assert isclose(coords[1], -74.0059413)


def test_location_sequence(graphobj):
    sequence = graphobj.location_sequence((0, 0), (1, 1), 2)
    expected = [[0., 0.], [1., 1.]]
    assert (sequence == expected).all()

    sequence = graphobj.location_sequence((0, 0), (0, 1), 2)
    expected = [[0., 0.], [0., 1.]]
    assert (sequence == expected).all()


def test_green_between(graphobj):
    with patch.object(graphobj,'location_sequence') as MockClass: #mock a function call
        MockClass.return_value =[[0., 0.], [1., 1.]]
        with patch.object(Map,'count_green') as MockMap: #mock the Map (API hidden) call
            MockMap.return_value = 0
            datapts = graphobj.green_between(2)
            assert datapts==[0,0]
