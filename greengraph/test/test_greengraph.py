import pytest
import os
from greengraph.greengraph import Greengraph

#https://www.python.org/dev/peps/pep-0485/#proposed-implementation
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def test_Greengraph_init():
    mygraph = Greengraph('New York','Chicago')
    assert mygraph.start == 'New York'
    assert mygraph.end == 'Chicago'
    assert mygraph.end != 'Dog'
    assert mygraph.geocoder

def test_geolocate():
    mygraph = Greengraph('New York', 'Chicago')
    coords = mygraph.geolocate('New York')
    assert coords
    assert type(coords) == tuple
    assert isclose(coords[0],40.7127837)
    assert isclose(coords[1], -74.0059413)