from greengraph.greengraph import Map
import numpy as np

#https://www.python.org/dev/peps/pep-0485/#proposed-implementation
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

@pytest.fixture(scope="module")
def newyork():
    return Map(40.7127837, -74.0059413, size=(2, 2))

def test_Map_init(newyork):
    expectedimage = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x02\x04\x03\x00\x00\x00\x80\x98\x10\x17\x00\x00\x00\x0fPLTETPD``Td`Thh\\\xff\xff\xff\x13\xd3\x10z\x00\x00\x00\x01bKGD\x04\x8fh\xd9Q\x00\x00\x00\x0cIDAT\x08\xd7c0`\x10\x02\x00\x00\xa6\x00C\xb6\xe8\xbe\xee\x00\x00\x00\x00IEND\xaeB`\x82'
    expectedpixels = [[[ 0.40784314,  0.40784314,  0.36078432],[ 0.32941177,  0.3137255 ,  0.26666668]],[[ 0.3764706 ,  0.3764706 ,  0.32941177], [ 0.39215687,  0.3764706 ,  0.32941177]]]
    assert newyork.image == expectedimage
    assert np.allclose(newyork.pixels,expectedpixels)

def test_green(newyork):
    greenar = newyork.green(1.1)
    expected = [[False, False],[False, False]]
    assert (greenar==expected).all()

def test_count_green(newyork):
    assert newyork.count_green()==0

def test_show_green(newyork):
    expected = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x02\x08\x06\x00\x00\x00r\xb6\r$\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00\tpHYs\x00\x00\x0fa\x00\x00\x0fa\x01\xa8?\xa7i\x00\x00\x00\x14IDAT\x08\x99cd``\xf8\xcf\xc0\xc0\xc0\xc0\xc4\x00\x05\x00\x0e(\x01\x03\xb68\xca\xd3\x00\x00\x00\x00IEND\xaeB`\x82'
    assert newyork.show_green()==expected
