# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 12:02:17 2018

@author: theo
"""
import os

from display import displayWBimage
from owslib.wms import WebMapService

class Request:

    def __init__(self, bbox, size, n_out):
        self.wms = WebMapService('https://wxs.ign.fr/bxsq2vie25e3rlp5vjfwn27m/geoportail/r/wms', version='1.3.0')
        self.layer = list(self.wms.contents)[1]
        self.crs = 'EPSG:2154'
        self.bbox = bbox
        self.size = size
        self.form = 'geotiff'
        self.n_out = n_out
        self.resolution = abs(self.bbox[0]-self.bbox[2])/self.size[0]


    def __str__(self):
        txt = "\n" + "Couche : " + self.layer + "\n" + "CRS : "+ self.crs[-4 :] + "\n" + "BBOX (xmin,ymin,xmax,ymax) : " + str(self.bbox) + "\n" + "Taille du raster (l,L) : " + str(self.size) + "\n" + "Resolution terrain (m) : " + str(self.resolution)  + "\n" + "Format de sortie : " + self.form + "\n"
        return txt

    def make_req(self):
        result = self.wms.getmap(layers=[self.layer],
                     srs=self.crs,
                     bbox=self.bbox,
                     size=self.size,
                     format= 'image/'+ self.form,
                     transparent=True)
        return result

    def write_img(self):
        dir = os.path.dirname(__file__)
        pthimg = os.path.join(dir,"MNS")
        image = open(pthimg + "/" +self.n_out+ "."+"tif", 'wb')
        image.write(self.make_req().read())
        image.close()












