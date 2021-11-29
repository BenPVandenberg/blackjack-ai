from __future__ import annotations
import copy
import random
import pandas as pd
from blackjack import Blackjack
from deck import Card


class Brain:
    """
        Brain Object
    """

    MUTATION_VALUE = 10

    def __init__(self, parent_brain: Brain = None):
        """
            If parent is passed in, copy that and mutate - otherwise randomize.
        """

        #make a deep copy and mutate if parent passed in
        if parent_brain is not None:
            self.__moves = copy.deepcopy(parent_brain.__moves)
            self.mutate()
        else:
            self.__init_move_tables()
            self.randomize()

    def __init_move_tables(self):
        """
            Read table as moves['table_name']['my_score']['dealer_score']
        """
        #initialize high-level dicts
        self.__moves = {'value_table': {}, 'ace_table': {}, 'pair_table': {}}

    def mutate(self):
        """
            Mutates by randomizing certain percentage of moves
        """
        self.randomize(self.MUTATION_VALUE)

    def randomize(self, amount: int = 100):
        """
            Randomize <amount> % of moves
        """
        possible_moves = ['H', 'S', 'D']
        possible_pair_moves = ['H', 'S', 'D', 'P']
        possible_cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'A']

        #value_table
        total_moves = 16 * 10
        to_randomize = random.sample(range(total_moves),
                                     amount // 100 * total_moves)
        counter = 0
        for p in range(20, 4, -1):
            self.__moves['value_table'][str(p)] = {}
            for d in possible_cards:
                if amount == 100 or counter in to_randomize:
                    self.__moves['value_table'][str(p)][d] = random.choice(
                        possible_moves)
                counter += 1

        #pair_table
        total_moves = 8 * 10
        to_randomize = random.sample(range(total_moves),
                                     amount // 100 * total_moves)
        counter = 0
        for p in reversed(possible_cards):
            self.__moves['pair_table'][p + '-' + p] = {}
            for d in possible_cards:
                if amount == 100 or counter in to_randomize:
                    self.__moves['pair_table'][p + '-' + p][d] = random.choice(
                        possible_pair_moves)
                counter += 1

        #ace_table
        total_moves = 10 * 10
        to_randomize = random.sample(range(total_moves),
                                     amount // 100 * total_moves)
        counter = 0
        for p in range(9, 1, -1):
            self.__moves['ace_table']['A-' + str(p)] = {}
            for d in possible_cards:
                if amount == 100 or counter in to_randomize:
                    self.__moves['ace_table']['A-' + str(p)][d] = random.choice(
                        possible_moves)
                counter += 1

    def get_move(self, player_cards: list[Card], dealer_card: Card):
        """
            Given player cards and visible dealer card, find move this brain chooses
        """
        #parse dealer card for dictionary lookup
        if dealer_card.value == 1:
            d = 'A'
        elif dealer_card.value >= 10:
            d = 'T'
        else:
            d = str(dealer_card.value)

        #parse player cards for dictionary lookup
        player_score = Blackjack.get_playing_value(player_cards)
        if player_score == 21:
            return 'H'

        c1 = player_cards[0].value
        c2 = player_cards[1].value
        if len(player_cards) == 2 and c1 == c2 and c1 >= 10:
            c1 = 'T'
            c2 = 'T'

        elif len(player_cards) == 2 and player_cards[0].rank == player_cards[
                1].rank and c1 == 1:
            c1 = 'A'
            c2 = 'A'

        aces_count = len([c for c in player_cards if c.rank == 1])

        #pair_table
        if len(player_cards) == 2 and c1 == c2:
            return self.__moves['pair_table'][str(c1) + '-' + str(c1)][d]
        #aces_table
        if len(player_cards) == 2 and aces_count == 1:
            if (c1 == 1):
                return self.__moves['aces_table']['A-' + str(c2)][d]
            else:
                return self.__moves['aces_table']['A-' + str(c1)][d]
        #value_table
        return self.__moves['value_table'][str(player_score)][d]

    def __str__(self):
        output = 'value_table\n\n'
        output += pd.DataFrame(self.__moves['value_table']).T.to_string()

        output += '\n\nace_table\n\n'
        output += pd.DataFrame(self.__moves['ace_table']).T.to_string()

        output += '\n\npair_table\n\n'
        output += pd.DataFrame(self.__moves['pair_table']).T.to_string()
        return output
