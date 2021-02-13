# -*- coding: utf-8 -*-
"""
Created on Sat May 16 17:42:36 2020

@author: Usuario
"""

import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import sys
import os
import numpy as np, os, gdal, glob, math
import math


root=Tk()
root.geometry("650x680")
root.iconbitmap("icono.ico")
root.title("VIs Córdoba & Urbano")


miFrame = Frame(root)
miFrame.grid(row=0, column=0, padx=15,pady=5)

miFramevi0 = Frame(root) #titulo indices
miFramevi0.grid(row=8, column=0,  padx=15,pady=10) 

miFramevi = Frame(root)#indices izquierda
miFramevi.grid(row=9, column=0)

miFramevisavi = Frame(root)#frame para savi
miFramevisavi.grid(row=10, column=0,  padx=15,pady=20)

miFramevipvi = Frame(root)#frame para pvi
miFramevipvi.grid(row=16, column=0,  padx=15,pady=20)

def infoAdicional ():
    messagebox.showinfo("VIs Córdoba & Urbano", "Procesador de imáganes Landsat 8 versión 2020")
    
         
def avisoLicencia():
    messagebox.showwarning("Licencia", "Producto bajo licencia genérica")
    
    
def guia():
      def abrir():
          messagebox.showinfo("Guía", "Desarrollado por:\n\n Valentina Córdoba Rojas\n Cristian David Urbano Rojas")          
      global dos
      dos=Toplevel()
      bit=dos.iconbitmap("icono.ico") 
      dos.geometry("200x650")
      dos.title("Guía de Usuario")
      dos.wm_attributes("-alpha", 0.9)
      dos.configure(bg="gray")
      dos.minsize(500,300)
      dos.resizable(0,0)
      
      imagen=PhotoImage(file="icono.png")
      botonimagen=Button(dos, image=imagen, command=abrir, bg="gray")
      titulo=Label(dos, bg="gray22", fg="white", font=("Terminal bold",8), 
                    text="VIs Córdoba & Urbano")
      
      instrucciones=Label(dos, bg="gray22", fg="white", font=("Terminal bold",8), anchor=S,
                    text="Para pasar las imágenes de DN a valores de reflectanciasiga los siguientes pasos:\n\n"
                    
                        "\n 1. Haga clic sobre el botón Abrir fichero. Posteriormente, elija el metadato de las imágenes."
                        "\n\n 2. Una vez obtenida la ruta del metadato haga clic sobre el botón Leer metadato."
                        "\n\n 3. Copie y pegue la ruta de la carpeta que contiene las imágenes: los separadores deben \nser de tipo \. Haga clic sobre Cargar ruta imágnes. "
                        "\n\n 4. Copie y pegue el nombre genérico de las imágenes: Es decir antes de _B#.TIF. \nHaga clic sobre Establecer destino"
                        "\n\n 5. Copie y pegue la ruta de la carpeta que almacenará los resultados: los separadores deben \nser de tipo \. Haga clic sobre Establecer destino. "
                        "\n\n 6. Finalmente, haga clic sobre iniciar proceso y espere a la finalización de la tarea:\n se notificará mediante una alerta."
                        "\n\n\n\n Finalizado el proceso anterior, podrá efectuar el cálculo de los índices disponibles en la lista \nhaciendo clic sobre el boton correspondiente. Para los VIs SAVI y PVI\n es necesario introducir el valor de las constantes solicitadas.")

      botonimagen.place(x=130,y=0)
      titulo.place(x=190,y=215)
      instrucciones.place(x=17, y=270)
      dos.transient(root)
      dos.grab_set()
      root.wait_window(dos)
    
    
    
def saliraplicacion():
    valor=messagebox.askquestion("Salir","¿Desea salir de la aplicación?")
    if valor =="yes":
        root.destroy()


def cerrarDocumento():
        valor=messagebox.askretrycancel("Reitentar","No es posible cerrar archivo bloqueado")
        if valor ==True:
            root.destroy()
            
            
         
        
def  abreFichero():
    messagebox.showinfo("Información","Seleccione el archivo del metadato de las imágenes: ....._MTL.txt. Posteriormete haga clic en el botón Leer metadato. ")
    fichero=filedialog.askopenfilename(title="Abrir",filetypes=(("Ficheros de Python","*.py"),
                                                                ("Ficheros de texto", "*.txt"),
                                                                ("Todos los archivos","*.*")))
    
    return var.set(fichero)

