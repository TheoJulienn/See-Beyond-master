# -*- coding: utf-8 -*-

"""
Created on Wed Feb 28 16:50:05 2018
Intervisibilité
@author: Camélia
"""


import numpy as np
import math as  m

"""
/****************************************************************************************
    Fonctions permettant de définir les différents paramètres utiles à l'intervisibilité

*****************************************************************************************/
"""

def refraction(h):
    """
    Calcul le coefficient de réfraction atmosphérique
    :param h: hauteur d'observation 
    :return integer: valeur de réfraction atmosphérique (radian)
    
    >>> h = 1.70
    R = 14.364583661789922  
    """
    R = 1.02/(m.tan(h+(10.3/(h + 5.11))))
    return R

def distance_max(h, r = 6371*(10**3)):
    """
    Calcul distance maximale de vision horizontale
    :param h: hauteur d'observation
    :param r: rayon terretre
    :return integer: distance maximale de vision (mètres)
    
    >>>h = 1.70
    >>>refraction(h) = 14.36458
    dist_max = 3985.6274705304218    
    """
    R = refraction(h)
    dist_max = (m.sqrt(2*h*r + h*h))*(1-R/100)  
    return dist_max


def limite_visibilite(arr, dep, res, dist_max):
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
    
def visu_elevation(dep,arr,MNT):
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
    liste = bresenham(dep, arr)
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
    Fonctions permettant de calculer un algorithme de lecture des différents pixels du MNT

*******************************************************************************************/

"""
def bresenham(start, end):
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

def intervisibilite(dep,arr,MNT,res,dist_max):
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
    if limite_visibilite(arr, dep, res, dist_max):
        # Si la distance max de vision est respectée alors on regarde l'élévation des points
        if visu_elevation(dep,arr,MNT):
            return True
        else:
            return False
    else:
        return False