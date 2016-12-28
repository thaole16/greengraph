import pytest

def test_Greengraph_init():
    from greengraph.greengraph import Greengraph
    mygraph = Greengraph('New York','Chicago')
    assert mygraph.start == 'New York'
    assert mygraph.end == 'Chicago'
    assert mygraph.end != 'Dog'
    assert mygraph.geocoder

