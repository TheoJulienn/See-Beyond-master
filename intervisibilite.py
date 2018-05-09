# -*- coding: utf-8 -*-

"""
Created on Wed Feb 28 16:50:05 2018
Intervisibilité
@author: Camélia
"""

import numpy as np
import math as  m
from display import displayWBimage
import gdal 

"""
/****************************************************************************************
    Fonctions permettant de définir les différents paramètres utiles à l'intervisibilité

*****************************************************************************************/
"""

def Refraction(h):
    """
    Calcul le coefficient de réfraction atmosphérique
    :param h: hauteur d'observation 
    :return integer: valeur de réfraction atmosphérique (radian)
    
    >>> h = 1.70
    R = 14.364583661789922  
    """
    R = 1.02/(m.tan(h+(10.3/(h + 5.11))))
    return R

def Distance_max(h, r = 6371*(10**3)):
    """
    Calcul distance maximale de vision horizontale
    :param h: hauteur d'observation
    :param r: rayon terretre
    :return integer: distance maximale de vision (mètres)
    
    >>>h = 1.70
    >>>refraction(h) = 14.36458
    dist_max = 3985.6274705304218    
    """
    R = Refraction(h)
    dist_max = (m.sqrt(2*h*r + h*h))*(1-R/100)  
    return dist_max


def Limite_visibilite(arr, dep, res, dist_max):
    """
    Determine si la distance entre deux points du MNT respecte la distance maximale de vision
    :param arr: point observé
    :param dep: point d'observation
    
    :return boolean: True si la distance est plus petite que la distance maximale de vision,
                     False sinon.
    
    >>> arr = (58,10)
    >>> dep = (1,58)
    >>> dist_max = 3985
    True
     
    """
    d_px = m.sqrt((arr[0] - dep[0])**2 + (arr[1] - dep[1])**2)
    d_metre = d_px*res
    if d_metre < dist_max:
        return True
    else:
        return False
    
def Visu_elevation(dep,arr,MNT):
    """
    Détermine si deux points sont visibles en fonction de leur élévation
    :param arr: point observé
    :param dep: point d'observation
    :return boolean: True si le point observé n'est pas caché par un autre point qui aurait une élévation plus grande
                     False sinon
    
    >>> dep = (1,58)
    >>> arr = (58,10)
    >>> MNT = MNT.tif
    False
    
    >>> dep = (58,69)
    >>> arr = (12,6)
    >>> MNT = MNT.tif
    True
    """
    vis = True
    liste = Bresenham(dep, arr)
    elev = []
    for coord in liste:
        elev.append(MNT[coord])  
    maxi = np.amax(elev)      
    if (MNT[dep])!= maxi or (MNT[dep])<maxi :
        if (MNT[arr])!= maxi or (MNT[arr])<maxi:
            vis = False 
    return  vis


