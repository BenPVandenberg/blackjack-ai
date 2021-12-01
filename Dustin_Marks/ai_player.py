from __future__ import annotations
from brain import Brain
from blackjack import Blackjack


class Ai_player:
    """
        blackjack Ai player
    """

    BET_AMOUNT = 100

    def __init__(self, parent_player: Ai_player = None):
        if parent_player is None:
            self.brain = Brain()
        else:
            self.brain = Brain(parent_player.brain)
        self.total_profit = 0
        self.finished = False
        # self.__build(num_decks)

    def play_rounds(self, num_rounds):
        """
            plays the set number of blackjack rounds
            
            Args:
                num_rounds: number of rounds of blackjack played
        """

        for _ in range(num_rounds):
            self.total_profit += self.__play_round()

        self.finished = True

    def __play_round(self):
        """
            Play 1 full game of blackjack

            Returns:
                int: total winnings from the round
        """

        game = Blackjack()

        state = game.start([self.BET_AMOUNT])

        while state['current_hand'] != -1:

            current_hand = state["player_hands"][state['current_hand']]
            move = self.brain.get_move(current_hand, state["dealer_hand"][0])

            if move == 'H':
                state = game.hit()
            elif move == 'S':
                state = game.stand()
            elif move == 'D':
                state = game.double()
            elif move == 'P':
                state = game.split()

        return game.end()["total_profit"]

    def get_fitness(self):
        return self.total_profit
