# Copyright 2017 Aly Shmahell
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at http:#www.apache.org/licenses/LICENSE-2.0 . Unless
# required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# Author: Aly Shmahell

import sys
import fileinput
import random
import subprocess
import timeit

# struct to store curses color values
# sources: https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/bcolors.py
class colors:
	header = '\033[96m'
	result = '\033[94m'
	ok = '\033[92m'
	warning = '\033[91m'
	debug = '\033[90m'

def replaceLine(file_, pattern, newline):
		for line in fileinput.input(file_, inplace=True):
			if pattern in line:
				line = newline+'\n'
			sys.stdout.write(line)

class individual(object):
	def __init__(self,size):
		self.size=size
		# genotype represents the seed values overgoing evolution
		# initializing is done with values derived from tested sub-optimal values
		self.genotype = [random.uniform(0.654,0.656), random.uniform(0.123,0.125), random.uniform(0.453,0.455), random.uniform(0.070,0.072), random.uniform(0.478,0.480), random.uniform(0.114,0.116), random.uniform(0.571,0.573), random.uniform(0.294,0.296), random.uniform(0.182,0.184), random.uniform(0.513,0.515)]
		# amino-acids represent upper bound restrictions
		self.aminoAcids = [1.0,300,60,300,60,300,60,50,20,100]
		# proteins represent the final optimized paramters to be injected inside 0SumBot
		self.proteins = []
		# setting default fitness for sorting population later
		self.default_fitness = 1
		
	def fitness(self):
		# set proteins to null
		self.proteins = []
		# building optimized parameters (proteins) from genotype and amino-acids (upper bounds)
		for i in range(self.size):
			self.proteins.append(self.genotype[i]*self.aminoAcids[i])
			
		# injecting optimized parameters inside 0SumBot
		replaceLine('./0SumBot/zeroSumBot.java', 'double oPWNumShipsProduction1 = ', '    double oPWNumShipsProduction1 = '+str(self.proteins[0])+';')
		replaceLine('./0SumBot/zeroSumBot.java', 'int oPNumShips = ', '    int oPNumShips = '+str(int(self.proteins[1]))+';')
		replaceLine('./0SumBot/zeroSumBot.java', 'int oPGrowthRate =  ', '    int oPGrowthRate =  '+str(int(self.proteins[2]))+';')
		replaceLine('./0SumBot/zeroSumBot.java', 'int oENumShips = ', '    int oENumShips = '+str(int(self.proteins[3]))+';')
		replaceLine('./0SumBot/zeroSumBot.java', 'int oEGrowthRate = ', '    int oEGrowthRate = '+str(int(self.proteins[4]))+';')
		replaceLine('./0SumBot/zeroSumBot.java', 'int oNNumShips = ', '    int oNNumShips = '+str(int(self.proteins[5]))+';')
		replaceLine('./0SumBot/zeroSumBot.java', 'int oNGrowthRate = ', '    int oNGrowthRate = '+str(int(self.proteins[6]))+';')
		replaceLine('./0SumBot/zeroSumBot.java', 'int oDistance = ', '    int oDistance = '+str(int(self.proteins[7]))+';')
		replaceLine('./0SumBot/zeroSumBot.java', 'int fleetDivider = ', '    int fleetDivider = '+str(int(self.proteins[8]))+';')
		replaceLine('./0SumBot/zeroSumBot.java', 'int oLocalMinima = ', '    int oLocalMinima = '+str(int(self.proteins[9]))+';')
		
		# fitness is calculated with bot performance over multiple maps
		fitcounter = 0.0;
		
		# choosing a lower bound for a map range
		firstMap = random.randint(1,95)
		for i in range(firstMap,firstMap+5):
			print (colors.header + "map chosen: "+str(i))
			# injecting the map we want inside the evolve script
			replaceLine('./evolve','java -jar PlanetWars-viz/PlayGame.jar', 'java -jar PlanetWars-viz/PlayGame.jar 2>&1 "maps/map'+str(i)+'.txt" 10000 10000 log.txt "java -jar 3rdPartyBots/Genebot.jar" "java -jar ./0SumBot/0SumBot.jar" 2>&1 >/dev/null | echo $(tail -1) > winner.txt')
			# calling evolve script
			evProc = subprocess.call("./evolve",shell=True)
			# finding the winner
			with open('winner.txt','r') as file:
				line = file.read()
				if 'Player 2 Wins!' in line:
					fitcounter+=1.0
				if 'Draw' in line:
					fitcounter+=0.5
		self.default_fitness = fitcounter
		if fitcounter < 2.5:
			color = colors.warning
		else:
			color = colors.ok
		print color + "no. of wins: " + str(fitcounter)
		self.display(color)
	# overriding __cmp__ to perform fitness compresence	
	def __cmp__(self, other):
		return cmp(self.fitness(), other.fitness())
		
	def display(self,color):
		print color + "Individual Genotype"
		print self.genotype
		print color + "Individual Proteins"
		print self.proteins
		print "\n"
		
		
		
		
