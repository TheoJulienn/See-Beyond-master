# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 15:57:46 2018

@author: theo
"""

from owslib.wms import WebMapService
from WMS import Request

wms = WebMapService('https://wxs.ign.fr/bxsq2vie25e3rlp5vjfwn27m/geoportail/r/wms', version='1.3.0')
def getInfo(wms = wms):

    print("\nINFO DU FLUX WMS : ", wms.identification.title,"\n")
    liste = list(wms.contents)
    print("Liste des couches servies\n" ,liste,"\n")
    for layer in liste :
        carte = layer
        print("Couche : " , carte,"\n")
        print("Emprise : " ,wms[carte].boundingBox,"\n")
        print("Opération possibles : ",[op.name for op in wms.operations],"\n")
        print("comment interroger le serveur : "  ,wms.getOperationByName('GetMap').methods,"\n")
        print("Formats : ", wms.getOperationByName('GetMap').formatOptions,"\n")
        print("-------------------------------------------------------")

def compute_Bbox(pt,footprint):

    #calcul de la bbox
    bbox = pt
    bbox += (int(pt[0]+footprint),)
    bbox += (int(pt[1]+footprint),)

    return bbox


def do_Request(pt,resolution,footprint,show = False) :


    #attributs de notre requête
    bbox = compute_Bbox(pt,footprint)
    size=(footprint/resolution, footprint/resolution)
    n_out = "IMG_" + str(pt[0]) + "_" + str(pt[1]) + "_" + "res=" + str(resolution) + "_" + "size=" + str(footprint)


    #test si la taille est trop grande pour la requête
    if(footprint/resolution >2048):
        print("La taille du raster ", str(size)," demandée en pixel est trop grande \n")
        return

    #requête
    req = Request(bbox,size,n_out)
    req.write_img()
    print(req)



