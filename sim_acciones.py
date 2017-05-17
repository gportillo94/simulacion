#!/usr/bin/env python

from scipy.stats import norm
from scipy.stats import tmean
from scipy.stats import tstd
import matplotlib.pyplot as plt
import random

STOCK_PRICE = 0
SHARES_HELD = 1
CASH_HELD = 2
TOTAL_WORTH = 3
SHARES_PURCH = 4
SHARES_SOLD = 5
CHANGE_PRICE = 6

table = [[ 0 for i in range(7)] for j in range(22)]
totalWoths = []
cumulativeAvg = []

def calculateCumulativeAvg():
	for i in range(1,len(totalWoths)+1):
		cumulativeAvg.append(tmean(totalWoths[:i]))

def amountSharesPurch(numDay):
	if(table[numDay-1][STOCK_PRICE] < table[numDay][STOCK_PRICE]):
		return round(0.1 * table[numDay][CASH_HELD] / table[numDay][STOCK_PRICE])
	else:
		return 0

def amountSharesSold(numDay):
	if(table[numDay-1][STOCK_PRICE] > table[numDay][STOCK_PRICE]):
		return round(0.1 * table[numDay][SHARES_HELD])
	else:
		return 0

def calculateTotalWorth (i):
	return table[i][STOCK_PRICE] * table[i][SHARES_HELD] + table[i][CASH_HELD] 

def calculateCashHeld(i):
	return table[i-1][CASH_HELD] + table[i-1][STOCK_PRICE] * (table[i-1][SHARES_SOLD] - table[i-1][SHARES_PURCH])

def calculateStockPrice(numDay):
	return table[numDay][CHANGE_PRICE] + table[numDay-1][STOCK_PRICE]

def calculateSharesHeld(numDay):
	return table[numDay-1][SHARES_HELD] + table[numDay-1][SHARES_PURCH] - table[numDay-1][SHARES_SOLD]

def day0(initialStockPrice, initialSharesHeld , initialCashHeld):
	table[0][STOCK_PRICE] = initialStockPrice
	table[0][SHARES_HELD] = initialSharesHeld
	table[0][CASH_HELD] = initialCashHeld
	table[0][TOTAL_WORTH] = calculateTotalWorth(0)
	table[0][SHARES_PURCH] = 0
	table[0][SHARES_SOLD] = 0
	table[0][CHANGE_PRICE] = 0

def dailyInvariants(numDay):
	table[numDay][STOCK_PRICE] = calculateStockPrice(numDay)
	table[numDay][SHARES_HELD] = calculateSharesHeld(numDay)
	table[numDay][CASH_HELD] = calculateCashHeld(numDay)
	table[numDay][TOTAL_WORTH] = calculateTotalWorth(numDay)
	table[numDay][SHARES_PURCH] = amountSharesPurch(numDay)
	table[numDay][SHARES_SOLD] = amountSharesSold(numDay)
	
def day1():
	table[1][CHANGE_PRICE] = norm.ppf(random.random() , 0 , table[0][STOCK_PRICE]/100)
	dailyInvariants(1)

def dayN(numDay):
	table[numDay][CHANGE_PRICE] = norm.ppf(random.random() , (table[numDay-1][STOCK_PRICE] - table[numDay-2][STOCK_PRICE])/10 , table[numDay-1][STOCK_PRICE]/100)
	dailyInvariants(numDay)

def main():
	print("Welcome to the Stock Market Simulation Using Monte Carlo Techniques")
	stckPrice = int(input("Stock Price : "))
	shrsHeld = int(input("Shares Held : "))
	for numSim in range(1000):
		day0(stckPrice, shrsHeld, 50000)
		day1()
		for numDay in range(2,22):
			dayN(numDay)
		totalWoths.append(table[21][TOTAL_WORTH])
	
	print("Mean = "+str(tmean(totalWoths)))
	print("Standard Deviation = " + str(tstd(totalWoths)))	
	totalBegin = 50000+stckPrice*shrsHeld
	print("P&L = " + str( (tmean(totalWoths) - totalBegin)))

	calculateCumulativeAvg()

	plt.plot(cumulativeAvg)
	plt.show()

if __name__ == '__main__':
	main()