def carpetaimg ():
    global path_img
    path_img=  str(entrada1.get()) #Cambiar ruta a la carpeta que contenga las imgs
    print("esta es la ruta de la carpeta  "+path_img)

def nombreimgs ():
    global imagen
    imagen=  str(entrada2.get()) #Cambiar ruta a la carpeta que tenga el metadato
    print("esta es nomebre de las imgs  "+imagen)
    
    
def rutaresultados ():
    global resultados
    resultados=  str(entrada3.get()) #Cambiar ruta a la carpeta que tenga el metadato
    print("esta es la ruta de los resultados  "+resultados)
    create_folder(resultados)



##3.FUNCION PARA CREAR CARPETA SI NO EXISTE
def create_folder(path):
    if not os.path.exists(path):
            os.mkdir(path)


##CALCULO INDICADORES DE VEGETACION




def rvi(RED, NIR):
    rvi= RED/NIR
    return (rvi)
def disparadorRVI():
    calculo_rvi_l8=rvi(reflectancias[2],reflectancias[3])
    salida_rvi=(resultados+os.sep+'l8_rvi.TIF')
    guardar_tif(salida_rvi,calculo_rvi_l8,img_banda)
    messagebox.showinfo(message="Proceso Terminado, Ratio Vegetation Index calculado", title="RVI")
    
    
    
    
def ndvi(RED,NIR):
    ndvi=(NIR-RED)/(NIR+RED)
    return(ndvi)
def disparadorNDVI():
    calculo_ndvi_l8=ndvi(reflectancias[2],reflectancias[3])
    salida_ndvi=(resultados+os.sep+'l8_ndvi.TIF')
    guardar_tif(salida_ndvi,calculo_ndvi_l8,img_banda)
    messagebox.showinfo(message="Proceso Terminado, Normalized Difference Vegetation Index calculado", title="NDVI")
    
    
    
     
def pvi(RED,NIR,b,a):
    pvi=(NIR-RED-b)/(math.sqrt(a**2 +1))
    return(pvi)
def disparadorPVI():
    a= float(apvi.get())
    b= float(bpvi.get())
    calculo_pvi_l8=pvi(reflectancias[2],reflectancias[3],b,a)
    salida_pvi=(resultados+os.sep+'l8_pvi.TIF')
    guardar_tif(salida_pvi,calculo_pvi_l8,img_banda)
    messagebox.showinfo(message="Proceso Terminado, Perpendicular Vegetation Index calculado", title="PVI")
    
 
  
def savi(RED,NIR,L):
    savi= (1 + L)*(NIR-RED)/(NIR+RED+ L)
    return(savi)
def disparadorSAVI():
    L = float(lsavi.get())
    calculo_savi_l8=savi(reflectancias[2], reflectancias[3],L)
    salida_savi=(resultados+os.sep+'l8_savi.TIF')
    guardar_tif(salida_savi,calculo_savi_l8,img_banda)
    messagebox.showinfo(message="Proceso Terminado, Soil Adjusted Vegetation Índex calculado", title="SAVI")     
    
   
   
def arvi(BLUE,RED,NIR):
    arvi2=(NIR-(RED-0.5*(RED-BLUE)))/(NIR+(RED-0.5*(RED-BLUE)))
    return(arvi2)
def disparadorARVI():
    calculo_arvi_l8=arvi(reflectancias[0],reflectancias[2],reflectancias[3])
    salida_arvi=(resultados+os.sep+'l8_arvi.TIF')
    guardar_tif(salida_arvi,calculo_arvi_l8,img_banda)
    messagebox.showinfo(message="Proceso Terminado, Atmospherically Resistant Vegetation Index calculado", title="ARVI")  
    
        
 
def gemi(RED,NIR):
    n=(2*(NIR**2 -RED**2)+1.5*NIR+0.5*RED)/(NIR+RED+0.5)
    gemi=(n*(1-0.25*n))-((RED-0.125))/(1-RED)
    return(gemi)
