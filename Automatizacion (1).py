# -*- coding: utf-8 -*-

##Valentina Cordoba Rojas
##Codigo 1531820
##Nota: Codigo para imagenes landsat 8
##IMPORTA LIBRERIAS NECESARIAS
import numpy as np, os, gdal, glob, math


##DEFINICION DE FUNCIONES
##1. FUNCION PARA LEER METADATO
def metadato (archivo):
    metadatos={}                            #Diccionario vacío 
    for i in archivo.readlines():           #iterar el archivo 
        if "=" in i:                        #si la línea tiene un '='
            separador = i.split("=")        #cortamos la línea en el ' = '
            clave=separador[0].strip()      #asignamos el primer elemento como clave
            valor=separador[1].strip()      #asignamos el segundo elemento como valor
            metadatos[clave]=valor          #llenamos el diccionario con clave y valor
    archivo.close()
    return metadatos
            
##2. FUNCION PARA GUARDAR COMO TIFF
def guardar_tif(salida,matriz,im_entrada,x_in=0,y_in=0):
    #Define coordenadas iniciales
    geoTs=im_entrada.GetGeoTransform()      #parametros
    driver=gdal.GetDriverByName("GTiff")
    prj=im_entrada.GetProjection()          #Proyeccion de la imagen de entrada     
    cols=matriz.shape[1]                    #Filas 
    filas=matriz.shape[0]                   #Columnas            
    ulx=geoTs[0]+x_in*geoTs[1]
    uly=geoTs[3]+y_in*geoTs[5]
    geoTs=(ulx,geoTs[1],geoTs[2],uly,geoTs[4],geoTs[5])
    #Crear el archivo con los datos de entrada
    export=driver.Create(salida,cols,filas,1,gdal.GDT_Float32)
    banda=export.GetRasterBand(1)
    banda.WriteArray(matriz)
    export.SetGeoTransform(geoTs)
    export.SetProjection(prj)
    banda.FlushCache()
    export.FlushCache()
    
##3.FUNCION PARA CREAR CARPETA SI NO EXISTE
def create_folder(path):
    if not os.path.exists(path):
            os.mkdir(path)
##4. FUNCIONES PARA EL PROCESAMIENTO
##FUNCION REFLECTANCIA CON CORRECCION POR ANGULO SOLAR
def reflectancia (M,ND,A,sun_elevation):
    reflec=(M*ND+A)/np.sin(sun_elevation)
    return(reflec)

##CORRECCION ATMOSFERIA POR HISTOGRAMA
def refle_corregida(r):
    correccion= r-np.nanmin(r)
    return(correccion)
##CALCULO INDICADORES DE VEGETACION
def rvi(RED, NIR):
    rvi= RED/NIR
    return (rvi)    
    
def ndvi(RED,NIR):
    ndvi=(NIR-RED)/(NIR+RED)
    return(ndvi)
    
def pvi(RED,NIR,b,a):
    pvi=(NIR-RED-b)/(math.sqrt(a**2 +1))
    return(pvi)
 
def savi(RED,NIR,L):
    savi= (1 + L)*(NIR-RED)/(NIR+RED+ L)
    return(savi)
    
def arvi(BLUE,RED,NIR):
    arvi2=(NIR-(2*RED)+BLUE)/(NIR+(2*RED)+BLUE)
    return(arvi2)

def gemi(RED,NIR):
    n=(2*(NIR**2 -RED**2)+1.5*NIR+0.5*RED)/(NIR+RED+0.5)
    gemi=(n*(1-0.25*n)-(RED-0.125))/(1-RED)
    return(gemi)

def msavi(RED,NIR):
    msavi=(2*NIR+1-math.sqrt((2*NIR+1)**2 -8*(NIR-RED)))/(2)
    return(msavi)

def gari(BLUE,GREEN,RED,NIR):
    gari2=(NIR-(GREEN-(BLUE-RED)))/(NIR-(GREEN+(BLUE-RED)))
    return(gari2)

def evi(BLUE,RED,NIR):
    evi= 2.5*(NIR-RED)/(NIR+ 6*RED- 7.5* BLUE+ 1)
    return(evi)
    
def gndvi(GREEN,NIR):
    gndvi=(NIR-GREEN)/(NIR+GREEN)
    return(gndvi)

def dvi(RED,NIR):
    dvi=NIR-RED
    return(dvi)

def tvi(RED,NIR):
    tvi=math.sqrt((NIR-RED)/(NIR+RED))+0.5
    return(tvi)

def ndwi(NIR,SWIR):
    ndwi=(NIR-SWIR)/(NIR+SWIR)
    return(ndwi)


##CALCULO INDICADOR DE TEMPERATURA
def temperatura(rad,bt,ndvi):
    f_veg=np.sqrt((ndvi-np.nanmin(ndvi))/(np.nanmax(ndvi)-np.nanmin(ndvi)))
    emisividad = 0.985*f_veg +0.96*(1-f_veg)
    LST= (bt/(1+(0.00115* bt/1.4394744927)*np.log(emisividad)))- 273   
    return(LST)
    

##DEFINICION DE VARIABLES
archivo_mtl= r"d:\Desktop\Universidad\Teledeteccion\PROCESAMIENTO\IMAGENES\LC08_L1TP_009058_20140820_20170420_01_T1_MTL.txt" #Cambiar ruta a la carpeta que tenga el metadato
ruta_mtl=open(archivo_mtl,"r")
datos=metadato(ruta_mtl)
path_img= r"d:\Desktop\Universidad\Teledeteccion\PROCESAMIENTO\IMAGENES"    #Cambiar ruta a la carpeta que contenga las imagenes
imagen= "LC08_L1TP_009058_20140820_20170420_01_T1"   #Nombre de la imagen sin el número de banda porque leeran cada una
resultados= r"d:\Desktop\Universidad\Teledeteccion\PROYECTO\resultados" ##Cambiar a ruta donde se desee guardar los resultados
create_folder(resultados)

