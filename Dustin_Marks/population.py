import random
import copy
from ai_player import Ai_player


class Population:
    """
        blackjack Ai player population
    """
    POPULATION_SIZE = 50
    BJ_ROUNDS = 1000
    PARENT_SIZE = 5

    def __init__(self):
        self.generation = 0
        self.best_player = None
        self.players = self.__init_players()

    def __create_new_gen_players(self, parents: list[Ai_player]):

        players = []

        if self.best_player is None \
             or parents[0].total_winnings > self.best_player.total_winnings:

            self.best_player = copy.deepcopy(parents[0])

        for _ in range(self.POPULATION_SIZE):
            random_ai_player = random.choices(parents,
                                              weights=(50, 25, 15, 8, 2),
                                              k=1)[0]
            players.append(Ai_player(random_ai_player))

        parents[0].total_winnings = 0
        players.append(copy.deepcopy(parents[0]))

        return players

    def __init_players(self) -> list[Ai_player]:
        return [Ai_player() for _ in range(self.POPULATION_SIZE)]

    def play_generation(self):
        """
            runs the current generation of players
            
        """

        for player in self.players:
            player.play_rounds(self.BJ_ROUNDS)
            # print("player completed")

    def __get_best_players(self) -> list[Ai_player]:
        """
            gets the top 5 highest ranked players
            
        """

        self.players.sort(key=lambda x: x.get_fitness(), reverse=True)
        return self.players[:self.PARENT_SIZE]

    def create_new_generation(self):
        parents = self.__get_best_players()

        self.players = self.__create_new_gen_players(parents)

        self.generation += 1

        return self.best_player
