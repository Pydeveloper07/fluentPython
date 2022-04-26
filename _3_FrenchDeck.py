import collections
import random

Card = collections.namedtuple("Card", ["rank", "suit"])


class FrenchDeck:
    ranks = [str(i) for i in range(2, 11)] + list("JKQA")
    suits = "spades diamonds hearts clubs".split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, item):
        return self._cards[item]


deck = FrenchDeck()

# print(len(deck))
#
# print(random.choice(deck))

# print(Card("3", "spades") in deck)
# print(Card("11", "clubs") in deck)

suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]


for card in sorted(deck, key=spades_high):
    print(card)