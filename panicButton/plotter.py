import json
import math
import os
import requests
import io

from color_dicts import mpl_color_map, html_color_codes


def safe_iter(var):
    try:
        return iter(var)
    except TypeError:
        return [var]


class GoogleMapPlotter(object):

    def __init__(self, center_lat, center_lng, zoom, apikey=''):
        self.center = (float(center_lat), float(center_lng))
        self.zoom = int(zoom)
        self.apikey = str(apikey)
        self.grids = None
        self.paths = []
        self.shapes = []
        self.points = []
        self.heatmap_points = []
        self.radpoints = []
        self.gridsetting = None
        self.coloricon = os.path.join(os.path.dirname(__file__), 'markers/%s.png')
        self.color_dict = mpl_color_map
        self.html_color_codes = html_color_codes

    @classmethod
    def setter_latlong(self, latitude, longitude):
        self.center = (float(latitude), float(longitude))

    def heatmap(self, lats, lngs, threshold=10, radius=10, gradient=None, opacity=0.8, maxIntensity=4,
                dissipating=True):
        """
        :param lats: list of latitudes
        :param lngs: list of longitudes
        :param maxIntensity:(int) max frequency to use when plotting. Default (None) uses max value on map domain.
        :param threshold:
        :param radius: The hardest param. Example (string):
        :return:
        """
        settings = {'threshold': threshold, 'radius': radius, 'gradient': gradient, 'opacity': opacity,
                    'maxIntensity': maxIntensity, 'dissipating': dissipating}
        settings_string = self._process_heatmap_kwargs(settings)

        heatmap_points = []
        for lat, lng in zip(lats, lngs):
            heatmap_points.append((lat, lng))
        self.heatmap_points.append((heatmap_points, settings_string))

    def _process_heatmap_kwargs(self, settings_dict):

        settings_string = ''
        settings_string += "heatmap.set('threshold', %d);\n" % settings_dict['threshold']
        settings_string += "heatmap.set('radius', %d);\n" % settings_dict['radius']
        settings_string += "heatmap.set('maxIntensity', %d);\n" % settings_dict['maxIntensity']
        settings_string += "heatmap.set('opacity', %f);\n" % settings_dict['opacity']

        dissipation_string = 'true' if settings_dict['dissipating'] else 'false'
        settings_string += "heatmap.set('dissipating', %s);\n" % (dissipation_string)

        gradient = settings_dict['gradient']
        if gradient:
            gradient_string = "var gradient = [\n"
            for r, g, b, a in gradient:
                gradient_string += "\t" + "'rgba(%d, %d, %d, %d)',\n" % (r, g, b, a)
            gradient_string += '];' + '\n'
            gradient_string += "heatmap.set('gradient', gradient);\n"

            settings_string += gradient_string

        return settings_string

    def draw(self):  # htmlfile=None
        """Create the html file which include one google map and all points and paths. If
        no string is provided, return the raw html. NOTE: This feature may disappear in
        a future version because it creates two very different APIs with a single param.
        Recommended method is to use temporary files until a real motivation appears.
        """
        s = ""

        s += ('<html>\n')
        s += ('<head>\n')
        s += (
            '<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />\n')
        s += (
            '<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>\n')
        s += ('<title>Google Maps - gmplot </title>\n')
        if self.apikey:
            s += (
                    '<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=visualization&sensor=true_or_false&key=%s"></script>\n' % self.apikey)
        else:
            s += (
                '<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=visualization&sensor=true_or_false"></script>\n')
        s += ('<script type="text/javascript">\n')
        s += ('\tfunction initialize() {\n')
        s += self.write_map(s)
        s += self.write_heatmap(s)
        s += ('\t}\n')
        s += ('</script>\n')
        s += ('</head>\n')
        s += (
            '<body style="margin:0px; padding:0px;" onload="initialize()">\n')
        s += (
            '\t<div id="map_canvas" style="width: 100%; height: 100%;"></div>\n')
        s += ('</body>\n')
        s += ('</html>\n')

        return s

    #############################################
    # # # # # # Low level Map Drawing # # # # # #
    #############################################

    def write_map(self, s):
        s += ('\t\tvar centerlatlng = new google.maps.LatLng(%f, %f);\n' %
              (self.center[0], self.center[1]))
        s += ('\t\tvar myOptions = {\n')
        s += ('\t\t\tzoom: %d,\n' % (self.zoom))
        s += ('\t\t\tcenter: centerlatlng,\n')
        s += ('\t\t\tmapTypeId: google.maps.MapTypeId.ROADMAP\n')
        s += ('\t\t};\n')
        s += (
            '\t\tvar map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);\n')
        s += ('\n')
        return s

    def write_heatmap(self, s):
        for heatmap_points, settings_string in self.heatmap_points:
            s += ('var heatmap_points = [\n')
            for heatmap_lat, heatmap_lng in heatmap_points:
                s += ('new google.maps.LatLng(%f, %f),\n' %
                      (heatmap_lat, heatmap_lng))
            s += ('];\n')
            s += ('\n')
            s += ('var pointArray = new google.maps.MVCArray(heatmap_points);' + '\n')
            s += ('var heatmap;' + '\n')
            s += ('heatmap = new google.maps.visualization.HeatmapLayer({' + '\n')
            s += ('\n')
            s += ('data: pointArray' + '\n')
            s += ('});' + '\n')
            s += ('heatmap.setMap(map);' + '\n')
            s += settings_string
        return s
