'''
from hand_evaluator import HandEvaluator
from card import Card

'''
from pokereval.hand_evaluator import HandEvaluator
from pokereval.card import Card

myCard = Card(13,'s')
myCard2 = Card(14,'s')
hand = HandEvaluator.Two()

print hand.evaluate_percentile([myCard, myCard2])
