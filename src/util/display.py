# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 12:20:19 2018

@author: Théo
"""
import numpy as np
import matplotlib.pyplot as plt


def displayRGBimage(Image):
    I_out=np.uint8(Image)
    plt.axis("off")
    imgplot=plt.imshow(I_out)
    plt.show(imgplot)


def displayWBimage(Image):
    I_out=np.uint8(Image)
    plt.figure()
    imgplot=plt.imshow(I_out)
    imgplot.set_cmap('gray')
    plt.axis("off")
    plt.show(imgplot)