"""
/******************************************************************************************
    Fonctions permettant de calculer selon un algorithme de lecture des différents pixels du MNT

*******************************************************************************************/

"""
def Bresenham(start, end):
    """
    Bresenham's Line Algorithm
    :param start: point de départ
    :param end: point d'arrivée
    :return: liste de tuples présents entre ces deux points (liste)
    
    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Initialisation des paramètres de base
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine comment est définie la pente
    is_steep = abs(dy) > abs(dx)
 
    # Inversion de la ligne
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    # Echange du début et de la fin si nécessaire, et conserver la valeur final
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalcul des différentiels
    dx = x2 - x1
    dy = y2 - y1
 
    # Calcul des erreurs
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Réitérez sur la limitation de la boîte produisant des points entre le début et la fin
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Inverser la liste si les coordonnées ont été changées
    if swapped:
        points.reverse()
    return points

"""
/******************************************************************************************
    Fonction d'intervisibilité entre deux points

*******************************************************************************************/
"""

def Intervisu(dep,arr,MNT,res,dist_max):
    """
    Détermine l'intervisibilité entre deux points à partir des paramètres calculés précédement
    :param dep: point de départ, d'observation
    :param arr: point d'arrivée, observé
    :param MNT: MNT, zone à étudier
    :param res: résolution du MNT
    :param dist_max: distance maximale d'observation
    :return boolean: True si l'intervisibilité est possible
                     False sinon
                     
    >>> dep = (58,69)
    >>> arr = (12,6)
    >>> MNT = MNT.tif
    >>> res = 1
    >>> dist_max = 3958
    True
    
    >>> dep = (1,58)
    >>> arr = (58,10)
    >>> MNT = MNT.tif
    >>> res = 1
    >>> dist_max = 3958
    False
    """
    if Limite_visibilite(arr, dep, res, dist_max):
        # Si la distance max de vision est respectée alors on regarde l'élévation des points
        if Visu_elevation(dep,arr,MNT):
            return True
        else:
            return False
    else:
        return False
    
    
"""
/*********************************************************************************************************
    Fonctions d'intervisibilité entre un point d'obervation et tous les points de la ligne d'observation

*********************************************************************************************************/
"""

def Points_visu(dep):
    """
    Détermine tous les points situés à une certaines distances du point d'observation
    :param i_view: distance maximale de vision autour du point d'observation
    :param dep: point d'observation
    :return tuple: un tuple contenant les deux coordonnées x, y des points situés sur le cercle entourant le point d'observation
    
    >>> dep = (12,35)
    ([32, 31, 31...31, 31],[[55, 54,..., 54, 54, 54])
    
    """
    x0 = dep[0]
    y0 = dep[1]
    x = []
    y = []
    for t in np.arange(0, 2*m.pi, 0.01):
        x.append(m.floor(x0+20*m.cos(t)))
        y.append(m.floor(y0+20*m.cos(t)))
    return x,y

def Pix2coord(x, y, pthimg):
    """
    Transforme les coordonnées pixel d'entrée du point en coordonnées terrain
    :param x: coordonnée x du point d'observation
    :param y: coordonnée y du point d'observation
    :param  pthimg: MNT, zone à analyser
    :return tuple: un tuple contenant les deux coordonnées x, y du point en coordonnée terrain
    
    >>> dep = (75,62)
    (780075.0, 6440038.0)
    """
    
    mnt_gdal= gdal.Open(pthimg)
    #Tranformation des coordonnees selon différents paramètre
    xoff, a, b, yoff, d, e = mnt_gdal.GetGeoTransform() 
    xp = a * x + b * y + xoff
    yp = d * x + e * y + yoff
    return xp, yp



def Ligne_intervisibilite(MNT, dep, dist_max ,x0, y0, res):
    """
    Création d'une matrice inscrite dans un MNT permettant de visualiser les zones d'inter-visibilité
    :param MNT: MNT, zone à analyser
    :param dep: coordonnées (x,y) du point d'observation
    :param  dist_max: distance maximale de visibilité 
    :param i_view: distance entre le point d'observation et le point d'arrivée
    :param x0: coordonnées x des points situés à une distance donné du point d'observation
    :param y0: coordonnées y des points situés à une distance donné du point d'observation
    :param res: 
    :return image: une image contenant la ligne d'intervisibilité

    """
    x, y = dep
    mat = np.array(MNT)
    vis = []
    for i in range (len(x0)):
        #Intervisibilite entre un point et tous les autres points possiblement visible
        vis.append(Intervisu(dep,(x0[i],y0[i]),MNT,res,dist_max))
        #Calcul des distances entre le point initial et le point final
        i_view = (m.sqrt((x0[i]-dep[0])**2 + (y0[i]-dep[1])**2))
    for j in range(len(x0)):
        if i_view < dist_max:
            if x0[j] <100 and x0[j] >0:
                if y0[j] <100 and y0[j] >0:
                    #On vérifie l'intervisibilité entre le point de départ et tous les points situé à une certaine distance
                    if Intervisu(dep,(x0[j],y0[j]),MNT,res,dist_max):
                        xl = [x, x0[j]]
                        yl = [y, y0[j]]
                        #On associe la zone visible à une valeur de 1 dans la matrice d'intervisibilité
                        mat[xl, yl] = 1                   
                    else:
                        xl = [x, x0[j]]
                        yl = [y, y0[j]]
                        #On associe la zone visible à une valeur de 0 dans la matrice d'intervisibilité
                        mat[x, y] = 0         
    #Affiche l'image
    displayWBimage(mat)
    
    return vis 