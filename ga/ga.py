import sys
import fileinput
import random
import subprocess


class individual(object):
	def __init__(self,SIZE_,maxnumber_,maxweight_,value_,weight_):
		self.SIZE=SIZE_
		self.maxnumber=maxnumber_
		self.maxweight=maxweight_
		self.value=value_
		self.weight=weight_
		self.genotype=[]
		for i in range(self.SIZE):
			self.genotype.append(random.randint(0,self.maxnumber))

	def fitness(self):
		fitcounter = 0;
		for i in range(96,101):
			replaceLine('./0SumBot/zeroSumBot.java', 'double oPWNumShipsProduction1 = ', '    double oPWNumShipsProduction1 = '+str(0.6)+';')
			replaceLine('./0SumBot/zeroSumBot.java', 'int oPNumShips = ', '    int oPNumShips = '+str(21)+';')
			replaceLine('./0SumBot/zeroSumBot.java', 'int oPNumShipsR ', '    int oPNumShipsR = '+str(6)+';')
			replaceLine('./0SumBot/zeroSumBot.java', 'int oPGrowthRate =  ', '    int oPGrowthRate =  '+str(20)+';')
			replaceLine('./0SumBot/zeroSumBot.java', 'int oPGrowthRateR = ', '    int oPGrowthRateR = '+str(5)+';')
			replaceLine('./0SumBot/zeroSumBot.java', 'int oENumShips = ', '    int oENumShips = '+str(20)+';')
			replaceLine('./0SumBot/zeroSumBot.java', 'int oENumShipsR = ', '    int oENumShipsR = '+str(5)+';')
			replaceLine('./0SumBot/zeroSumBot.java', 'int oEGrowthRate = ', '    int oEGrowthRate = '+str(20)+';')
			replaceLine('./0SumBot/zeroSumBot.java', 'int oEGrowthRateR = ', '    int oEGrowthRateR = '+str(5)+';')
			replaceLine('./0SumBot/zeroSumBot.java', 'int oNNumShips = ', '    int oNNumShips = '+str(20)+';')
			replaceLine('./0SumBot/zeroSumBot.java', 'int oNNumShipsR = ', '    int oNNumShipsR = '+str(5)+';')
			replaceLine('./0SumBot/zeroSumBot.java', 'int oNGrowthRate = ', '    int oNGrowthRate = '+str(20)+';')
			replaceLine('./0SumBot/zeroSumBot.java', 'int oNGrowthRateR = ', '    int oNGrowthRateR = '+str(5)+';')
			replaceLine('./0SumBot/zeroSumBot.java', 'int oDistance = ', '    int oDistance = '+str(39)+';')
			replaceLine('./0SumBot/zeroSumBot.java', 'int oDistanceR = ', '    int oDistanceR = '+str(5)+';')
			replaceLine('./0SumBot/zeroSumBot.java', 'int numFleets = ', '    int numFleets = '+str(6)+';')

			with open('evolve', 'r') as file :
				evolve = file.read()

			evolve = evolve.replace('maps/map'+str(i-1)+'.txt', 'maps/map'+str(i)+'.txt')

			with open('evolve', 'w') as file:
				file.write(evolve)

			evProc = subprocess.call("./evolve",shell=True)

			with open('winner.txt','r') as file:
				line = file.read()
				if 'Player 2 Wins!' in line:
					fitcounter+=1
		print fitcounter



def replaceLine(file_, pattern, newline):
		for line in fileinput.input(file_, inplace=True):
			if pattern in line:
				line = newline+'\n'
			sys.stdout.write(line)


if __name__ == '__main__':
	indd = individual(5,6,7,9,10)
	indd.fitness()
