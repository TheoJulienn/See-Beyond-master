# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 20:47:52 2018

@author: theoj
"""

import os
import algos as a
from display import displayWBimage
from skimage import io



if __name__ == "__main__":
    dir = os.path.dirname(__file__)
    #print(dir)
    pthimg = os.path.join(dir,"MNS/IMG_780000_6440000_res=1_size=100.tif")
    #print(pthimg)
    MNT = io.imread(pthimg)
    displayWBimage(MNT)
    h = 1.70
    res = 1
    dep = (58,69)
    arr = (12,6)
    dist_max = a.distance_max(h)
    visu_elevation = a.visu_elevation(dep,arr,MNT)
    limite = a.limite_visibilite(arr, dep, res, dist_max)
    print(a.intervisibilite(dep,arr,MNT,res,dist_max))
