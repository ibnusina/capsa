from enum import Enum
from typing import List, Tuple
from functools import reduce
from collections import Counter


class Rank(Enum):
    STRAIGHT = 1
    ROYAL_STRAIGHT = 2
    FLUSH = 3
    FULL_HOUSE = 4
    FOUR_A_KIND = 5
    STRAIGHT_FLUSH = 6
    ROYAL_STRAIGHT_FLUSH = 7

    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name


class Suit(Enum):
    D = 1 # diamond
    C = 2 # club
    H = 4 # heart
    S = 8 # spade

    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name


class Card:
    def __init__(self, score: int, suit: Suit):
        self.score = score
        self.suit = suit
        self.value = score if score > 2 else score + 13

    def __repr__(self):
        return f"{self.score}{self.suit}"

    def __eq__(self, other):
        return self.score == other.score and self.suit == other.suit

    def __gt__(self, other):
        return (self.value * 10 + self.suit.value) > (other.value * 10 + other.suit.value)

    def __lt__(self, other):
        return (self.value * 10 + self.suit.value) < (other.value * 10 + other.suit.value)


def isValid1Card(prevTurn: Card, currentTurn: Card) -> bool:
    return currentTurn > prevTurn


def isValid2Card(prevTurn: List[Card], currentTurn: List[Card]) -> bool:
    prevScores =  [card.score for card in prevTurn]
    currentScores = [card.score for card in currentTurn]

    if (currentScores[0] != (currentScores[0] | currentScores[1]) or
        prevScores[0] != prevScores[0] | prevScores[1]):
        return False
    
    return max(prevTurn) < max(currentTurn)


def isValid3Card(prevTurn: List[Card], currentTurn: List[Card]) -> bool:
    prevScores = [card.score for card in prevTurn]
    currentScores = [card.score for card in currentTurn]

    if (currentScores[0] != (currentScores[0] | currentScores[1] | currentScores [2]) or
        prevScores[0] != prevScores[0] | prevScores[1] | prevScores[2]):
        return False
    
    return max(prevTurn) < max(currentTurn)


def isFlush(turn: List[Card]):
    suits = reduce(lambda x, y: x | y, map(lambda card: card.suit.value, turn))
    return suits == turn[0].suit.value


def isStraightAndRoyal(turn: List[Card]) -> Tuple:
    order = "12345678910111213"
    royalOrder = "110111213"
    sortedCard = sorted(turn, key=lambda x: x.score)
    sortedTurn = ''.join(map(lambda x: str(x.score), sortedCard))
    
    if sortedTurn == royalOrder:
        return True, True, sortedCard[0]

    searchIndex = order.find(sortedTurn)
    if searchIndex != -1:
        return True, False, sortedCard[4]
    
    return False, False, None


def isFullHouseOrFourAKind(turn: List[Card]) -> Tuple:
    values = list(map(lambda x: x.value, turn))
    valuesSet = list(Counter(values).keys())
    valuesCount = list(Counter(values).values())
    maxCount = max(valuesCount)
    hightValue = valuesSet[valuesCount.index(maxCount)]
    hightCards = filter(lambda x: x.value == hightValue, turn)

    if len(valuesSet) == 2:
        if maxCount == 3:
            return Rank.FULL_HOUSE, max(hightCards)
        elif maxCount == 4:        
            return Rank.FOUR_A_KIND, max(hightCards)
    
    return None


def clasify5Card(turn: List[Card]) -> Tuple:
    straight, royal, highest = isStraightAndRoyal(turn)
    flush = isFlush(turn)

    if royal and straight and flush:
        return Rank.ROYAL_STRAIGHT_FLUSH, highest
    elif straight and flush:
        return Rank.STRAIGHT_FLUSH, highest
    elif royal and straight:
        return Rank.ROYAL_STRAIGHT, highest
    elif straight:
        return Rank.STRAIGHT, highest
    elif flush:
        return Rank.FLUSH, max(turn)
    else:
        return isFullHouseOrFourAKind(turn)


def isValid5Card(prevTurn: List[Card], currentTurn: List[Card]):
    prevRank, prevCard = clasify5Card(prevTurn)
    currentRank, currentCard = clasify5Card(currentTurn)

    if prevRank and prevCard and currentRank and currentCard:
        if currentRank.value > prevRank.value:
            return True
        elif currentRank.value == prevRank.value:
            return currentCard > prevCard
        else:
            return False
    else:
        return False


def isValidFirstTurn(turn: List[Card], enableTriple: bool=False) -> bool:
    if len(turn) == 1:
        return turn[0] == Card(3, Suit.D)
    elif len(turn) == 2:
        return Card(3, Suit.D) in turn and turn[0].score == 3 and turn[1].score == 3
    elif len(turn) == 3 and enableTriple:
        return Card(3, Suit.D) in turn and turn[0].score == 3 and turn[1].score == 3 and turn[2].score == 3
    elif len(turn) == 5:
        rank, _ = clasify5Card(turn)
        return Card(3, Suit.D) in turn and rank is not None


def isValidTurn(prevTurn: List[Card], currentTurn: List[Card], enableTriple: bool=False) -> bool:
    if (prevTurn is None or len(prevTurn) == 0) and len(currentTurn) > 0:
        return isValidFirstTurn(currentTurn, enableTriple)
    elif len(prevTurn) == 1 and len(currentTurn) == 1:
        return isValid1Card(prevTurn[0], currentTurn[0])
    elif len(prevTurn) == 2 and len(currentTurn) == 2:
        return isValid2Card(prevTurn, currentTurn)
    elif len(prevTurn) == 3 and len(currentTurn) == 3 and enableTriple:
        return isValid3Card(prevTurn, currentTurn)
    elif len(prevTurn) == 5 and len(currentTurn) == 5:
        return isValid5Card(prevTurn, currentTurn)
    elif len(prevTurn) == 1 and prevTurn[0].score == 2 and len(currentTurn) == 5:
        rank, _ = clasify5Card(currentTurn)
        return rank in [Rank.FOUR_A_KIND, Rank.STRAIGHT_FLUSH, Rank.ROYAL_STRAIGHT_FLUSH]

    return False


turn1 = [Card(1, Suit.D), Card(3, Suit.D), Card(4, Suit.S), Card(5, Suit.H), Card(2, Suit.D)]
turn2 = [Card(1, Suit.D), Card(1, Suit.H), Card(1, Suit.S), Card(5, Suit.H), Card(5, Suit.D)]
turn3 = [Card(1, Suit.D), Card(5, Suit.H), Card(5, Suit.S), Card(5, Suit.D), Card(5, Suit.C)]
turn4 = [Card(2, Suit.D)]
turn5 = [Card(3, Suit.D)]


print(isValidTurn(turn1, turn2))
print(isValidTurn(turn3, turn2))
print(isValidTurn(turn4, turn3))
print(isValidTurn(None, turn4))
print(isValidTurn(None, turn5))
print(isValidTurn(None, turn1))
print(isValidTurn(None, turn2))

