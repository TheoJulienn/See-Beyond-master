# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 20:47:52 2018



@author: theoj
"""

from request_functions import do_Request,getInfo


if __name__ == "__main__":


    #point initial
    liste_pt = []
    pt = (780000,6440000)
    print("\n------------------------------\n")


    # limite de la zone du flux lim = (704997.25, 6403997.75, 819002.25, 6483002.75)

    #resolution choisie
    resolution = 1
    #coté de la tuile sur le terrain (m)
    footprint = 100
    #creation de liste de point
    for i in range(10):
        liste_pt.append( (pt[0] + i *footprint , pt[1] + i * footprint) )

    getInfo()
    for pt in liste_pt:
        do_Request(pt,resolution,footprint)


