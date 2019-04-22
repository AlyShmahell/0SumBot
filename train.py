from zeroSumGA import PlanetWarsProblem, PlanetWarsTimeLine
from pygga import PyGGA
from build import zeroSumBuilder
from argparse import ArgumentParser


class zeroSumGaParser(object):
    def __new__(self):
        argparser = ArgumentParser()
        argparser.add_argument('-generations', default=10, type=int)
        argparser.add_argument('-population_size', default=10, type=int)
        argparser.add_argument('-tournament_size', default=2, type=int)
        argparser.add_argument('-elitism_percentage', default=10.0, type=float)
        argparser.add_argument('-crossover_probability', default=1.0, type=float)
        argparser.add_argument('-mutation_probability', default=0.5, type=float)
        args = argparser.parse_args()
        return args


if __name__ == '__main__':
    zeroSumBuilder()
    args = zeroSumGaParser()
    pygga = PyGGA(problem = PlanetWarsProblem(),
                  generations=args.generations,
                  population_size=args.population_size,
                  tournament_size=args.tournament_size,
                  elitism_percentage=args.elitism_percentage,
                  crossover_probability=args.crossover_probability,
                  mutation_probability=args.mutation_probability,
                  timeline = PlanetWarsTimeLine)
    optimus = pygga()
    optimus()
    print(f"{optimus}")
