# -*- coding: utf-8 -*-
"""
Created on Wed May  9 10:30:11 2018

@author: Theo
"""

import numpy
import gdal




def Viewshed (x_geog,y_geog, rast, z_obs, radius, output):


    """
    Applique l'algorithme de viewshed sur un raster en entrée à partir d'un point d'observation
    Produit un raster, la valeur 1 correspondant au visible depuis le point d'observation et 0 sinon
    :param x_geog: float coordonnée x géographique du point d'observation
    :param y_geog: float coordonnée y géographique du point d'observation
    :param rast: string chemin relatif du MNT/MNS en raster
    :param z_obs: float hauteur au dessus du sol du point d'observation
    :param radius: int rayon en mètres pour le viewshed autout du point d'observation
    :param output: string chaine de caractère spécifiant le nom du raster produit par le viewshed
    :return booléen: True en cas de succès
    """

    #supprime un message d'erreur négligeable
    numpy.seterr(divide='ignore', invalid='ignore')
    #on recupère le raster avec gdal
    gdal_raster=gdal.Open(rast)


    #récupération des  paramètres de transformation géographiques tels que : (Xp,Yp) coordonnées pixels
        #Xp = padfTransform[0] + P*padfTransform[1] + L*padfTransform[2];
        #Yp = padfTransform[3] + P*padfTransform[4] + L*padfTransform[5];

    gt=gdal_raster.GetGeoTransform()
    projection= gdal_raster.GetProjection() #recupération de la projection du raster
    global pix; pix=gt[1] #taille du pixel sur le terrain

    #taille du raster en pixels
    raster_y_size = gdal_raster.RasterYSize
    raster_x_size = gdal_raster.RasterXSize
    #bornes du raster en coordonnées terrain
    global raster_x_min; raster_x_min = gt[0]
    global raster_y_max; raster_y_max = gt[3]


    # rayon en pixel
    radius_pix = int(radius/pix)

    #taille de la fenetre contenant le cercle formé par le point et le rayon en pixel
    fenetre_travail = radius_pix *2 + 1

    #initialisation de la matrice qui va contenir les resultats de viewshed
    mx_vis = numpy.zeros((fenetre_travail, fenetre_travail))


    temp_x= ((numpy.arange(fenetre_travail) - radius_pix) * pix) **2
    temp_y= ((numpy.arange(fenetre_travail) - radius_pix) * pix) **2

    #matrice de distances par rapport au centre de la matrice, l'element dans chaque cellule correspond a la distance en metres au centre de la matrice
    mx_dist = numpy.sqrt(temp_x[:,None] + temp_y[None,:])

    #matrice qui va définir le cercle de recherche : False en dehors du cercle, True à l'intérieur
    mask_circ = mx_dist [:] > radius



    #initialisation de la matrice finale (qui va ensuite etre convertie en raster)
    matrix_final = numpy.zeros ((gdal_raster.RasterYSize, gdal_raster.RasterXSize) )

    #index matrice
    t = line_of_sight(radius_pix)

    #Matrices pour l'algorithme de viewshed
    mx_err = t[:,:, 2]
    mx_err_dir = numpy.where(mx_err > 0, 1, -1); mx_err_dir[mx_err == 0]=0
    mask = t[: ,: , 3]==1
    x0=y0=radius_pix
    mx_x = t[:, : , 1].astype(int)
    mx_y = t[: ,:, 0].astype(int)
    mx_y_err = mx_y + mx_err_dir
    mx_x_rev = numpy.subtract ( mx_x, (mx_x - x0) *2 , dtype=int )
    mx_y_rev = numpy.subtract ( mx_y , (mx_y - y0) *2, dtype = int)
    mx_y_err_rev = mx_y_rev + mx_err_dir *-1
    mx_x_steep = x0 + (mx_y - y0)
    mx_y_steep = y0 + (mx_x - x0)
    mx_x_err_steep = x0 + (mx_y_err - y0)
    mx_x_rev_steep = x0 + (mx_y_rev - y0)
    mx_y_rev_steep = y0 + (mx_x_rev - x0)
    mx_x_err_rev_steep = x0 + (mx_y_err_rev - y0)

    #On regarde si le point est bien dans le raster
    if if_in((x_geog,y_geog),rast):

        #coordonnées du point en pixel dans le raster
        x = int((x_geog - raster_x_min) / pix)
        y = int((raster_y_max - y_geog) / pix)

    else:
        return False

    #intialisation de z
    z = 0

    if x <= radius_pix:
        x_offset =0
        x_offset_dist_mx = radius_pix - x
    else:
        x_offset = x - radius_pix
        x_offset_dist_mx= 0

    x_offset2 = min(x + radius_pix +1, raster_x_size)

    if y <= radius_pix:
        y_offset =0
        y_offset_dist_mx= radius_pix - y
    else:
        y_offset = y - radius_pix
        y_offset_dist_mx= 0

    y_offset2 = min(y + radius_pix + 1, raster_y_size )

    window_size_y = y_offset2 - y_offset
    window_size_x = x_offset2 - x_offset

    data = numpy.zeros((fenetre_travail, fenetre_travail))

    #matrice de la taille de la fenetre de travail contenant les altitudes provenant du mnt
    data[ y_offset_dist_mx : y_offset_dist_mx +  window_size_y,
          x_offset_dist_mx : x_offset_dist_mx + window_size_x] = gdal_raster.ReadAsArray(
              x_offset, y_offset, window_size_x, window_size_y).astype(float)


    z = data [radius_pix,radius_pix] + z_obs #hauteurs selon l'observateur

    data -= z # Hauteur selon l'observateur

    data /= mx_dist #(data -z - mxcurv) /mx_dist

   ################ viewshed ################

   #basé sur l'algorithme de Zoran Cuckovic

    for steep in [False, True]:
        for rev_x in [True, False]:
            mx = mx_x_rev if rev_x else mx_x
            for rev_y in [True, False]:
                my = mx_y_rev if rev_y else mx_y
                me =mx_y_err_rev if rev_y else  mx_y_err
                if  steep:
                    mx = mx_x_rev_steep if rev_x else mx_x_steep
                    my= mx_y_rev_steep if rev_y  else mx_y_steep
                    me= mx_x_err_rev_steep if rev_x  else  mx_x_err_steep
                if steep:
                    interp = data[mx,my] + (data[me, my]-data[mx,my] ) * numpy.absolute(mx_err)
                else:
                    interp = data[mx,my] + (data[mx, me] -data[mx,my] ) * numpy.absolute(mx_err)
                test_val = numpy.maximum.accumulate(interp, axis=1)
                v = interp >= test_val
                mx_vis [mx[mask], my[mask]]=v[mask]

        #Matrice contenant les résultat : on place la valeur 1 dans les cellules qui sont "visibles"
        mx_vis [radius_pix,radius_pix]=1
        matrix_vis = mx_vis

        #les cellules se situant en dehors du mask sont nulles
        matrix_vis [mask_circ] = 0

        matrix_final [ y_offset : y_offset + window_size_y,
                       x_offset : x_offset + window_size_x ] += matrix_vis [
                           y_offset_dist_mx : y_offset_dist_mx +  window_size_y,
                            x_offset_dist_mx : x_offset_dist_mx + window_size_x]

        #certaines valeurs sont au dessus de 1 donc on rectifie
        for i in range(matrix_final.shape[0]):
            for j in range(matrix_final.shape[1]):
                if(matrix_final[i,j]>1):
                    matrix_final[i,j]=1


        ####  ecriture du fichier de sortie ####

    success = write_raster (matrix_final, output,gdal_raster.RasterXSize, gdal_raster.RasterYSize, gt, projection)
    if success : return True
    else: return False







