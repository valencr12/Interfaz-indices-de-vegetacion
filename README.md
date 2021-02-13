# Interfaz-indices-de-vegetacion
Interfaz para la corrección de imágenes Landsat 8 y posteriormente cálculo de 13 índices de vegetación en lenguaje python
1. En el primer módulo se realiza la importación del metadato de la imagen (mtl.txt). Posteriormente, se cuenta con un botón de lectura del mismo,
quedando así guardados los datos de la imagen en la variables internas del algoritmo para su posterior uso.
2.El módulo dos, corresponde a la ruta donde se encuentran las imágenes. La ruta debe se debe copiar completa para que el algoritmo funcione correctamente.Posteriormente haga clic en el botón “Cargar ruta imágenes”.
3. El módulo tres, corresponde a la sección donde se debe ingresar (pegar) el nombre genéricos de las imágenes, es decir antes de _B#.TIF. Posteriormentehaga clic en el botón “Cargar nombre imgs”
4. El módulo cuatro, corresponde a la entrada de la ruta donde se almacenarán los resultados. Esta carpeta debe ser creada previamente. Una vez establecido el destino de los productos haga clic en el botón “Establecer destino”
5. El módulo cinco, corresponde al botón que inicia el proceso deconversión de ND a reflectancia, correcciones y posteriormenteel almacenamiento de las bandas corregidas.
6. El módulo seis, realiza el cálculo de los índices que no requieren parámetros adicionales. Para el cálculo de los VI solo basta con hacer clic en el índice deseado, al finalizar el proceso, la interfaz mostrará un mensaje de “Índice calculado”.
7. El módulo siete, calcula los VI que requieren de parámetro sadicionales: factor de ajuste del suelo, a o b. Una vez ingresados estos valores se hace clic en el índice deseado y al finalizar el proceso, la interfaz mostrará un mensaje de “Índice calculado”.

Para que el código funcione es necesario que el usuario cuente con python o es su defecto un entorno de desarrollo de código abierto para programación en lenguaje python, como spyder. Además es necesario que previamene instale las siguientes librerías: numpy, gdal, os, sys, math, tkinter.
Adicionalmente, la interfaz cuenta con una guía de usuario.

Nota: se deben descargar todos los archivos aquí cargados y guardarlos en una misma carpeta, finalmente el código que se debe ejecutar es el de "ventanaavanzada.py"
