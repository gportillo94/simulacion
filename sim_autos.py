#!/usr/bin/env python

import random

fact_estacionales = [1.2, 1.0, 0.9, 0.8, 0.8, 0.7, 0.8, 0.9, 1.0, 1.2, 1.3, 1.4]

test_num_aleatorio = [0.74022,0.65741,0.66083,0.08355,0.55121,0.00911,0.14060,0.14845,0.41839,0.39685,0.74416,0.53152] 

test_meses_orden = [2,3,1]

INVENTARIO_INICIAL = 0
DEMANDA_AJUSTADA = 1
INVENTARIO_FINAL = 2
FALTNTE = 3
ORDEN = 4
INVENTARIO_MENSUAL_PROM = 5

tabla = [[ 0 for i in range(6)] for j in range(12)]

def sim_demanda (N):
	if 0.000 <= N < 0.010 :
		return 35
	elif 0.010 <= N < 0.025:
		return 36
	elif 0.025 <= N < 0.045:
		return 37
	elif 0.045 <= N < 0.065:
		return 38
	elif 0.065 <= N < 0.087:
		return 39
	elif 0.087 <= N < 0.110:
		return 40
	elif 0.110 <= N < 0.135:
		return 41
	elif 0.135 <= N < 0.162:
		return 42
	elif 0.162 <= N < 0.190	:
		return 43
	elif 0.190 <= N < 0.219:
		return 44
	elif 0.219 <= N < 0.254:
		return 45
	elif 0.254 <= N < 0.299:
		return 46
	elif 0.299 <= N < 0.359:
		return 47
	elif 0.359 <= N < 0.424:
		return 48
	elif 0.424 <= N < 0.494:
		return 49
	elif 0.494 <= N < 0.574:
		return 50
	elif 0.574 <= N < 0.649	:
		return 51
	elif 0.649 <= N < 0.719	:
		return 52
	elif 0.719 <= N < 0.784:
		return 53
	elif 0.784 <= N < 0.844:
		return 54
	elif 0.844 <= N < 0.894:
		return 55
	elif 0.894 <= N < 0.934:
		return 56
	elif 0.934 <= N < 0.964:
		return 57
	elif 0.964 <= N < 0.980:
		return 58
	elif 0.980 <= N < 0.995:
		return 59
	elif 0.995 <= N < 1.000:
		return 60

def sim_entrega(N):
	if 0.000 <= N < 0.300:
		return 1
	elif 0.300 <= N < 0.700:
		return 2
	elif 0.700 <= N < 1.000:
		return 3

def calcular_inventario_final():
	for mes in tabla:
		if(mes[INVENTARIO_FINAL] == 0):
			mes[INVENTARIO_MENSUAL_PROM] = round ((mes[INVENTARIO_INICIAL]**2) / (2*mes[DEMANDA_AJUSTADA]))
		else:
			mes[INVENTARIO_MENSUAL_PROM] =  round((mes[INVENTARIO_INICIAL] + mes[INVENTARIO_FINAL])/2)

def calcular_costo_total():
	total = 0
	unidades_faltantes = 0
	total_inventarios = 0
	for mes in tabla:
		if(mes[ORDEN]):
			total+=100
		elif(mes[FALTNTE]):
			unidades_faltantes += mes[FALTNTE]
		total_inventarios +=mes[INVENTARIO_MENSUAL_PROM]
	return total + unidades_faltantes*50 + total_inventarios*1.67

def imprimir_tabla():
	for mes in tabla:
		print(mes)

def limpiar_tabla():
	for ren in range(12):
		for col in range(6):
			tabla[ren][col] = 0

def main():

	num_simulaciones = 10
	q = 200
	R = 100
	costo_total = 0

	for i in range(num_simulaciones):

		limpiar_tabla()
		tabla[0][INVENTARIO_INICIAL] = 150
		meses_orden = 0
		orden_en_proceso = False

		for numMes in range(12):

			if orden_en_proceso and meses_orden == 0:
				orden_en_proceso = False
				tabla[numMes][INVENTARIO_INICIAL] = q
			elif orden_en_proceso:
				meses_orden = meses_orden -1

			#Cada Mes
			if numMes > 0:
				tabla[numMes][INVENTARIO_INICIAL] += tabla[numMes-1][INVENTARIO_FINAL] - tabla[numMes-1][FALTNTE]

			tabla[numMes][DEMANDA_AJUSTADA] = round(sim_demanda(random.random())*fact_estacionales[numMes])
			#tabla[numMes][DEMANDA_AJUSTADA] = round(sim_demanda(test_num_aleatorio[numMes])*fact_estacionales[numMes])

			#calculo invetario_final y faltante
			if tabla[numMes][INVENTARIO_INICIAL] > tabla[numMes][DEMANDA_AJUSTADA]:
				tabla[numMes][INVENTARIO_FINAL] = tabla[numMes][INVENTARIO_INICIAL] - tabla[numMes][DEMANDA_AJUSTADA]
				tabla[numMes][FALTNTE] = 0
			else:
				tabla[numMes][INVENTARIO_FINAL] = 0
				tabla[numMes][FALTNTE] = tabla[numMes][DEMANDA_AJUSTADA] - tabla[numMes][INVENTARIO_INICIAL] 

			#calculo orden
			if tabla[numMes][INVENTARIO_FINAL] < R and not orden_en_proceso:
				tabla[numMes][ORDEN] = 1
				meses_orden = sim_entrega(random.random())
				#meses_orden = test_meses_orden.pop()
				orden_en_proceso = True

		calcular_inventario_final()
		costo_total += calcular_costo_total()

		imprimir_tabla()
		print(calcular_costo_total())

	print(costo_total/num_simulaciones)

if __name__ == '__main__':
	main()