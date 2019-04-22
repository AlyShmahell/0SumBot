import os
from pygga import Oneliner
from build import zeroSumBuilder

if __name__ == '__main__':
    zeroSumBuilder()
    os.system(
                Oneliner("""
                            java -jar PlanetWars/engine/build/PlayGame.jar 
                            "maps/map100.txt" 10000 10000 /dev/null 
                            "java -jar PlanetWars/opponents/build/Genebot.jar" 
                            "java -jar 0SumBots/v2/build/0SumBot.jar" 
                            | java -jar PlanetWars/engine/build/ShowGame.jar""")
             )