class GA(object):
	def __init__(self):
		# number of generations
		self.generations = 2
		# size of population
		self.population_size = 10
		# size of individual
		self.individual_size = 10
		# elitism percentage
		self.elderly_percentage = 10
		# 
		self.crossover_probability = 1.00
		# 
		self.mutation_probability = 0.5
		#
		self.population = []
		
		# constructing a random population
		for i in range(self.population_size):
			c = individual(self.individual_size)
			self.population.append(c)
			
	# generation generator		
	def genGen(self):
		newpopulation = []
		while len(newpopulation) < self.population_size * (1.0 - (self.elderly_percentage / 100.0)):
			print colors.header + "Size of New Population: " + str(len(newpopulation))
			size = len(self.population)
			i = random.randint(0,size-1)
			j = k = l = i

			while (j == i):
				j = random.randint(0,size-1)
			while (k == i or k == j):
				k = random.randint(0,size-1)
			while (l == i or l == j or k == l):
				l = random.randint(0,size-1)

			citizen1 = self.population[i]
			citizen2 = self.population[j]
			citizen3 = self.population[k]
			citizen4 = self.population[l]
			citizen1f = citizen1.fitness()
			citizen2f = citizen2.fitness()
			citizen3f = citizen3.fitness()
			citizen4f = citizen4.fitness()

			if citizen1f > citizen2f:
				winner1 = citizen1
				self.winner1f = citizen1f
			else:
				winner1 = citizen2
				self.winner1f = citizen2f
				
			if citizen3f > citizen4f:
				winner2 = citizen3
				self.winner2f = citizen3f
			else:
				winner2 = citizen4
				self.winner2f = citizen4f
			
			# setting children fitness to negative value
			self.child1f, self.child2f = -1.0, -1.0
			
			if random.random() < self.crossover_probability:
				child1,child2 = self.consummate(winner1,winner2)
			else:
				child1, child2 = winner1, winner2
				self.child1f, self.child2f = winner1f, winner2f
				
			if random.random() <= self.mutation_probability:
				child1 = self.mutate(child1)
				self.child1f = child1.fitness()
			if random.random() <= self.mutation_probability:
				child2 = self.mutate(child2)
				self.child2f = child2.fitness()
				
			if self.child1f < 0:
				self.child1f = child1.fitness()
			if self.child2f < 0:
				self.child2f = child2.fitness()
			
			if self.child1f > self.winner1f and self.child1f > self.winner2f:
				newpopulation.append(child1)
			else:
				newpopulation.append(winner1)

			if self.child2f > self.winner1f and self.child2f > self.winner2f:
				newpopulation.appned(child2)
			else:
				newpopulation.append(winner2)
		j = int(self.population_size * self.elderly_percentage / 100.0)
		for i in range(j-1):
			newpopulation.append(self.population[i])
		self.population = newpopulation
		self.population.sort(key=lambda obj: obj.default_fitness, reverse=True)
		print colors.header + "\nSize of generational population: " + str(len(self.population))+"\n"
			
	def consummate(self,parent1, parent2):
		child1 = individual(self.individual_size)
		child2 = individual(self.individual_size)
		for i in range(self.individual_size):
		 	if random.random()>=0.5:
				child1.genotype[i] = parent1.genotype[i]
				child2.genotype[i] = parent2.genotype[i]
			else:
				child1.genotype[i] = parent2.genotype[i]
				child2.genotype[i] = parent1.genotype[i]
		return child1,child2
	
	def mutate(self,child):
		index = random.randint(0,self.individual_size-1)
		mutation_val = 0.0
		if index == 0:
			mutation_val = 0.001
		else:
			mutation_val = 0.01
		child.genotype[index] += mutation_val
		if child.genotype[index] > 1.0:
			child.genotype[index]-=1.0
		return child
		
	def display(self):
		for individual in self.population:
			print colors.result + "individual default fitness"
			print individual.default_fitness
			print colors.result + "Individual Genotype"
			print individual.genotype
			print colors.result + "Individual Proteins"
			print individual.proteins
			print "\n"
		
	def run(self):
		for i in range(self.generations):
			print colors.header + "Generation #: " + str(i)
			self.genGen()
			print colors.header + "Generation Results"
			self.display()
		print colors.header + "Era Results"
		self.display()

if __name__ == '__main__':
	startime = timeit.default_timer()
	ga = GA()
	ga.run()
	stoptime = timeit.default_timer()
	print "Time to Compute: " + str(stoptime - startime) + " seconds"
