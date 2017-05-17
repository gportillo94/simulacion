#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import sys

def ganoVolado():
	if random.random() >= 0.5 :
		return True
	else:
		return False

def imprimirEncabezado(index,file):
	file.write("***************\n"+"Simulacion no."+str(index)+"\n***************\n")

def main(numSim):

	print("Se simulan "+str(numSim)+" juegos")
	numSimulaciones = int(numSim)
	apuestaInicial = 10
	resultados = []

	f = open("res_sim_volados.txt", "w")

	for i in range(numSimulaciones):

		cantidad = 30
		apuesta = apuestaInicial
		imprimirEncabezado(i,f)
		while cantidad>0 and cantidad <50 :
			f.write("Cantidad = "+str(cantidad)+"\n")
			f.write("Apuesta = "+str(apuesta)+"\n")
			if apuesta > cantidad:
				apuesta = cantidad
			if ganoVolado():
				f.write("Ganas"+"\n")
				cantidad = cantidad + apuesta
				apuesta = apuestaInicial
			else:
				f.write("Pierdes"+"\n")
				cantidad = cantidad - apuesta
				apuesta = apuesta * 2
			f.write("Cantidad = "+str(cantidad)+"\n")
			f.write("---------------"+"\n")
		if cantidad>=50 :
			resultados.append(1)
		else :
			resultados.append(0)
	
	prob = sum(resultados)/float(numSimulaciones)
	print("Probabilidad de ganar = "+str(prob))

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print("Nombre:\n\tSimulacion de Volados\n")
		print("Descripcion:\n\tEsta aplicacion simula un juego de volados utilizando la siguiente estrategia de doblar la apuesta cada vez que se pierde. Por ejemplo, si se apuesta $X y se pierde, entonces se apuesta $2X; si en esta ocasión se vuelve a perder, entonces, se apuesta  $4X y así sucesivamente. Sin embargo, si al seguir esta politica sucede que la apuesta es mayor que la cantidad de que se dispone, entonces, se apuesta lo que se tiene disponible. Por el contrario, cada vez que se gane, la apuesta sera de $X\n")
		print("Opciones:\n\t./sim_volados.py [NUMERO DE SIMULACIONES]")

	else:
		main(sys.argv[1])
