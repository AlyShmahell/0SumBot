from pygga import Genotype, Phenotype, Problem, Pretty, Oneliner, TimeLine
import os
import sys
import random
import fileinput
import subprocess
import numpy as np 


class PlanetWarsTimeLine(TimeLine):
    def synchronize(self):
        opponent         = random.choice(os.listdir("PlanetWars/opponents/build"))
        self.phenominons =  [ 
                                [
                                    random.choice(os.listdir("PlanetWars/maps")), 
                                    opponent
                                ]
                                for _ in range(3)
                            ]


class PlanetWarsProblem(Problem):

    def __setindividualsize__(self: 'Problem'):
        """
        sets self.individual_size for both PyGGA & Individual.
        """
        return 10

    def __setgenotype__(self: 'Problem'):
        """
        sets self.genotype for both PyGGA & Individual.
        """
        return Genotype(
                            functions = [
                                            random.uniform 
                                            for _ in range(self.individual_size)
                                        ],
                            ranges    = [
                                            (0.0, 1.0)
                                            for _ in range(self.individual_size)
                                        ]
                        )

    def __setphenotype__(self: 'Problem'):
        """
        sets self.phenotype for both PyGGA & Individual.
        """
        return Phenotype(
                            denormalizations   = [
                                                    1.0, 
                                                    300,
                                                    60, 
                                                    300, 
                                                    60, 
                                                    300, 
                                                    60, 
                                                    50, 
                                                    20, 
                                                    100
                                                 ]
                        )

    def fit(self, cls):
        values = np.array(cls.genome) * np.array(cls.phenotype["denormalizations"])
        def replace_line(file_, replacements):
            for pattern, newline in replacements:
                for line in fileinput.input(file_, inplace=True):
                    if pattern in line:
                        line = f"{newline}\n"
                    sys.stdout.write(line)
        replace_line(
            '0SumBots/v1/src/zeroSumBot.java',
            [
                [
                    'double oPWNumShipsProduction1 = ', 
                    f'    double oPWNumShipsProduction1 = {values[0]};'
                ],
                [
                    'int oPNumShips = ',                
                    f'    int oPNumShips = {int(values[1])};'
                ],
                [
                    'int oPGrowthRate = ',              
                    f'    int oPGrowthRate = {int(values[2])};'
                ],
                [
                    'int oENumShips = ',                
                    f'    int oENumShips = {int(values[3])};'
                ],
                [
                    'int oEGrowthRate = ',              
                    f'    int oEGrowthRate = {int(values[4])};'
                ],
                [
                    'int oNNumShips = ',                
                    f'    int oNNumShips = {int(values[5])};'
                ],
                [
                    'int oNGrowthRate = ',              
                    f'    int oNGrowthRate = {int(values[6])};'
                ],
                [
                    'int oDistance = ',                 
                    f'    int oDistance = {int(values[7])};'
                ],
                [
                    'int fleetDivider = ',              
                    f'    int fleetDivider = {int(values[8])};'
                ],
                [
                    'int oLocalMinima = ',              
                    f'    int oLocalMinima = {int(values[9])};'
                ]
            ]
        )
        fitness = 0.0
        for game_map, game_opponent in TimeLine().flow():
            os.system(Oneliner("""(cd 0SumBots/v1/src && make 2>&1 > /dev/null 
                                   && make clean 2>&1 > /dev/null)"""))
            result = subprocess.check_output(
                                                Oneliner(f"""java -jar PlanetWars/engine/build/PlayGame.jar 2>&1 
                                                             'PlanetWars/maps/{game_map}' 10000 10000 /dev/null
                                                             'java -jar PlanetWars/opponents/build/{game_opponent}' 
                                                             'java -jar 0SumBots/v1/build/0SumBot.jar' 
                                                             2>&1 >/dev/null | echo $(tail -1)"""), 
                                                shell=True
                                            )
            result = f"{result}"
            if 'Player 2 Wins!' in result:
                fitness += 1.0
            if 'Draw' in result:
                fitness += 0.5
        return fitness

    def mutate(self: 'Problem', cls: 'PyGGA', i: 'int'):
        index = random.randint(0, cls.individual_size-1)
        mutation = 0.0
        if index == 0:
            mutation = 0.001
        else:
            mutation = 0.01
        cls.children[i].genome[index] += mutation
        if cls.children[i].genome[index] > 1.0:
            cls.children[i].genome[index] -= 1.0
        return cls.children[i]
