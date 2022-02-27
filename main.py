from enum import Enum
from typing import List, Tuple
from functools import reduce

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
        
    return None


def isValidTurn(prevTurn: List[Card], currentTurn: List[Card]) -> bool:
    if len(prevTurn) != len(currentTurn):
        return False

    if len(prevTurn) == 1 and len(currentTurn) == 1:
        return isValid1Card(prevTurn[0], currentTurn[0])

    if len(prevTurn) == 2 and len(currentTurn) == 2:
        return isValid2Card(prevTurn, currentTurn)

    if len(prevTurn) == 3 and len(currentTurn) == 3:
        return isValid2Card(prevTurn, currentTurn)
    
    return False

print(clasify5Card([Card(10, Suit.D), Card(11, Suit.D), Card(12, Suit.D), Card(13, Suit.D), Card(2, Suit.D)]))