def disparadorGEMI():
    calculo_gemi_l8=gemi(reflectancias[2],reflectancias[3])
    salida_gemi=(resultados+os.sep+'l8_gemi.TIF')
    guardar_tif(salida_gemi,calculo_gemi_l8,img_banda)
    messagebox.showinfo(message="Proceso Terminado, Global Environmental Monitoring Index calculado", title="GEMI")  




def msavi(RED,NIR):
    msavi=(2*NIR+1-np.sqrt((2*NIR+1)**2 -8*(NIR-RED)))/(2)
    return(msavi)
def disparadorMSAVI():
    calculo_msavi_l8=msavi(reflectancias[2],reflectancias[3])
    salida_msavi=(resultados+os.sep+'l8_msavi.TIF')
    guardar_tif(salida_msavi,calculo_msavi_l8,img_banda)
    messagebox.showinfo(message="Proceso Terminado, A modified soil adjusted vegetation index calculado", title="MSAVI") 
    
    
    
def gari(BLUE,GREEN,RED,NIR):
    gari2=(NIR-(GREEN-(BLUE-RED)))/(NIR+(GREEN-(BLUE-RED)))
    return(gari2)
def disparadorGARI():
    calculo_gari_l8=gari(reflectancias[0],reflectancias[1],reflectancias[2],reflectancias[3])
    salida_gari=(resultados+os.sep+'l8_gari.TIF')
    guardar_tif(salida_gari,calculo_gari_l8,img_banda)
    messagebox.showinfo(message="Proceso Terminado, A Green Atmospherically Resistant Vegetation Index calculado", title="GARI") 



def evi(BLUE,RED,NIR):
    evi= 2.5*(NIR-RED)/((NIR+ 6*RED- 7.5* BLUE)+ 1)
    return(evi)
def disparadorEVI():
    calculo_evi_l8=evi(reflectancias[0],reflectancias[2],reflectancias[3])
    salida_evi=(resultados+os.sep+'l8_evi.TIF')
    guardar_tif(salida_evi,calculo_evi_l8,img_banda)
    messagebox.showinfo(message="Proceso Terminado, Enhanced Vegetation Index calculado", title="EVI") 

    

def gndvi(GREEN,NIR):
    gndvi=(NIR-GREEN)/(NIR+GREEN)
    return(gndvi)
def disparadorGNDVI():
    calculo_gndvi_l8=gndvi(reflectancias[1],reflectancias[3])
    salida_gndvi=(resultados+os.sep+'l8_gndvi.TIF')
    guardar_tif(salida_gndvi,calculo_gndvi_l8,img_banda)
    messagebox.showinfo(message="Proceso Terminado, Green Normalized Difference Vegetation Index calculado", title="GNDVI") 
    
    

def dvi(RED,NIR):
    dvi=NIR-RED
    return(dvi)
def disparadorDVI():
    calculo_dvi_l8=dvi(reflectancias[2],reflectancias[3])
    salida_dvi=(resultados+os.sep+'l8_dvi.TIF')
    guardar_tif(salida_dvi,calculo_dvi_l8,img_banda)
    messagebox.showinfo(message="Proceso Terminado, Difference Vegetation Index calculado", title="DVI") 


def tvi(RED,NIR):
    tvi= np.sqrt(((NIR-RED)/(NIR+RED))+0.5)
    return(tvi)
def disparadorTVI():
    calculo_tvi_l8=tvi(reflectancias[2],reflectancias[3])
    salida_tvi=(resultados+os.sep+'l8_tvi.TIF')
    guardar_tif(salida_tvi,calculo_tvi_l8,img_banda)
    messagebox.showinfo(message="Proceso Terminado, Transformed Vegetation Index calculado", title="TVI") 

 
    
def yvi(GREEN,RED,NIR,SWIR):
    yvi=((-0.899*GREEN)+(0.428*RED)+(0.076*NIR)-(0.041*NIR))
    return(yvi)
def disparadorYVI():
    calculo_yvi_l8=yvi(reflectancias[1],reflectancias[2],reflectancias[3])
    salida_yvi=(resultados+os.sep+'l8_yvi.TIF')
    guardar_tif(salida_yvi,calculo_yvi_l8,img_banda)
    messagebox.showinfo(message="Proceso Terminado, Yellow Vegetation Index calculado", title="YVI") 
    
 
    
 
    

#funciones de la automatización 
#------------------------------------------------------------------------------------------

##1. FUNCION PARA LEER METADATO 
   
