import random
from ai_player import Ai_player
from population import Population


class Main:
    """
        blackjack Ai player population
    """

    def __init__(self):
        self.population = Population()
        self.generation = 0
        self.current_best = None

    def main(self):

        while True:
            self.population.play_generation()

            #did it reach goal

            self.current_best = self.population.create_new_generation()

            self.generation += 1
            print("generation ", self.generation)


if __name__ == "__main__":
    main = Main()
    main.main()
