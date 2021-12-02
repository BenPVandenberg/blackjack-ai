import time
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
        self.best_max = 2

    def main(self):

        while True:
            # time how long it takes to run a gen
            start = time.time()

            #did it reach goal

            (generation_best, attempt) = self.population.play_generation()

            if self.current_best is None:
                self.current_best = generation_best

            end = time.time()
            print(f"Generation {self.generation} took: {end - start}")
            print(
                f"Current best: {generation_best.total_profit}, attempt: {attempt.total_profit}\n\n"
            )

            self.population.create_new_generation()
            self.generation += 1

            if self.end_program(generation_best):
                print(
                    f"AI has remained unchanged for {self.best_max} turns, best brain boi is",
                    generation_best.brain)
                break

            if (self.generation % 100) == 0:
                print("best brain boi", generation_best.brain)

    def end_program(self, generation_best: Ai_player):
        if self.best_counter == self.best_max:
            return True

        if self.current_best.total_profit == generation_best.total_profit:
            self.best_counter += 1

        self.current_best = generation_best
        return False


if __name__ == "__main__":
    main = Main()
    main.main()