def line_of_sight(rayon):

    """
    Fonction permettant de créer des lignes de vues qui vont être réutilisée pour les calcules de viewshed.
    Chaque ligne partant du point d'observation possède son point d'arrivée et les pixels par lesquelles elle passe.
    On peut utiliser 1/8ème du rayon, le reste peut etre copié.
    basé sur l'algorithme de Zoran Cuckovic
    :param rayon: int rayon maximum de vue autour du point d'observation
    :return mx_index: numpy.array matrice d'indices de pixels correspondant aux lignes de vues
    """


    rayon_largeur = rayon #largeur du rayon de balayage

    mx_index= numpy.zeros((rayon_largeur +1 , rayon, 4))
    min_err = {}

    j=0

    for m in range(0,rayon_largeur+1):
        x_f, y_f = rayon, rayon #x0,y0
        #dy = x; dx = y
        dy,dx= m, rayon_largeur
        D=0
        for i in range(0,rayon):
            x_f += 1
            if 2* (D + dy) < dx:
                D += dy
            else:
                y_f += 1
                D += dy - dx
            yx= (y_f,x_f)
            mx_index[j,i,0:2]=yx

            if D: e=D/dx; err=abs(e)
            else: e, err = 0,0
            mx_index[j,i,2]=e
            try:
                err_old = min_err[yx][0]
                if err < err_old: min_err[yx]=[err,j,i]
            except:
                min_err[yx]=[err,j,i]

        j+=1

    for key in min_err:
        ix=min_err[key][1:3]
        mx_index[ix[0], ix[1]][3]= 1

    return mx_index



