from deck import Deck, Card


class Blackjack:
    __DEALER_HAND_ID = -1
    __DEALER_HIT_THRESHOLD = 17

    def __init__(self):
        self.bets = None
        self.deck = None
        self.player_hands = None
        self.current_hand = None
        self.dealer_hand = None

    def start(self, bets: list[int]):
        # Initialize the deck
        deck = Deck()
        deck.shuffle()

        # init the player's hands
        player_hands = [[] for _ in bets]
        # Deal the cards
        dealer_hand = []
        for _ in range(2):
            for i in range(len(bets)):
                player_hands[i].append(deck.draw())
            dealer_hand.append(deck.draw())

        self.bets = bets
        self.deck = deck
        self.player_hands = player_hands
        self.current_hand = 0
        self.dealer_hand = dealer_hand

        return self.__return_state("Game started")

    def hit(self):
        current_hand = self.player_hands[self.current_hand]
        current_hand.append(self.deck.draw())
        message = "Hit Success"

        if min(self.get_hand_value(current_hand)) > 21:
            self.__next_hand()
            message = "Bust"

        return self.__return_state(message)

    def stand(self):
        self.__next_hand()

        return self.__return_state("Stand Success")

    def __next_hand(self):
        if (self.current_hand + 1) == len(self.bets):
            # if no more hands left, return the dealer's hand
            self.current_hand = self.__DEALER_HAND_ID
        else:
            self.current_hand += 1

    def get_state(self):
        return self.__return_state("Get state request")

    def __return_state(self, message=None):
        return {
            "message": message,
            "player_hands": self.player_hands,
            "current_hand": self.current_hand,
            "dealer_hand": self.dealer_hand
        }

    @staticmethod
    def get_hand_value(hand: list[Card]) -> list[int]:
        """
            Returns all the possible value(s) of the hand

            Args:
                hand: list of Card objects

            Returns:
                list of possible values
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


if __name__ == "__main__":

    game = Blackjack()

    game.start([100, 100])
