==========
Greengraph
==========

Greengraph generates a graph of the porportion of green pixels in a series of satellite images between two points
(locations on Earth). As input, it will take in the names of the two locations, along with the number of steps/points
to sample in-between. Whether a point is green or not is determined by whether it is "more green" than it is red or
blue.

The greengraph.py code is taken from the appendix of the MPHYG001 First Continous Assessment pdf file, which in turn
comes from https://github.com/UCL/rsd-engineeringcourse/blob/master/ch01data/110Capstone.ipynb

Installation Instructions
=========================

To install via pip:

    pip install git+https://github.com/thaole16/greengraph.git

Otherwise, you can download [Greengraph](https://github.com/thaole16/greengraph/archive/master.zip)

Typical Usage
=============

Typical usage would look like this:

    #!/usr/bin/env python

    from greengraph.greengraph import Greengraph, Map
    from matplotlib import pyplot as plt

    mygraph=Greengraph('New York','Chicago')
    data = mygraph.green_between(20)
    plt.plot(data)

Alternatively, commandline usage would look like this:

    greengraph --start "New York" --end "Chicago" --steps 20 --imageout dataplot.png --dataout data.txt
