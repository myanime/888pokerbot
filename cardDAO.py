class CardDAO:
    
    def __init__(self, database):
        self.db = database
        self.hands = database.hands
    def insert_cards(self, cards):
        cards_on_table = {"card_1":cards}
        self.hands.insert_one(cards_on_table)
        return True
    def get_cards(self, hand=None):
        cursor = self.cards.find({}).limit(10)
        my_cards = []

        for card in cursor:
            my_cards.append({'color':card['color'], 'value':card['value'],
                             'suit':card['suit']})
        return my_cards
