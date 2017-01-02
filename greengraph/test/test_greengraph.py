import pytest
import os
from greengraph.greengraph import Greengraph

#https://www.python.org/dev/peps/pep-0485/#proposed-implementation
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

@pytest.fixture(scope="module")
def graphobj():
    return Greengraph('New York', 'Chicago')

def test_Greengraph_init(graphobj):
    assert graphobj.start == 'New York'
    assert graphobj.end == 'Chicago'
    assert graphobj.end != 'Dog'
    assert graphobj.geocoder

def test_geolocate(graphobj):
    coords = graphobj.geolocate('New York')
    assert coords
    assert type(coords) == tuple
    assert isclose(coords[0],40.7127837)
    assert isclose(coords[1], -74.0059413)

def test_location_sequence(graphobj):
    sequence=graphobj.location_sequence((0, 0), (1, 1), 2)
    expected = [[ 0.,  0.],[ 1.,  1.]]
    assert (sequence==expected).all()

    sequence = graphobj.location_sequence((0, 0), (0, 1), 2)
    expected = [[0., 0.], [0., 1.]]
    assert (sequence == expected).all()

def test_green_between(graphobj):
    datapts = graphobj.green_between(2)
    expected = [60300, 28125]
    assert datapts == expected