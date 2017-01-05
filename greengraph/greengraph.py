import numpy as np
import geopy
from StringIO import StringIO
from matplotlib import image as img
import requests


"""
Created in 2016 or earlier
@author: James Hetherington ?
"""

class Greengraph(object):
    """
    Create a new greengraph object with locations *start* and *end*
    """
    def __init__(self, start, end):
        """

        :param start: Name of the starting place
        :param end: Name of the ending place
        """
        self.start=start
        self.end=end
        self.geocoder=geopy.geocoders.GoogleV3(
          domain="maps.google.co.uk")

    def geolocate(self, place):
        """
        Finds the latitude and longitude coordinates of *place*
        :param place: Name of a place
        :return: The coordinates as a tuple
        """
        return self.geocoder.geocode(place,
          exactly_one=False)[0][1]

    def location_sequence(self, start,end,steps):
        """

        :param start: (lat,long) tuple of starting location
        :param end: (lat,long) tuple of ending location
        :param steps: Number of locations in between to sample
        :return: A numpy array of (latitude,longitude) locations between *start* place and *end* place
        """
        lats = np.linspace(start[0], end[0], steps)
        longs = np.linspace(start[1],end[1], steps)
        return np.vstack([lats, longs]).transpose()

    def green_between(self, steps):
        """

        :param steps: number of locations to sample between
        :return:  a list of the number of green pixels (pixels that are more green than blue or red) at the locations given by **location_sequence**
        """
        return [Map(*location).count_green()
                for location in self.location_sequence(
                    self.geolocate(self.start),
                    self.geolocate(self.end),
                    steps)]

"""
Created in 2016 or earlier
@author: James Hetherington ?
With some/a bug fix by Thao Le in 2016/2017
"""

class Map(object):
    """
        A map object contains the image (png and RGB array) of the location
    """
    def __init__(self, lat, long, satellite=True,
          zoom=10, size=(400,400), sensor=False):
        """
        Create a new Map object that contains the image of the location (latitude,longitude)
        :param lat: Latitude
        :param long: Longitude
        """
        base="http://maps.googleapis.com/maps/api/staticmap?"

        params=dict(
            sensor= str(sensor).lower(),
               zoom= zoom,
               size= "x".join(map(str, size)),
               center= ",".join(map(str, (lat, long) )),
               style="feature:all|element:labels|visibility:off"
             )

        if satellite:
            params["maptype"]="satellite"

        self.image = requests.get(base, params=params).content
        # Fetch our PNG image data
        self.pixels= img.imread(StringIO(self.image))
        # Parse our PNG image as a numpy array

    def green(self, threshold):
        """

        :param threshold: How much more green (in RGB terms) a pixel needs to have to be called "green"
        :return: A boolean array of whether a pixel is green or not
        """
        # Use NumPy to build an element-by-element logical array
        greener_than_red = self.pixels[:,:,1] > threshold* self.pixels[:,:,0]
        greener_than_blue = self.pixels[:,:,1] > threshold*self.pixels[:,:,2]
        green = np.logical_and(greener_than_red, greener_than_blue)
        return green

    def count_green(self, threshold = 1.1):
        """

        :param threshold: How much more green (in RGB terms) a pixel needs to have to be called "green"
        :return: the number of green pixels in the map
        """
        return np.sum(self.green(threshold))

    def show_green(self, threshold = 1.1):
        """

        :param threshold: How much more green (in RGB terms) a pixel needs to have to be called "green"
        :return: an image that highlights the pixels that are green (and black everywhere else)
        """
        green = self.green(threshold)
        out = green[:,:,np.newaxis]*np.array([0,1,0])[np.newaxis,np.newaxis,:]
        buffer = StringIO()
        result = img.imsave(buffer, out, format='png')
        return buffer.getvalue()