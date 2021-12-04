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
                                     int((amount * total_moves) / 100))
        counter = 0
        for p in range(20, 4, -1):
            if not str(p) in self.__moves['value_table'].keys():
                self.__moves['value_table'][str(p)] = {}
            for d in possible_cards:
                if amount == 100 or counter in to_randomize:
                    self.__moves['value_table'][str(p)][d] = random.choice(
                        possible_moves)
                counter += 1

        #pair_table
        total_moves = 10 * 10
        to_randomize = random.sample(range(total_moves),
                                     int((amount * total_moves) / 100))
        counter = 0
        for p in reversed(possible_cards):
            if not (p + '-' + p) in self.__moves['pair_table'].keys():
                self.__moves['pair_table'][p + '-' + p] = {}
            for d in possible_cards:
                if amount == 100 or counter in to_randomize:
                    self.__moves['pair_table'][p + '-' + p][d] = random.choice(
                        possible_pair_moves)
                counter += 1

        #ace_table
        total_moves = 8 * 10
        to_randomize = random.sample(range(total_moves),
                                     int((amount * total_moves) / 100))
        counter = 0
        for p in range(9, 1, -1):
            if not ('A-' + str(p)) in self.__moves['ace_table'].keys():
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
            return 'S'

        c0 = player_cards[0]
        c1 = player_cards[1]

        #case hand is a pair (use pair_table)
        if len(player_cards) == 2 and c0.rank == c1.rank:
            if c0.value == 1:
                return self.__moves['pair_table']['A-A'][d]
            elif c0.value >= 10:
                return self.__moves['pair_table']['T-T'][d]
            else:
                return self.__moves['pair_table'][str(c0.rank) + '-' +
                                                  str(c1.rank)][d]

        #case hand contains an ace (use ace_table)
        aces_count = len([c for c in player_cards if c.rank == 1])
        if len(player_cards) == 2 and aces_count == 1:
            if (c0.rank == 1):
                return self.__moves['aces_table']['A-' + str(c1.rank)][d]
            else:
                return self.__moves['aces_table']['A-' + str(c0.rank)][d]

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

    def bg_colour_col(self, col):
        colours = {'S': 'red', 'H': 'green', 'D': 'yellow', 'P': 'purple'}
        return ['background-color: %s' % colours[x] for _, x in col.iteritems()]

    def to_html(self, path: str):
        with open(path, 'w+') as outfile:
            outfile.write(
                pd.DataFrame(self.__moves['value_table']).T.style.apply(
                    self.bg_colour_col).render())
            outfile.write(
                pd.DataFrame(self.__moves['ace_table']).T.style.apply(
                    self.bg_colour_col).render())
            outfile.write(
                pd.DataFrame(self.__moves['pair_table']).T.style.apply(
                    self.bg_colour_col).render())

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Brain):
            if (self.__moves == other.__moves):
                return True
        return False