var= StringVar()
    
# def obtenerRutametadato():
#     ruta= str(var.get())
#     archivo_mtl= ruta #Cambiar ruta a la carpeta que tenga el metadato
#     print(archivo_mtl)
#     ruta_mtl=open(archivo_mtl,"r")
#     datos=metadato(ruta_mtl)




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
    
def reflectancia (M,ND,A,sun_elevation):
    reflec=(M*ND+A)/np.sin(sun_elevation)
    return(reflec)

##CORRECCION ATMOSFERIA POR HISTOGRAMA
def refle_corregida(r):
    correccion= r-np.nanmin(r)
    return(correccion)   
    
##1. FUNCION PARA LEER METADATO
def obtenerRutametadato ():
    global archivo_mtl
    global ruta_mtl
    global datos    
    archivo_mtl=  str(var.get()) #Cambiar ruta a la carpeta que tenga el metadato
    print(archivo_mtl)
    ruta_mtl=open(archivo_mtl,"r")
    datos=metadato(ruta_mtl)
    
    
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




##SCRIPT


def ndareflectancia():
    
    print("estos son los parametros")
    print("*************************")
    print("*************************")
    print(path_img)
    print(imagen)
    print(resultados)  
    
    global reflectancias
    reflectancias= []
    for banda in range (1,7):
        global img_banda
        global nd   
        print ("Inicia procesamiento de: "+imagen+"_B"+str(banda)+".TIF")
        img_banda=gdal.Open(path_img+os.sep+imagen+"_B"+str(banda)+".TIF")
        nd=img_banda.ReadAsArray().astype('float')
        nd [[nd==0]] = np.nan
        if (banda==2 or banda==3 or banda==4 or banda==5 or banda==6):
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
    messagebox.showinfo(message="Proceso Terminado", title="DN To Reflectance")


   

##DEFINICION DE VARIABLES







#BARRA DE MENÚ

barraMenu=Menu(root)
root.config(menu=barraMenu, width= 600, height=300)

archivoMenu= Menu(barraMenu, tearoff=0)
# archivoMenu.add_command(label="Nuevo")
# archivoMenu.add_command(label="Guardar")
# archivoMenu.add_command(label="Reiniciar")
archivoMenu.add_command(label="Cerrar", command= cerrarDocumento)
archivoMenu.add_command(label="Salir", command= saliraplicacion)

archivoEdicion= Menu(barraMenu)
archivoEdicion.add_command(label="Copiar")
archivoEdicion.add_command(label="Cortar")
archivoEdicion.add_command(label="Pegar")



archivoHerramientas= Menu(barraMenu)




archivoAyuda= Menu(barraMenu)
archivoAyuda.add_command(label="Guía", command= guia)
archivoAyuda.add_command(label="Documentación", command= avisoLicencia)
archivoAyuda.add_command(label="About", command= infoAdicional)


barraMenu.add_cascade(label="Archivo", menu=archivoMenu)

# barraMenu.add_cascade(label="Edición", menu=archivoEdicion)

# barraMenu.add_cascade(label="Herramientas", menu=archivoHerramientas)

barraMenu.add_cascade(label="Ayudas", menu=archivoAyuda)




#---------------------------------------botones------------------------------------------------------------ 

botonExaminar = Button(miFrame, width=17, text="Abrir fichero", cursor="hand2", command=abreFichero)
botonExaminar.grid(row=2, column=1,padx=3, pady=10)


botonExaminar = Button(miFrame, width=17, text="Leer metadato", command=obtenerRutametadato)
botonExaminar.grid(row=2, column=2,padx=3, pady=10)

entrada1= Entry(miFrame, width=59)
entrada1.grid(row=3, column=0)
beRutaimg = Button(miFrame, width=17, text="Cargar ruta imáganes", cursor="hand2",command=carpetaimg)
beRutaimg.grid(row=3, column=1,padx=3, pady=10)

#be  boton ruta tal.....

entrada2= Entry(miFrame, width=59)
entrada2.grid(row=4, column=0)
beRutanombreimg = Button(miFrame, width=17, text="Cargar nombre imgs", cursor="hand2",command= nombreimgs)
beRutanombreimg.grid(row=4, column=1,padx=3, pady=10)

