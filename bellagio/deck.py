import random


class Deck:

    def __init__(self, num_decks=1):
        self.cards = []
        self.__build(num_decks)

    def __repr__(self) -> str:
        return f"Deck of {len(self.cards)} cards"

    def __build(self, num_decks):
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
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) == 0:
            return None
        else:
            return self.cards.pop()


class Card:
    SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]
    FACE_CARDS = ["Jack", "Queen", "King"]

    def __init__(self, rank, suit):
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
