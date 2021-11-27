from brain import Brain


class Ai_player:
    """
        blackjack Ai player
    """

    def __init__(self, parent_player=None):
        self.brain = Brain(parent_player.brain)
        self.total_winnings = 0
        self.finished = False
        # self.__build(num_decks)

    def play_rounds(self, num_rounds):
        """
            plays the set number of blackjack rounds
            
            Args:
                num_rounds: number of rounds of blackjack played
        """

        for _ in range(num_rounds):
            self.__play_round()

        self.finished = True

    def __play_round(self):
        # do Blackjack things
        return "yay"

    def get_fitness(self):
        return self.total_winnings
