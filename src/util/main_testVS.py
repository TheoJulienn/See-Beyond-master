# -*- coding: utf-8 -*-
"""
Created on Wed May  9 17:37:18 2018

@author: Theo
"""
from Viewshed import Viewshed
from Viewshed import milieu


if __name__ == "__main__":
    pthimg = "IMG_780000_6440000_res=1_size=100.tif"
    milieu = milieu(pthimg)
    x = milieu[0] + 1
    y = milieu[1] + 1
    h_obs = 1.60
    rayon = 100
    nom_sortie = "test_"+ "(" + str(x) + str(y) + ")" + "_" + str(rayon) + "_" + str(h_obs)
    Viewshed(x,y,pthimg,h_obs,rayon,nom_sortie)
