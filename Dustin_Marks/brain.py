import copy
import random
import pandas as pd
from blackjack import Blackjack

class Brain:
    """
        Brain Object
    """

    def __init__(self, parentBrain=None):
        """
            If parent is passed in, copy that and mutate - otherwise randomize.
        """
        self._mutation_value = 10

        #make a deep copy and mutate if parent passed in
        if parentBrain is not None:
            self._moves = copy.deepcopy(parentBrain._moves)
            self.mutate()
        else:
            self._init_move_tables()
            self.randomize()

    def _init_move_tables(self):
        """
            Read table as moves['table_name']['my_score']['dealer_score']
        """
        #initialize high-level dicts
        self._moves = {
            'value_table' : {},
            'ace_table' : {},
            'pair_table' : {}
        }

    def mutate(self):
        """
            Mutates by randomizing certain percentage of moves
        """
        self.randomize(self._mutation_value)

    def randomize(self, amount=100):
        """
            Randomize <amount> % of moves
        """
        possible_moves = ['H','S','D','P']
        possible_cards = ['2','3','4','5','6','7','8','9','T','A']
        
        #value_table
        total_moves = 16*10
        to_randomize = random.sample(range(total_moves), amount//100*total_moves)
        counter = 0
        for p in range(20, 4, -1):
            self._moves['value_table'][str(p)] = {}
            for d in possible_cards:
                if amount == 100 or counter in to_randomize:
                    self._moves['value_table'][str(p)][d] = random.choice(possible_moves)
                counter += 1

        #ace_table
        total_moves = 8*10
        to_randomize = random.sample(range(total_moves), amount//100*total_moves)
        counter = 0
        for p in reversed(possible_cards):
            self._moves['ace_table'][p+'-'+p] = {}
            for d in possible_cards:
                if amount == 100 or counter in to_randomize:
                    self._moves['ace_table'][p+'-'+p][d] = random.choice(possible_moves)
                counter += 1
        
        #pair_table
        total_moves = 10*10
        to_randomize = random.sample(range(total_moves), amount//100*total_moves)
        counter = 0
        for p in range(9, 1, -1):
            self._moves['pair_table']['A-'+str(p)] = {}
            for d in possible_cards:
                if amount == 100 or counter in to_randomize:
                    self._moves['pair_table']['A-'+str(p)][d] = random.choice(possible_moves)
                counter += 1

    def get_move(self, player_cards, dealer_card):
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
        aces_count = len([c for c in player_cards if c.rank == 1])
        
        #pair_table
        if len(player_cards) == 2 and player_cards[0].value == player_cards[1].value:
            return self._moves['pair_table'][str(player_cards[0].value)+'-'+str(player_cards[0].value)][d]
        #aces_table
        if len(player_cards) == 2 and aces_count == 1:
            if (player_cards[0].value == 1):
                return self._moves['aces_table']['A-'+str(player_cards[1].value)][d]
            else:
                return self._moves['aces_table']['A-'+str(player_cards[0].value)][d]
        #value_table
        return self._moves['value_table'][str(player_score)][d]

    def __str__(self):
        output = 'value_table\n\n'
        output += pd.DataFrame(self._moves['value_table']).T.to_string()

        output += '\n\nace_table\n\n'
        output += pd.DataFrame(self._moves['ace_table']).T.to_string()

        output += '\n\npair_table\n\n'
        output += pd.DataFrame(self._moves['pair_table']).T.to_string()
        return output
