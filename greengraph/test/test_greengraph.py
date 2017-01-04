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
    with open(os.path.join(os.path.dirname(__file__),
                           'fixtures', 'location_sequence.yaml')) as fixtures_file:
        fixtures = yaml.load(fixtures_file)
        print(fixtures)
        for fixture in fixtures:
            if (fixture['error']==False):
                sequence =  graphobj.location_sequence(fixture['start'],fixture['end'],fixture['steps'])
                expected = fixture['expected']
                assert (sequence == expected).all()
            elif (fixture['error']==True):
                with pytest.raises(ValueError):
                    graphobj.location_sequence(fixture['start'],fixture['end'],fixture['steps'])

def test_green_between(graphobj):
    with patch.object(graphobj,'location_sequence') as MockClass: #mock a function call
        MockClass.return_value =[[0., 0.], [1., 1.]]
        with patch.object(graphobj.geocoder, 'geocode') as mock_get:
            mock_get.return_value = [geopy.location.Location('New York, NY, USA', (40.7127837, -74.0059413, 0.0))]
            with patch.object(requests, 'get') as mock_get:
                expectedimage = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x02\x04\x03\x00\x00\x00\x80\x98\x10\x17\x00\x00\x00\x0fPLTETPD``Td`Thh\\\xff\xff\xff\x13\xd3\x10z\x00\x00\x00\x01bKGD\x04\x8fh\xd9Q\x00\x00\x00\x0cIDAT\x08\xd7c0`\x10\x02\x00\x00\xa6\x00C\xb6\xe8\xbe\xee\x00\x00\x00\x00IEND\xaeB`\x82'
                mock_get.return_value = mock_response = Mock()
                mock_response.content = expectedimage
                with patch.object(Map,'count_green') as MockMap: #mock the Map (API hidden) call
                    MockMap.return_value = 0
                    datapts = graphobj.green_between(2)
                    assert datapts==[0,0]
