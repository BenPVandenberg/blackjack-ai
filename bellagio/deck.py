import random
import random_api
from typing import Union


class Deck:
    """
        Class to manage the deck
    """

    def __init__(self, num_decks=1):
        self.cards = []
        self.__build(num_decks)

    def __repr__(self) -> str:
        return f"Deck of {len(self.cards)} cards"

    def __build(self, num_decks):
        """
            Builds the deck with (num_decks * 52) cards
            
            Args:
                num_decks: number of decks to build
        """

        one_deck = []

        for suit in Card.SUITS:
            for rank in range(1, 11):
                one_deck.append(Card(rank, suit))
            for face_card in Card.FACE_CARDS:
                one_deck.append(Card(face_card, suit))

        # multiple decks
        for _ in range(num_decks):
            self.cards.extend(one_deck)

    def shuffle(self):
        """
            Shuffles the deck
        """

        random.shuffle(self.cards)
        api_shuffle = random_api.shuffle(self.cards)
        self.cards = api_shuffle or self.cards

    def draw(self):
        """
            Draws a card from the deck

            Returns:
                Card: card drawn from the deck

            Raises:
                IndexError: if the deck is empty
        """

        if len(self.cards) == 0:
            raise IndexError("No cards left in deck")
        else:
            return self.cards.pop()


class Card:
    """
        Class to manage the individual cards
    """

    SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]
    FACE_CARDS = ["Jack", "Queen", "King"]

    def __init__(self, rank: Union[int, str], suit: str):
        self.suit = suit
        self.rank = rank

        if self.rank in ["Jack", "Queen", "King"]:
            self.value = 10
        else:
            self.value = int(self.rank)

    def __repr__(self):
        return str(self.rank) + " of " + self.suit

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit
