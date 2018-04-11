# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 20:47:52 2018



@author: theoj
"""
import math as m
import numpy as np
import os
import algos as a
import gdal
from display import displayWBimage
from skimage import io



if __name__ == "__main__":
    dir = os.path.dirname(__file__)
    print(dir)
    pthimg = os.path.join(dir,"MNS/IMG_780000_6440000_res=1_size=100.tif")
    print(pthimg)
    MNT = io.imread(pthimg)
    displayWBimage(MNT)
    h = 1.70
    res = 1
    dep = (2,98)
    arr = (4,55)
    d = a.distance_max(h)
    elevation = a.Elevation(dep,arr,MNT)
    limite = a.limite_visibilite(arr, dep, res,d)
    print(elevation, limite)