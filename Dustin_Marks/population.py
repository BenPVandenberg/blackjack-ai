from ai_player import Ai_player


class Population:
    """
        blackjack Ai player population
    """

    def __init__(self):
        self.players = self.create_players()
        self.pop_size = 50
        self.round_size = 100
        # self.__build(num_decks)

    def create_players(self):
        players = []
        for _ in range(self.pop_size):
            player = Ai_player()
            player.brain.createBrain()
            players.append[players]

        return players

    def playGeneration(self, num_rounds):
        """
            plays the set number of blackjack rounds
            
            Args:
                num_rounds: number of rounds of blackjack played
        """

        for _ in range(num_rounds):
            self.__playRound()

        self.finished = True

    def __playRound(self):
        # do Blackjack things
        return "yay"

    def get_fitness(self):
        return self.total_winnings
