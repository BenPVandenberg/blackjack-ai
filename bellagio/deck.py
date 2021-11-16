import random


class Deck:

    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in Card.SUITS:
            for rank in range(2, 11):
                self.cards.append(Card(suit, rank))
            for face_card in Card.FACE_CARDS:
                self.cards.append(Card(suit, face_card))

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

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return str(self.rank) + " of " + self.suit

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def get_value(self):
        if self.rank in ["Jack", "Queen", "King"]:
            return 10
        # Ace is 1 or 11
        elif self.rank == 1:
            return [1, 11]
        else:
            return int(self.rank)