entrada3= Entry(miFrame, width=59)
entrada3.grid(row=5, column=0)
beRutasalida = Button(miFrame, width=17, text="Establecer destino", cursor="hand2", command=rutaresultados)
beRutasalida.grid(row=5, column=1,padx=3, pady=10)


iniciarproceso = Button(miFrame, width=17, text="Iniciar proceso",font= "Helvetica 10 bold",cursor="hand2", command=ndareflectancia)
iniciarproceso.grid(row=6, column=0)


botonrvi = Button(miFramevi, width=17, text="RVI", cursor="hand2", command=disparadorRVI)
botonrvi.grid(row=8, column=0,padx=5, pady=5)

botonNDVI= Button(miFramevi, width=17, text="NDVI", cursor="hand2", command=disparadorNDVI)
botonNDVI.grid(row=9, column=0,padx=5, pady=5)


botonARVI = Button(miFramevi, width=17, text="ARVI", cursor="hand2", command=disparadorARVI)
botonARVI.grid(row=11, column=0,padx=5, pady=5)


botonGEMI = Button(miFramevi, width=17, text="GEMI", cursor="hand2", command=disparadorGEMI)
botonGEMI.grid(row=13, column=0,padx=5, pady=5)


botonMSAVI = Button(miFramevi, width=17, text="MSAVI", cursor="hand2", command=disparadorMSAVI)
botonMSAVI.grid(row=10, column=0,padx=5, pady=5)


botonGARI = Button(miFramevi, width=17, text="GARI", cursor="hand2", command=disparadorGARI)
botonGARI.grid(row=8, column=1,padx=5, pady=5)


botonEVI = Button(miFramevi, width=17, text="EVI", cursor="hand2", command=disparadorEVI)
botonEVI.grid(row=9, column=1,padx=5, pady=5)

botonGNDVI = Button(miFramevi, width=17, text="GNDVI", cursor="hand2", command=disparadorGNDVI)
botonGNDVI.grid(row=10, column=1,padx=5, pady=5)


botonDVI = Button(miFramevi, width=17, text="DVI", cursor="hand2", command=disparadorDVI)
botonDVI.grid(row=11, column=1,padx=5, pady=5)

botonTVI = Button(miFramevi, width=17, text="TVI", cursor="hand2", command=disparadorTVI)
botonTVI.grid(row=12, column=0,padx=5, pady=5)



botonGEMI = Button(miFramevi, width=17, text="YVI", cursor="hand2", command=disparadorYVI)
botonGEMI.grid(row=11, column=1,padx=5, pady=5)


#--------------------------------------------SAVI BOTON----------------------------------------------

factorL= Label(miFramevisavi,bg ='#DEDFDB' ,text="Ajuste del suelo L : ", width=15) #label L SAVI
factorL.grid(row=14,column=0,padx=5)


lsavi= Entry(miFramevisavi, width=15)
lsavi.grid(row=14, column=1,padx=5)


botonSAVI = Button(miFramevisavi, width=17, text="SAVI", cursor="hand2", command=disparadorSAVI)
botonSAVI.grid(row=14, column=2, padx=5)

#-------------------------------------------- PVI BOTON----------------------------------------------

apvi= Label(miFramevipvi,bg ='#DEDFDB' ,text="Valor constante a : ", width=15) #label a
apvi.grid(row=16,column=0, padx=5)

apvi= Entry(miFramevipvi, width=15)
apvi.grid(row=16, column=1, padx=5)


bpvi= Label(miFramevipvi,bg ='#DEDFDB' ,text="Valor constante b : ", width=15) #label b
bpvi.grid(row=18,column=0, padx=5)

bpvi= Entry(miFramevipvi, width=15)
bpvi.grid(row=18, column=1, padx=5)



botonPVI = Button(miFramevipvi, width=17, text="PVI", cursor="hand2", command=disparadorPVI)
botonPVI.grid(row=17, column=2, padx=5)




#------------------------------------Label----------------------------------------------------------
examinarMetadato= Label(miFrame, bg='#C9C5DC',textvariable=var, width=50) #caja para ruta del metadato
examinarMetadato.grid(row=2, column=0)

labelindices= Label(miFramevi0, bg='#29A436',text= "ÍNDICES",font= "Helvetica 10 bold", width=50) #titulo índices
labelindices.grid(row=7, column=0)



root.mainloop()