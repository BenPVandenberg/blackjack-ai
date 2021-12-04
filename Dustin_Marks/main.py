import time
import os
from Dustin_Marks.ai_player import Ai_player
from population import Population


class Main:
    """
        blackjack Ai player population
    """

    def __init__(self):
        self.population = Population()
        self.generation = 0
        self.current_best = None
        self.best_counter = 0
        self.best_max = 25

    def main(self):

        while True:
            # time how long it takes to run a gen
            start = time.time()

            #did it reach goal

            self.population.play_generation()

            if self.current_best is None:
                self.current_best = self.population.best_player

            end = time.time()
            if (self.best_counter != 0):
                print(f"best player unchanged in {self.best_counter} round(s)")
            print(f"Generation {self.generation} took: {end - start}")
            print(
                f"Current best: {self.population.best_player.total_profit}\n\n")

            if self.end_program(self.population.best_player):
                print(
                    f"AI has remained unchanged for {self.best_max} turns, best brain boi is",
                    self.population.best_player.brain)
                break

            # make a folder for each generation
            os.makedirs(f".\\gen_data\\{self.generation}")

            self.population.best_player.brain.to_html(
                f".\\gen_data\\{self.generation}\\top_brain.html")

            # write total profit to file
            with open(f".\\gen_data\\{self.generation}\\total_profit.txt",
                      "w") as f:
                f.write(str(self.population.best_player.total_profit))

            print("best brain boi", self.population.best_player.brain)

            self.population.create_new_generation()
            self.generation += 1

    def end_program(self, generation_best: Ai_player):
        if self.best_counter == self.best_max:
            return True

        if self.current_best == generation_best:
            self.best_counter += 1
        else:
            self.best_counter = 0

        self.current_best = generation_best
        return False


if __name__ == "__main__":
    main = Main()
    main.main()
