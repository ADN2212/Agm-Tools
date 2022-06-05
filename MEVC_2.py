from pyautocad import APoint, Autocad
from tkinter import messagebox
from tkinter import filedialog
from io import open
from random import randint

print(" Este porgrama sirve para marcar las estaciones de una polilinea \n asegurece de tener AutoCAD abierto y responda las siguentes preguntas: \n")

#Variables:
ejecucion = True
radio = float()
altura_texto = None
direccion = ''
puntos = []
desicion = "1"

def get_data():
	"""
	Esta funcion se encarga de colectar la informacion para retornar los argumentos que resivirá la funcion principal.
	"""
	global radio
	global altura_texto
	global direccion
	global puntos

	no_cumple = True

	while no_cumple:
		try:
			radio = float(input("Espesifique el radio de los circulos: "))
			if radio <= 0:
				print("Error: Este valor no puede ser negativo")
			else:	
				no_cumple = False

		except ValueError:
			print("Error: Debe ser un valor numerico")

	no_cumple = True

	altura_texto = input("Desea anotar las coordenadas mas al Norte, Sur, Este y Oeste? (1 = Si, otro caracter = No): ")

	if altura_texto == "1":
		while no_cumple:
			try:
				altura_texto = float(input("Espefisique la altura del texto: "))

				if altura_texto <= 0:
					print("Error: Este valor no puede ser cero ni negativo")
				else:
					no_cumple = False
				
			except ValueError:
				print("Error: Debe ser un valor numerico")		
	else:
		altura_texto = None

	no_cumple = True

	direccion = filedialog.askopenfilename(title="Busque PM(text)", initialdir = "desktop", filetypes = (("Ficheros de Texto", "*.txt"), ("Todos los Ficheros", "*.*")))

	while direccion == '' and no_cumple:

		messagebox.showwarning("Alerta!!", "Debe elegir un archivo de tipo txt para poder realizar esta acción")
		continuar = input("Desea continuar con la ejecución ? (1 = Si, otro caracter = No): ")
		
		if not (continuar == "1"):
			no_cumple = False# Detiene el ciclo.
			
		else:
			direccion = filedialog.askopenfilename(title="Busque PM(text)", initialdir = "desktop", filetypes = (("Ficheros de Texto", "*.txt"), ("Todos los Ficheros", "*.*")))				

	if not(direccion == ''):
		archivo = open(direccion, "r")
		archivo = archivo.readlines()	
		
		if not(archivo[0] == "AutoCAD-MIM por FeloCAD\n"):
			messagebox.showwarning("Alerta!!", "Este archivo de texto no es producto del comando PM")


		else:
			for i in range(1, len(archivo)):
				try:
					archivo[i] = archivo[i].split()
					puntos.append(APoint(round(float(archivo[i][0]), 3), round(float(archivo[i][1]), 3)))

				except:	
					messagebox.showwarning("Error!!", "Hay un error en la linea No.{}".format(i + 1))
					puntos = []
					break

		#Eliminar Los puntos Repetidos:
		if puntos != []:
			while puntos[0].x == puntos[len(puntos)-1].x and puntos[0].y == puntos[len(puntos) - 1].y:
				puntos.pop()
				print("Punto Repetido Eliminado!!")
		

	return (radio, altura_texto, puntos)


