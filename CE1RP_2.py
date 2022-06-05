from pyautocad import APoint, Autocad, aDouble
from tkinter import messagebox
from tkinter import filedialog
from io import open


#Variables:-------------------------------------------------------------------------------------------------------------------------------------------

puntos = []
E1 = None
revertir = False
direccion = ''
ejecucion = True

#Funciones:------------------------------------------------------------------------------------------------------------------------------------------------------

def reasignar_E1_revertir(lista_puntos, new_E1, revertir):
	"""
	Recibe la lista de puntos extraidos del pm y revierte la lista en caso de que el usuario lo desee.
	-el argumento "revertir" es de tipo booleano.
	-"new_E1" es la nueva estacion uno. 	
	"""
	new_E1 = new_E1 - 1#para que coincida con los indices de la lista.

	if new_E1 < 0 or new_E1 > (len(lista_puntos) -1):
		return None
	
	else:
		#reasignar E1:
		new_lista_puntos = [lista_puntos[new_E1]] + lista_puntos[new_E1 + 1:] + lista_puntos[:new_E1]

		#revertir en caso de...
		if revertir == True:
			new_lista_puntos = [new_lista_puntos[0]] + list(reversed(new_lista_puntos[1:]))

		return new_lista_puntos


def get_and_show_data():
	"""
	Esta función colecta la informacion recibida, comprueba que sea correcta y la muestra al usuario. 
	"""	
	global direccion
	global puntos

	direccion = filedialog.askopenfilename(title="Busque PM(text)", initialdir = "desktop", filetypes = (("Ficheros de Texto", "*.txt"), ("Todos los Ficheros", "*.*")))

	if direccion == '':
		print("ALERTA: SI NO ELIGE EL ARCHIVO DE TEXTO NO SE PODRA SEGURI CON LA EJECUCION")
	
	else:
		archivo = open(direccion, "r")
		archivo = archivo.readlines()	
		
		if not(archivo[0] == "AutoCAD-MIM por FeloCAD\n"):
			print("ALERTA: ESTE ARCHIVO DE TEXTO NO ES PRODUCTO DEL COMANDO PM")

		else:
			for i in range(1, len(archivo)):
				try:
					archivo[i] = archivo[i].split()
					puntos.append((round(float(archivo[i][0]), 3), round(float(archivo[i][1]), 3)))#En este caso son tuplas

				except:	
					print("ERROR: HAY UN ERROR EN LA LINEA No.{}".format(i + 1))
					puntos = []
					break	

			if not puntos == []:
				#Eliminar puntos repetidos
				while puntos[0][0] == puntos[len(puntos) - 1][0] and puntos[0][1] == puntos[len(puntos) - 1][1]:
					puntos.pop()
					#print("Bye!")

				print("Estas son las estacines y sus coordenadas: \n ")
				for numero, punto in enumerate(puntos, start = 1):
					print("E-{}: E = {}, N = {}".format(numero, punto[0], punto[1]))
				print(" ")
				se_puede = True
				#print(puntos)

def trazar_PL(lista_puntos):
	"""
	Esta función se encarga de trazar la nueva polilinea y marcar la Nueva E-1.
	"""

	para_PL = []
	acad = Autocad()

	for i in range(len(lista_puntos)):
		para_PL.append(lista_puntos[i][0])
		para_PL.append(lista_puntos[i][1])

	#print(para_PL)
			
	punto_E1 = APoint(lista_puntos[0][0], lista_puntos[0][1])
	"""
	#Estas ultimas tres son las coordenadas de la nueva E-1, pero sospecho que existe un comando que hace esto.

	para_PL.append(punto_E1.x)	
	para_PL.append(punto_E1.y)
	para_PL.append(0)
	"""
	#Crear y editar polilinea:

	para_PL = aDouble(para_PL)
	nueva_polilinea = acad.model.AddLightWeightPolyline(para_PL)#Este metodo hace que el objeto creado sea del tipo "Polilyne" no "2D Polyline". 
	nueva_polilinea.Color = 1
	nueva_polilinea.LineType = "ACAD_ISO04W100"
	nueva_polilinea.Closed = True
	nueva_polilinea.ConstantWidth = 0.1
	nueva_polilinea.LinetypeScale = 0.15

	text_E1 = acad.model.AddText("Nueva E-1", APoint(punto_E1.x + 0.7, punto_E1.y), 1)
	text_E1.Color = 2

	acad.model.AddCircle(punto_E1, 0.5).Color = 2


	print("La Nueva Polilinea ha sido Trazada con Exito !!")
	#print("Nota: El objeto creado es una Polilinea 2D, para transformarla a una Polilinea normal vaya a Modify (Modificar) --> Edit Polyline (Editar Polilinea), seleccione la polilinea y luego pulse 'Escape' ")
	print("-------------------------------------------------------------------------------------------------------")


#Ejecucion:-----------------------------------------------------------------------------------------------------------------------------------------------------------------

print("Este programa sirve para reasignar la Estación No.01 de una polilinea e invertir el sentido en el que ha sido dibujada en caso de que se desee.")
print("Seleccione un archivo de texto que sea el resultado de aplicar el comando 'PM' a la polilinea que quiere editar.")
print(" ")
E1 = input("Pulse Enter para continuar")
E1 = None

while ejecucion:
	get_and_show_data()
	if not (puntos == []):		
		while True:
			try:
				E1 = int(input("Especifique el numero de la Estación que quiere asignar como la Estación No.01: "))
				indice = E1 - 1
				if indice < 0 or indice >= len(puntos):
					print("ERROR: ESTA POLILINEA NO POSEE ESTACION No.{}\nPOR FAVOR INDIQUE UN NUMERO ENTRE 1 y {}".format(indice + 1, len(puntos)))
				else:	
					break
			except ValueError:
				print("ERROR: DEBE INTRODUCIR UN VALOR NUMERICO")
				

		revertir = input("Desea cambiar el sentido de dibujo de la Polilinea ? (1 = Si, otra tecla = No): ")
	
		if revertir == "1":
			revertir = True
		else:			
			revertir = False

		nuevos_puntos = reasignar_E1_revertir(puntos, E1, revertir)
		

		print(" ")
		print("Estos son los puntos en el nuevo orden: \n")

		for numero, punto in enumerate(nuevos_puntos, start = 1):
			print("E-{}: E = {}, N = {}".format(numero, punto[0], punto[1]))

		print(" ")	
		trazar_PL(nuevos_puntos)
		puntos = []#borrar los puntos en caso de una nueva ejecucion.

		ejecucion = input("Desea continuar con la ejecución ? (1 = Si, otro caracter = No): ")
		if not(ejecucion == "1"):
			ejecucion = False
			print("Fin de la Ejecución")	
				
	else:
		ejecucion = input("Desea continuar con la ejecución ? (1 = Si, otro caracter = No): ")
		if not(ejecucion == "1"):
			ejecucion = False
			print("Fin de la Ejecución")
		



















































