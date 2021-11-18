from deck import Deck, Card


class Blackjack:
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

    def start(self, bets: list[int]):
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

        return self.__return_state("Game started")

    def split(self):
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

    def hit(self):
        if not self.__is_users_turn():
            return self.__return_state("Not your turn")

        current_hand = self.__player_hands[self.__current_hand]
        current_hand.append(self.__deck.draw())
        message = "Hit Success"

        if min(self.get_all_hand_values(current_hand)) > self.HIGHEST_VALUE:
            self.__next_hand()
            message = "Bust"

        return self.__return_state(message)

    def stand(self):
        if not self.__is_users_turn():
            return self.__return_state("Not your turn")

        self.__next_hand()

        return self.__return_state("Stand success")

    def __is_users_turn(self):
        return self.__current_hand != self.__DEALER_HAND_ID

    def __next_hand(self):
        if (self.__current_hand + 1) == len(self.__bets):
            # if no more hands left, return the dealer's hand
            self.__current_hand = self.__DEALER_HAND_ID
        else:
            self.__current_hand += 1

    def end_turn(self):
        self.__game_over = True
        self.__current_hand = self.__DEALER_HAND_ID
        output = self.__return_state("Game over")
        output["results"] = []

        dealer_score = self.__run_dealer()
        total_winnings = 0

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
                continue

            if dealer_score > self.HIGHEST_VALUE:
                output["results"].append({
                    "hand_id": i,
                    "player_win": True,
                    "reason": "Dealer Bust",
                    "winnings": self.__bets[i] * 2,
                })
                total_winnings += self.__bets[i] * 2
                continue

            if player_score > dealer_score:
                output["results"].append({
                    "hand_id": i,
                    "player_win": True,
                    "reason": "Player beat Dealer",
                    "winnings": self.__bets[i] * 2,
                })
                total_winnings += self.__bets[i] * 2
                continue

            if player_score < dealer_score:
                output["results"].append({
                    "hand_id": i,
                    "player_win": False,
                    "reason": "Dealer beat Player",
                    "winnings": -self.__bets[i],
                })
                total_winnings -= self.__bets[i]
                continue

        output["total_winnings"] = total_winnings

        return output

    def __run_dealer(self):
        dealer_hand = self.__dealer_hand

        while min(self.get_all_hand_values(
                dealer_hand)) < self.__DEALER_HIT_THRESHOLD:

            playing_score = self.get_playing_value(dealer_hand)

            if playing_score > self.__DEALER_HIT_THRESHOLD:
                return playing_score

            dealer_hand.append(self.__deck.draw())

        return min(self.get_all_hand_values(dealer_hand))

    def get_state(self):
        return self.__return_state("State request")

    def __return_state(self, message=None):
        dealer_hand = self.__dealer_hand[:1] if not self.__game_over else self.__dealer_hand

        return {
            "message": message,
            "player_hands": self.__player_hands,
            "current_hand": self.__current_hand,
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
        hand_values = cls.get_all_hand_values(hand)

        eligible_values = [v for v in hand_values if v <= cls.HIGHEST_VALUE]

        if not eligible_values:
            return min(hand_values)

        return max(eligible_values)


if __name__ == "__main__":

    game = Blackjack()

    print(game.start([100, 100]))
    game.split()
    game.stand()
    game.split()
    print(game.end_turn())