def draw(tupla_rap):
	"""
	Esta funcion se encarga de dibujar los circulos y las estaciones en AutoCAD
	"""
	if len(puntos) == 0:
		pass

	else:
		acad = Autocad()
		is_there = False

		#Buscar si el layer de las estaciones ya está creado, en caso de que se repita la ejecución

		for Layer in acad.doc.Layers:
			#print(Layer.Name)
			if Layer.Name == "Layer_Estaciones":
				is_there = True
				break

		if is_there:
			layer_anterior = acad.doc.ActiveLayer#Para reaccicnarlo al final.
			acad.doc.ActiveLayer = acad.doc.Layers.Item("Layer_Estaciones")#para dibujar sobre este Layer
			
			print("Layer_Estaciones Existente")

		else:
			#En caso de que no exista será creado y asignado al layer activo para dibujar en/con el				
			Layer_Estaciones = acad.doc.Layers.Add("Layer_Estaciones")
			layer_anterior = acad.doc.ActiveLayer
			acad.doc.ActiveLayer = Layer_Estaciones
			Layer_Estaciones.Color = 2#El amarillo es el color que uso para las letras.

			print("Layer_Estaciones Creado")

		if tupla_rap[1] == None:
			for punto in tupla_rap[2]:
				acad.model.AddCircle(punto, tupla_rap[0]).Color = 7#para que los "puntos" sean de color blanco.

			acad.doc.ActiveLayer = layer_anterior#vuelve a hacer que el layer principal se el que estava activo antes de la ejecución

			print("Hecho!!")

		else:
			#Hallar las coordenadas de las Estaciones mas al Norte, Sur, Este y Oeste.
		
			punto_minima_N = [0, APoint(5000000, 5000000)]
			punto_maxima_N = [0, APoint(-5000000, -5000000)]
			punto_minima_E = [0, APoint(5000000, 5000000)]
			punto_maxima_E = [0, APoint(-5000000, -5000000)]


			for i in range(len(tupla_rap[2])):
				if tupla_rap[2][i].y > punto_maxima_N[1].y:
					punto_maxima_N[0] = i + 1
					punto_maxima_N[1] = tupla_rap[2][i]

				if tupla_rap[2][i].y < punto_minima_N[1].y:
					punto_minima_N[0] = i + 1 
					punto_minima_N[1] = tupla_rap[2][i]
			
				if tupla_rap[2][i].x > punto_maxima_E[1].x:
					punto_maxima_E[0] = i + 1
					punto_maxima_E[1] = tupla_rap[2][i]

				if tupla_rap[2][i].x < punto_minima_E[1].x:
					punto_minima_E[0] = i + 1 
					punto_minima_E[1] = tupla_rap[2][i]

			for punto in tupla_rap[2]:
				acad.model.AddCircle(punto, tupla_rap[0]).Color = 7

			punto_minima_N[1].y = punto_minima_N[1].y - (tupla_rap[1] + tupla_rap[0] + 0.2)#Para que el texto no se meta al circulo.
			punto_minima_E[1].x = punto_minima_E[1].x + tupla_rap[0] + 0.2	
			punto_maxima_N[1].y	= punto_maxima_N[1].y + tupla_rap[0] + 0.2   		
			punto_maxima_E[1].x = punto_maxima_E[1].x + tupla_rap[0] + 0.2


			#Probar si la E-1 es uno de los puntos limites:

			marcar_E1 = True

			for punto_max_min in [punto_minima_E, punto_maxima_E, punto_maxima_N, punto_minima_N]:
				if punto_max_min[0] == 1:
					marcar_E1 = False#si alguno de estos es la E-1 esta no será marcada, porque ya lo estará

			if marcar_E1:
				punto_base = APoint(tupla_rap[2][0].x + tupla_rap[0] + 0.2, tupla_rap[2][0].y - (tupla_rap[0] + 0.2))
				acad.model.AddText("E-1", punto_base, tupla_rap[1])		
					
				
			acad.model.AddText("E-{}".format(punto_minima_N[0]), punto_minima_N[1], tupla_rap[1])
			acad.model.AddText("E-{}".format(punto_maxima_N[0]), punto_maxima_N[1], tupla_rap[1])
			acad.model.AddText("E-{}".format(punto_minima_E[0]), punto_minima_E[1], tupla_rap[1])
			acad.model.AddText("E-{}".format(punto_maxima_E[0]), punto_maxima_E[1], tupla_rap[1])

			if randint(1, 10) == 5:#Una probabilidad de 1 en 10 de que esto suceda.
				punto_medio = APoint((punto_maxima_N[1].x + punto_minima_N[1].x)/2, (punto_maxima_N[1].y + punto_minima_N[1].y)/2) 
				acad.model.AddText("Written By Agm: Juan A. Núñez", punto_medio, tupla_rap[1])

			acad.doc.ActiveLayer = layer_anterior
			
			print("Hecho!!")


while ejecucion:
	draw(get_data())
	desicion = input("Desea volver a ejecutar el programa ? (1 = Si, otro caracter = No): ")
	if not(desicion == "1"):
		ejecucion = False
		print("Fin de la ejecución")
	
	else:
		print("Ingrese nueva información \n")
		#Drvolver las variables a su estado inicial:
		radio = float()
		altura_texto = None
		direccion = ''
		puntos = []
		desicion = "1"		
	





























