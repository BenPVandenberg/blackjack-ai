import time
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
            # time how long it takes to run a gen
            start = time.time()

            self.population.play_generation()

            #did it reach goal

            self.current_best = self.population.create_new_generation()

            end = time.time()
            print(f"Generation {self.generation} took: {end - start}")
            print(f"Current best: {self.current_best.total_profit}\n\n")

            self.generation += 1

            if self.generation == 100:
                print("best brain boi", self.current_best.brain)
                break


if __name__ == "__main__":
    main = Main()
    main.main()
