# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 20:47:52 2018



@author: theoj
"""
import os
import algos
import gdal
from display import displayWBimage
from skimage import io





if __name__ == "__main__":
    dir = os.path.dirname(__file__)
    print(dir)
    pthimg = os.path.join(dir,"MNS/IMG_786144_6446144_res=1_size=2048.tif")
    print(pthimg)
    Image = io.imread(pthimg)
    ds = gdal.Open('IMG_786144_6446144_res=1_size=2048.tif')
    displayWBimage(Image)


