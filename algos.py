# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 16:50:05 2018

@author: Théo
"""

import numpy as np
import math as m

def refraction(h):
    R = 1.02/(m.tan(h+(10.3/(h + 5.11))))
    return R

def distance_max(h, r = 6371*(10**3)):
    R = refraction(h)
    D = (m.sqrt(2*h*r + h*h))*(1-R/100)  
    return D

def bresenham(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
 
    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points


def limite_visibilite(arr, dep, res,d):
    d_px = m.sqrt((arr[0] - dep[0])**2 + (arr[1] - dep[1])**2)
    d_metre = d_px*res
    if d_metre < d:
        return True
    else:
        return False
    
def Elevation(dep,arr,MNT):
    visi = True
    liste = bresenham(dep, arr)
    elev = []
    for coord in liste:
        elev.append(MNT[coord])  
    maxi = np.amax(elev)      
    if (MNT[dep])!= maxi or (MNT[dep])<maxi :
        visi = False 
    return elev, maxi, visi
    