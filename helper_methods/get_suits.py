import numpy

def get_suits(all_cards, suit_box):
    suit = all_cards.crop(box=suit_box)
    suit_array = numpy.array(suit)
    suit_array_sum = suit_array.sum()
    if suit_array_sum < 100000:
        return None
    if suit_array_sum > 128000 and suit_array_sum < 135000:
        return 1#S
    if suit_array_sum > 135000 and suit_array_sum < 140000:
        return 4#C
    if suit_array_sum > 150000 and suit_array_sum < 155000:
        return 2#H
    if suit_array_sum > 160000 and suit_array_sum < 165000:
        return 3#D
    #suit.save("./images/suit.png")
