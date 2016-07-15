def get_hand(table_region):
    hand_array = []
    cards = get_area_screenshot(table_region, my_hand_x, my_hand_y, cards_box)
    cards.save("./images/myHand.png")
    card_boxes = [card_one_box_hand,card_two_box_hand]
    suit_boxes = [suit_one_box,suit_two_box]
    for suit_box, card_box in zip(suit_boxes,card_boxes):
        suit = get_suits(cards, suit_box)
        card = get_individual_cards(cards, card_box, number_box_dimension_x_hand, number_box_dimension_y_hand)
        if suit:
            hand_array.append((card, suit))
        if len(hand_array) > 0:
            insert_into_db(hand_array)
            return hand_array
        else:
            return "No Hand visible..."
