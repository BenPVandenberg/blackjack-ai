import random
from multiprocessing import Pool
from ai_player import Ai_player
from deck import Deck


class Population:
    """
        blackjack Ai player population
    """
    POPULATION_SIZE = 100
    BJ_ROUNDS = 100
    PARENT_SIZE = 5
    MAX_THREADS = 9  # most efficient

    def __init__(self):

        def __init_players():
            return [Ai_player() for _ in range(self.POPULATION_SIZE)]

        self.generation = 0
        self.best_player = None
        self.players = __init_players()
        self.__decks = []

    def create_new_generation(self):
        self.__create_new_gen_players()
        self.generation += 1

    def __create_new_gen_players(self):
        parents = self.__get_best_players(self.PARENT_SIZE)

        # an array of ai players that will make the next generation
        players_parents = random.choices(parents,
                                         weights=(50, 25, 15, 8, 2),
                                         k=(self.POPULATION_SIZE -
                                            self.PARENT_SIZE))

        self.players = [Ai_player(player) for player in players_parents]

        for i in range(self.PARENT_SIZE):
            self.players.append(parents[i])

    def __get_best_players(self, num) -> list[Ai_player]:
        """
            gets the top num highest ranked players
        """
        return self.players[:num]

    def play_generation(self):
        """
            runs the current generation of players
        """

        # generate the decks
        self.__decks = [Deck(6) for _ in range(self.BJ_ROUNDS)]
        # shuffle the decks
        for deck in self.__decks:
            deck.shuffle()

        with Pool(self.MAX_THREADS) as pool:
            players = pool.map(self.thread_worker, self.players)

        self.players = players

        # set the best player
        self.players.sort(key=lambda x: x.get_fitness(), reverse=True)
        self.best_player = self.players[0]

    def thread_worker(self, player: Ai_player):
        player.play_rounds(self.__decks)

        return player
