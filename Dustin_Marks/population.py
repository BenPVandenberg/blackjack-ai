import random
from ai_player import Ai_player


class Population:
    """
        blackjack Ai player population
    """

    def __init__(self):
        self.players = self.__init_players()
        self.pop_size = 50
        self.round_size = 100
        self.parent_size = 5
        self.generation = 0

    def create_new_gen_players(self, parents):

        players = []
        for _ in range(self.pop_size):
            random_ai_player = random.choices(parents,
                                              weights=(50, 25, 15, 8, 2),
                                              k=1)[0]
            players.append[Ai_player(random_ai_player)]

        return players

    def __init_players(self) -> list[Ai_player]:
        players = []
        for _ in range(self.pop_size):
            players.append[Ai_player()]

        return players

    def play_generation(self):
        """
            runs the current generation of players
            
        """

        for player in self.players:
            player.play_rounds(self.round_size)

    def __get_best_players(self) -> list[Ai_player]:
        """
            gets the top 3 highest ranked players
            
        """

        self.players.sort(key=lambda x: x.get_fitness(), reverse=True)
        return self.players[:self.parent_size]

    def create_new_generation(self):
        parents = self.__get_best_players()
