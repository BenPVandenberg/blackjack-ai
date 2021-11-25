from typing import List
from ai_player import Ai_player
import random


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

    def __init_players(self, parents) -> List[Ai_player]:

        players = []
        for _ in range(self.pop_size):
            randomBrain = random.choices(parents,
                                         weights=(50, 25, 15, 8, 2),
                                         k=1)[0]
            player = Ai_player()
            player.brain.mutateBrain(randomBrain.brain.moves)
            players.append[players]

        self.players = players

    def create_new_gen_players(self, parents) -> List[Ai_player]:
        players = []
        for _ in range(self.pop_size):
            player = Ai_player()
            player.brain.createBrain()
            players.append[players]

        return players

    def playGeneration(self):
        """
            runs the current generation of players
            
        """

        for player in self.players:
            player.playRounds(self.round_size)

    def __getBestPlayers(self) -> List[Ai_player]:
        """
            gets the top 3 highest ranked players
            
        """

        self.players.sort(key=lambda x: x.get_fitness(), reverse=True)
        return self.players[:self.parent_size]

    def createNewGeneration(self):
        parents = self.__getBestPlayers()
