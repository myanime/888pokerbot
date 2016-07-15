def get_cards(table_region):
    cards_array = []
    cards = get_area_screenshot(table_region, cards_x, cards_y, cards_box)

    card_boxes = [card_one_box,card_two_box,card_three_box,card_four_box,card_five_box]
    suit_boxes = [suit_one_box,suit_two_box,suit_three_box,suit_four_box,suit_five_box]
    for suit_box, card_box in zip(suit_boxes,card_boxes):
        suit = get_suits(cards, suit_box)
        if suit:
            card = get_individual_cards(cards,card_box,number_box_dimension_x, number_box_dimension_y)
            cards_array.append((card, suit))
    if len(cards_array) > 0:
        insert_into_db(cards_array)
        return cards_array
    else:
        return "No cards on table Visible..."
