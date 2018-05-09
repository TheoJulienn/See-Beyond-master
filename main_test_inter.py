# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 20:47:52 2018

@author: theoj
"""


import os
import intervisibilite as a
from skimage import io
import math as m
from display import displayWBimage

#from request_functions import do_Request,getInfo



if __name__ == "__main__":
    #Informations sur le MNT
    dir = os.path.dirname(__file__)
    #print(dir)
    pthimg = os.path.join(dir,"MNS/IMG_780000_6440000_res=1_size=100.tif")
    #print(pthimg)
    MNT = io.imread(pthimg)
    #Afficher le MNT
    displayWBimage(MNT)
    #print(MNT)
    
    #Paramètres utiles
    h = 1.70
    res = 1
    dep = (68,72)
    arr =(12,58)
    vis = []
    dist_max = a.distance_max(h)
    x0 = a.Points_visu(dep)[0]
    y0 = a.Points_visu(dep)[1]
    pix2coord = a.pix2coord(dep[0], dep[1], pthimg) 
    #print(pix2coord)
    
    #Fonction renvoyant un booleen selon l'intervisibilite entre deux points
    inter = a.intervisu(dep,arr,MNT,res,dist_max)
    #print(inter)
    for i in range (len(x0)):
        #Intervisibilite entre un point et tous les autres points possiblement visible
        vis.append(a.intervisu(dep,(x0[i],y0[i]),MNT,res,dist_max))
        #print(vis)
        #Calcul des distances entre le point initial et le point final
        i_view = (m.sqrt((x0[i]-dep[0])**2 + (y0[i]-dep[1])**2))
    
    if i_view < dist_max:
        #On vérifie que le point final est bien inférieur à la distance max de vision
        c = a.Ligne_intervisibilite(MNT, dep, dist_max, i_view, x0, y0, res)
        
    