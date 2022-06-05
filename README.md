# Amg Tools
Algunas Herramientas que desarrollé para facilitar mi trabajo como agrimensor dibujante de planos.

<b>CE1RP</b>: Es un script que permite cambiar el primer vértice de una polilínea en AutoCAD y además revertir el sentido en el que ha sido dibujada, se hace especialmente útil cuando el dibujante crea una polilínea usando el comando “Boundary” cuyas estaciones (vértices) no están ordenadas en el sentido de las manecillas del reloj.

<b>LineaConexion</b>: Recibe como input un archivo de texto con las coordenadas de los PGs y las estaciones de conexión al inmueble, y con esta información crea la tabla de Líneas de Conexión que se muestran en los planos generales de cualquier operación catastral.

<b>MEVC</b>: Dibuja un círculo de radio especificado por el usuario en cada vértice de una polilínea, además marca las estaciones mas al Norte, Sur Este y Oeste si el usuario lo desea.

<b>Nota</b>: tanto CE1RP como MEVC reciben como input el archivo de texto que genera AutoCAD cuando se aplica el comando “PM” a una polilínea, este debe ser agregado usando el comando “APPLOAD”. Este también forma parte del repositorio como “Felo6.vlx” y que no es de mi autoría.














