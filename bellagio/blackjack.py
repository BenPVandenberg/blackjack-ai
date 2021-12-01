"""
    A blackjack game, played only by python api.

    Ben Vandenberg, 2021
"""

from typing import Any
from deck import Deck, Card


class Blackjack:
    """
        A blackjack game as an object
    """

    NUMBER_OF_DECKS = 6
    HIGHEST_VALUE = 21
    __DEALER_HAND_ID = -1
    __DEALER_HIT_THRESHOLD = 17

    def __init__(self):
        self.__bets = None
        self.__deck = None
        self.__player_hands = None
        self.__current_hand = None
        self.__dealer_hand = None
        self.__game_over = True
        self.__final_state = None

    def start(self, bets: list[int]) -> dict[str, Any]:
        """
            Starts a new game

            Args:
                bets: A list of bets for each hand

            Returns:
                A dict containing the state of the game
        """

        # Initialize the deck
        deck = Deck(self.NUMBER_OF_DECKS)
        deck.shuffle()

        # init the player's hands
        player_hands = [[] for _ in bets]
        # Deal the cards
        dealer_hand = []
        for _ in range(2):
            for i in range(len(bets)):
                player_hands[i].append(deck.draw())
            dealer_hand.append(deck.draw())

        self.__bets = bets
        self.__deck = deck
        self.__player_hands = player_hands
        self.__current_hand = 0
        self.__dealer_hand = dealer_hand
        self.__game_over = False
        self.__final_state = None

        return self.__return_state("Game started")

    def hit(self):
        """
            Draws a card from the deck and adds it to the current hand

            Returns:
                A dict containing the state of the game
        """

        if self.__game_over:
            return self.__return_state("Game over")
        if not self.__is_users_turn():
            return self.__return_state("Not your turn")

        current_hand = self.__player_hands[self.__current_hand]
        current_hand.append(self.__deck.draw())
        message = "Hit success"

        if min(self.get_all_hand_values(current_hand)) > self.HIGHEST_VALUE:
            self.__next_hand()
            message = "Bust"

        return self.__return_state(message)

    def stand(self):
        """
            Stands the current hand

            Returns:
                A dict containing the state of the game
        """

        if self.__game_over:
            return self.__return_state("Game over")
        if not self.__is_users_turn():
            return self.__return_state("Not your turn")

        self.__next_hand()

        return self.__return_state("Stand success")

    def split(self):
        """
            Splits the current hand into two hands

            Returns:
                A dict containing the state of the game
        """

        if self.__game_over:
            return self.__return_state("Game over")

        if not self.__is_users_turn():
            return self.__return_state("Not your turn")

        current_hand = self.__player_hands[self.__current_hand]
        if len(current_hand) != 2:
            return self.__return_state("Can't split more than 2 cards")

        if current_hand[0].rank != current_hand[1].rank:
            return self.__return_state("Can't split cards that are different")

        # Split the hand
        card_to_move = current_hand.pop()
        current_hand.append(self.__deck.draw())

        # Add the new hand + bet
        self.__player_hands.append([card_to_move, self.__deck.draw()])
        self.__bets.append(self.__bets[self.__current_hand])

        return self.__return_state("Split success")

    def double(self):
        """
            Doubles the bet on the current hand

            Returns:
                A dict containing the state of the game
        """

        if self.__game_over:
            return self.__return_state("Game over")

        if not self.__is_users_turn():
            return self.__return_state("Not your turn")

        current_hand = self.__player_hands[self.__current_hand]
        if len(current_hand) != 2:
            # Can't double if there are more than 2 cards
            # preform a hit instead
            return self.hit()

        # double the bet
        self.__bets[self.__current_hand] *= 2

        # hit
        state = self.hit()

        # if successful, stand
        if state["message"] == "Hit success":
            self.__next_hand()
            return self.__return_state("Double success")

        return state

    def __is_users_turn(self):
        """
            Checks if it is the user's turn

            Returns:
                True if it is the user's turn, False otherwise
        """
        return self.__current_hand != self.__DEALER_HAND_ID

    def __next_hand(self):
        """
            Moves to the next hand
        """

        if (self.__current_hand + 1) == len(self.__bets):
            # if no more hands left, return the dealer's hand
            self.__current_hand = self.__DEALER_HAND_ID
        else:
            self.__current_hand += 1

    def end(self):
        """
            Ends the game and returns the results

            Returns:
                A dict containing the state and results of the game

            Examples:
                >>> game = Blackjack([100]).start()
                >>> game.end()
                {
                    'message': 'Game over',
                    'current_hand': -1,
                    'player_hands': [[1 of Clubs, 5 of Spades]],
                    'dealer_hand': [5 of Diamonds, 1 of Hearts, 3 of Clubs],
                    'results': [
                        {
                            'hand_id': 0,
                            'player_win': False,
                            'reason': 'Dealer beat Player',
                            'winnings': -100
                        }
                    ],
                    'total_winnings': -100,
                    'wins': 0,
                    'losses': 1,
                    'win_percentage': 0.0
                }
        """

        self.__game_over = True
        self.__current_hand = self.__DEALER_HAND_ID
        output = self.__return_state("Game over")
        output["results"] = []

        dealer_score = self.__run_dealer()
        total_winnings = 0
        wins = 0
        losses = 0

        # For each hand, compare the scores and update the statistics
        for i, hand in enumerate(self.__player_hands):
            player_score = self.get_playing_value(hand)

            if player_score > self.HIGHEST_VALUE:
                output["results"].append({
                    "hand_id": i,
                    "player_win": False,
                    "reason": "Player Bust",
                    "winnings": -self.__bets[i],
                })
                total_winnings -= self.__bets[i]
                losses += 1
                continue

            if dealer_score > self.HIGHEST_VALUE:
                output["results"].append({
                    "hand_id": i,
                    "player_win": True,
                    "reason": "Dealer Bust",
                    "winnings": self.__bets[i] * 2,
                })
                total_winnings += self.__bets[i] * 2
                wins += 1
                continue

            if player_score <= dealer_score:
                output["results"].append({
                    "hand_id": i,
                    "player_win": False,
                    "reason": "Dealer beat Player",
                    "winnings": -self.__bets[i],
                })
                total_winnings -= self.__bets[i]
                losses += 1
                continue

            if player_score > dealer_score:
                output["results"].append({
                    "hand_id": i,
                    "player_win": True,
                    "reason": "Player beat Dealer",
                    "winnings": self.__bets[i] * 2,
                })
                total_winnings += self.__bets[i] * 2
                wins += 1
                continue

            # if no conditions are met, an unknown error has occurred
            raise Exception("Unknown Error")

        output["total_winnings"] = total_winnings
        output["wins"] = wins
        output["losses"] = losses
        output["win_percentage"] = wins / (wins + losses)

        self.__final_state = output

        return output

    def __run_dealer(self):
        """
            Runs the dealer's hand

            Returns:
                The dealer's score
        """

        dealer_hand = self.__dealer_hand

        while min(self.get_all_hand_values(
                dealer_hand)) < self.__DEALER_HIT_THRESHOLD:

            playing_score = self.get_playing_value(dealer_hand)

            if playing_score >= self.__DEALER_HIT_THRESHOLD:
                return playing_score

            dealer_hand.append(self.__deck.draw())

        return min(self.get_all_hand_values(dealer_hand))

    def get_state(self):
        """
            Allows for the user to request the state of the game

            Returns:
                A dict containing the state of the game

            Examples:
                >>> game = Blackjack([100]).start()
                >>> game.get_state()
                {
                    "message": "State request",
                    "current_hand": 0,
                    "player_hands": [
                        [
                            8 of Diamonds,
                            2 of Spades
                        ]
                    ],
                    "dealer_hand": [
                        8 of Hearts
                    ]
                }
        """
        return self.__return_state("State request")

    def __return_state(self, message: str = None):
        """
            Compiles a dict containing the state of the game

            Returns:
                A dict containing the state of the game
        """

        # if the game is over and final state is computed, always return it
        if self.__final_state is not None:
            return self.__final_state

        dealer_hand = self.__dealer_hand[:1] if not self.__game_over else self.__dealer_hand

        return {
            "message": message,
            "current_hand": self.__current_hand,
            "player_hands": self.__player_hands,
            "dealer_hand": dealer_hand,
        }

    @staticmethod
    def get_all_hand_values(hand: list[Card]) -> list[int]:
        """
            Returns all the possible value(s) of the hand

            Args:
                hand: list of Card objects

            Returns:
                list of possible values

            Examples:
                >>> get_all_hand_values([Card(10, "Diamonds"), Card(2, "Diamonds")])
                [12]

                >>> get_all_hand_values([Card(1, "Spades"), Card(5, "Spades")])
                [6, 16]

                >>> get_all_hand_values([Card(1, "Spades"), Card(1, "Hearts")])
                [2, 12, 22]
        """

        # get all possible hand values given ace as 1 or 11
        init_count = sum(card.value for card in hand)
        aces = [card.value for card in hand if card.value == 1]
        if not aces:
            return [init_count]

        rtn = [init_count]
        for i, _ in enumerate(aces):
            rtn.append(init_count + (10 * (i + 1)))

        return rtn

    @classmethod
    def get_playing_value(cls, hand: list[Card]) -> int:
        """
            Returns the playing value of the hand, i.e. the highest possible value <= 21

            Args:
                hand: list of Card objects

            Returns:
                Playing value of the hand

            Examples:
                >>> get_playing_value([Card(10, "Diamonds"), Card(2, "Diamonds")])
                12

                >>> get_playing_value([Card(1, "Spades"), Card(5, "Spades")])
                16

                >>> get_playing_value([Card(1, "Spades"), Card(1, "Hearts")])
                12

                >>> get_playing_value([Card(1, "Spades"), Card(10, "Hearts"), Card(10, "Diamonds"), Card(10, "Spades")])
                31
        """

        hand_values = cls.get_all_hand_values(hand)

        eligible_values = [v for v in hand_values if v <= cls.HIGHEST_VALUE]

        if not eligible_values:
            return min(hand_values)

        return max(eligible_values)


if __name__ == "__main__":
    game = Blackjack()

    print(game.start([100] * 10))

    for _ in range(10):
        state = game.double()

    print(game.end())