def write_raster (matrix, file_name,columns_no, rows_no,
                  geotransform_data, GDAL_projection_data):

    """
    Transforme une matrice en raster et l'écrit à l'emplacement du script
    :param matrix: numpy.array matrice à convertir en raster
    :param file_name: string nom du raster à écrire
    :param columns_no: int nombre de colonnes du raster à écrire
    :param rows_no: int nombre de lignes du raster à écrire
    :param geotransform_data: tableau correspondant aux paramètres de transformation géographiques
    :param GDAL_projection_data: string chaine de caractère spécifiant les details de la projection
    :return nothing:
    """

    driver = gdal.GetDriverByName( 'GTiff' )
    dst_ds = driver.Create( file_name+'.tiff', columns_no, rows_no, 1, gdal.GDT_Float32)

    dst_ds.SetProjection(GDAL_projection_data)
    dst_ds.SetGeoTransform(geotransform_data)

    dst_ds.GetRasterBand(1).Fill(numpy.nan)
    dst_ds.GetRasterBand(1).SetNoDataValue(numpy.nan)

    dst_ds.GetRasterBand(1).WriteArray(matrix,0,0)

    dst_ds=None

    return file_name +'.tiff'


def if_in(point,raster):
    """
    Controle si le point est dans l'emprise du raster
    :param point: tuple correspondant aux coordonnées du point
    :param raster: string chemin relatif du raster
    :return boolean: succès de l'opération
    """
    x_geog = point[0]
    y_geog = point[1]
    gdal_raster=gdal.Open(raster)
    gt=gdal_raster.GetGeoTransform()
    global pix; pix=gt[1]
    global raster_x_min; raster_x_min = gt[0]
    global raster_y_max; raster_y_max = gt[3]
    raster_y_size = gdal_raster.RasterYSize
    raster_x_size = gdal_raster.RasterXSize
    raster_y_min = raster_y_max - raster_y_size * pix
    raster_x_max = raster_x_min + raster_x_size * pix
    if raster_x_min <= x_geog <= raster_x_max and raster_y_min <= y_geog <= raster_y_max:
        return True
    else: return False

def milieu(raster):
    """
    (FONCTION POUR TEST)
    Renvoie les coordonnées du milieu d'un raster
    :param raster: string chemin relatif du raster
    :return point: tuple coordonnées du milieu
    """
    src = gdal.Open(raster)
    ulx, xres, xskew, uly, yskew, yres  = src.GetGeoTransform()
    lrx = ulx + (src.RasterXSize * xres)
    lry = uly + (src.RasterYSize * yres)
    bound = numpy.array([[ulx,uly],[lrx,lry]])
    milieu = ((bound[0][0]+bound[1][0])/2,(bound[0][1]+bound[1][1])/2)

    return milieu


