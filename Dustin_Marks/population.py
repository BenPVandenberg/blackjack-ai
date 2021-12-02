import random
import copy
from multiprocessing import Pool
from ai_player import Ai_player


class Population:
    """
        blackjack Ai player population
    """
    POPULATION_SIZE = 50
    PARENT_SIZE = 5
    MAX_THREADS = 9  # 9 is the most efficient

    def __init__(self):
        self.generation = 0
        self.best_player = None
        self.players = self.__init_players()

    def __create_new_gen_players(self, parents: list[Ai_player]):

        players = []

        if self.best_player is None \
             or parents[0].total_profit > self.best_player.total_profit:

            self.best_player = copy.deepcopy(parents[0])

        for _ in range(self.POPULATION_SIZE):
            random_ai_player = random.choices(parents,
                                              weights=(50, 25, 15, 8, 2),
                                              k=1)[0]
            players.append(Ai_player(random_ai_player))

        parents[0].total_profit = 0
        players.append(copy.deepcopy(parents[0]))

        return players

    def __init_players(self) -> list[Ai_player]:
        return [Ai_player() for _ in range(self.POPULATION_SIZE)]

    def play_generation(self):
        """
            runs the current generation of players
            
        """

        with Pool() as pool:
            players = pool.map(self.thread_worker, self.players)

        self.players = players

        self.players.sort(key=lambda x: x.get_fitness(), reverse=True)

        return (self.best_player or self.players[0], self.players[0])

    def thread_worker(self, player: Ai_player):
        player.play_rounds()

        return player

    def __get_best_players(self) -> list[Ai_player]:
        """
            gets the top 5 highest ranked players
            
        """

        self.players.sort(key=lambda x: x.get_fitness(), reverse=True)
        return self.players[:self.PARENT_SIZE]

    def create_new_generation(self) -> tuple[Ai_player, Ai_player]:
        parents = self.__get_best_players()

        self.players = self.__create_new_gen_players(parents)

        self.generation += 1

        return (self.best_player, self.players[0])