##SCRIPT
reflectancias= []

for banda in range (1,7):
    print ("Inicia procesamiento de: "+imagen+"_B"+str(banda)+".TIF")
    img_banda=gdal.Open(path_img+os.sep+imagen+"_B"+str(banda)+".TIF")
    nd=img_banda.ReadAsArray().astype('float')
    nd [[nd==0]] = np.nan
    if (banda==2 or banda==3 or banda==4 or banda==5 or banda==6):
        #Reflectancia
        m=float(datos['REFLECTANCE_MULT_BAND_'+str(banda)])
        a=float(datos['REFLECTANCE_ADD_BAND_'+str(banda)])
        sun_el = float(datos['SUN_ELEVATION'])
        reflec=reflectancia(m,nd,a,sun_el)
        #Refelctancia corregida
        reflectancia_cor= refle_corregida(reflec)
        reflectancias.append(reflectancia_cor)
        out_file = resultados + os.sep+'reflectancia_cor_B'+str(banda)+'.tif'
        guardar_tif(out_file,reflectancia_cor,img_banda,x_in=0,y_in=0)
        print ("HECHO")


##APLICACION DE FUNCIONES
calculo_rvi_l8=rvi(reflectancias[2],reflectancias[3])
salida_rvi=(resultados+os.sep+'l8_rvi.TIF')
guardar_tif(salida_rvi,calculo_rvi_l8,img_banda)

calculo_ndvi_l8=ndvi(reflectancias[2],reflectancias[3])
salida_ndvi=(resultados+os.sep+'l8_ndvi.TIF')
guardar_tif(salida_ndvi,calculo_ndvi_l8,img_banda)

calculo_pvi_l8=(reflectancias[2],reflectancias[3])
salida_pvi=(resultados+os.sep+'l8_pvi.TIF')
guardar_tif(salida_pvi,calculo_pvi_l8,img_banda)

calculo_savi_l8=savi(reflectancias[2], reflectancias[3],0.5)
salida_savi=(resultados+os.sep+'l8_savi.TIF')
guardar_tif(salida_savi,calculo_savi_l8,img_banda)

calculo_arvi_l8=arvi(reflectancias[0],reflectancias[2],reflectancias[3])
salida_arvi=(resultados+os.sep+'l8_arvi.TIF')
guardar_tif(salida_arvi,calculo_arvi_l8,img_banda)

calculo_gemi_l8=gemi(reflectancias[2],reflectancias[3])
salida_gemi=(resultados+os.sep+'l8_gemi.TIF')
guardar_tif(salida_gemi,calculo_gemi_l8,img_banda)

calculo_msavi_l8=msavi(reflectancias[2],reflectancias[3])
salida_msavi=(resultados+os.sep+'l8_msavi.TIF')
guardar_tif(salida_msavi,calculo_msavi_l8,img_banda)

calculo_gari_l8=gari(reflectancias[0],reflectancias[1],reflectancias[2],reflectancias[3])
salida_gari=(resultados+os.sep+'l8_gari.TIF')
guardar_tif(salida_gari,calculo_gari_l8,img_banda)

calculo_evi_l8=evi(reflectancias[0],reflectancias[1],reflectancias[2])
salida_evi=(resultados+os.sep+'l8_evi.TIF')
guardar_tif(salida_evi,calculo_evi_l8,img_banda)

calculo_gndvi_l8=gndvi(reflectancias[1],reflectancias[3])
salida_gndvi=(resultados+os.sep+'l8_gndvi.TIF')
guardar_tif(salida_gndvi,calculo_gndvi_l8,img_banda)

calculo_dvi_l8=dvi(reflectancias[2],reflectancias[3])
salida_dvi=(resultados+os.sep+'l8_dvi.TIF')
guardar_tif(salida_dvi,calculo_dvi_l8,img_banda)

calculo_tvi_l8=tvi(reflectancias[2],reflectancias[3])
salida_tvi=(resultados+os.sep+'l8_tvi.TIF')
guardar_tif(salida_tvi,calculo_tvi_l8,img_banda)

calculo_ndwi_l8=ndwi(reflectancias[3],reflectancias[4])
salida_ndwi=(resultados+os.sep+'l8_ndwi.TIF')
guardar_tif(salida_ndwi,calculo_ndwi_l8,img_banda)


 ##RECORTAR CON SHAPE
mask= r"d:\Desktop\Universidad\Teledeteccion\PROCESAMIENTO\shp\Recorte.shp" ##Cambiar a ruta donde este el shape de recorte - ruta que no contenga espacios
path_img_recortar=r"d:\Desktop\Universidad\Teledeteccion\PROYECTO\resultados" ##Cambiar a ruta que contenga las imagenes tif a recortar
salida_recorte=r"d:\Desktop\Universidad\Teledeteccion\PROYECTO\resultados\corte" ##Cambiar a ruta donde se desee guardar los recortes
create_folder(salida_recorte)
rasters=glob.glob(path_img_recortar+os.sep+"*.tif")  ##Devuelve una lista de todos los tif en la carpeta
 
for raster in rasters:
    print("archivo a recortar: "+raster)
    corte=salida_recorte+os.sep+os.path.basename(raster)
    vp="gdalwarp -dstnodata 0.0 -q -cutline %s -crop_to_cutline -of GTiff %s %s"%(mask,raster,corte)
    os.system("gdalwarp -dstnodata 0.0 -q -cutline %s -crop_to_cutline -of GTiff %s %s"%(mask,raster,corte))
    
    
    