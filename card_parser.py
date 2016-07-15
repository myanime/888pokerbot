import os
print os.path
import pyautogui
import tesseract
from PIL import Image
from pytesseract import *
from selenium import webdriver
import StringIO
import time
import random
import numpy
import pymongo
from cardDAO import CardDAO
from pokerevalmod.card import Card
from pokerevalmod.hand_evaluator import HandEvaluator

from helper_methods.check_card import check_card
from helper_methods.get_hand_cards import get_hand_cards
from helper_methods.get_suits import get_suits
import traceback
import sys

#Database Connection
connection = pymongo.MongoClient("mongodb://localhost")
database = connection.poker
card_data = CardDAO(database)

#Table Window Dimenstions
table_dimensions_x = 800
table_dimensions_y = 570

#Cards relative to table window
cards_relative_top_x = 264
cards_relative_top_y = 173

#my_hand_x = 219
#my_hand_y = 347

#Distance Between Cards
dbc = 54 

#Card Box Dimensions
cards_box = (0,0,240,40)
card_number_box_dimension_x = 14#14
card_number_box_dimension_y = 21#21
card_one_box = (0,0,card_number_box_dimension_x,card_number_box_dimension_y)
card_two_box = (dbc*1,0,dbc*1+card_number_box_dimension_x,card_number_box_dimension_y)
card_three_box = (dbc*2,0,dbc*2+card_number_box_dimension_x,card_number_box_dimension_y)
card_four_box = (dbc*3,0,dbc*3+card_number_box_dimension_x,card_number_box_dimension_y)
card_five_box = (dbc*4,0,dbc*4+card_number_box_dimension_x,card_number_box_dimension_y)

'''
#Card Box Dimensions
cards_box_hand = (0,0,240,40)
card_number_box_dimension_x_hand = 15
card_number_box_dimension_y_hand = 20
card_one_box_hand = (0,0,card_number_box_dimension_x_hand,card_number_box_dimension_y_hand)
card_two_box_hand = (dbc*1,0,dbc*1+card_number_box_dimension_x_hand,card_number_box_dimension_y_hand)
'''

#Suit Box Dimensions
suits_box = (0,20,240,38)
suit_box_dimension_x = 16
suit_box_dimension_y = suits_box[1] + 16
suit_one_box = (0,suits_box[1],suit_box_dimension_x,suit_box_dimension_y)
suit_two_box = (dbc*1,suits_box[1],dbc*1+suit_box_dimension_x,suit_box_dimension_y)
suit_three_box = (dbc*2,suits_box[1],dbc*2+suit_box_dimension_x,suit_box_dimension_y)
suit_four_box = (dbc*3,suits_box[1],dbc*3+suit_box_dimension_x,suit_box_dimension_y)
suit_five_box = (dbc*4,suits_box[1],dbc*4+suit_box_dimension_x,suit_box_dimension_y)

def image_path(filename):
    return os.path.join('', filename)

def get_table_region():
    region = pyautogui.locateOnScreen(image_path('./images/poker_window.png'), region=(0,0,500,500))
    if region is None:
        raise Exception('Could not find game on screen. Is the game visible?')
    topLeftX = region[0] # left
    topLeftY = region[1] # top
    table_region = (topLeftX, topLeftY, topLeftX + table_dimensions_x, topLeftY + table_dimensions_y) # the game screen is always 800 x 570
    #print 'Table region found: {0}'.format(table_region)
    return table_region

def get_table_screenshot(table_region,cards_box,cards_relative_top_x,cards_relative_top_y):
    area = pyautogui.screenshot(region=(table_region[0]+ cards_relative_top_x,table_region[1]+cards_relative_top_y,cards_box[2],cards_box[3]))
    #area.save("./images/images/area.png")
    return area

def get_table_cards(all_cards, card_box, card_number_box_dimension_x, card_number_box_dimension_y):
    #To Black and White
    card = all_cards.crop(box=card_box).convert('1')
    #Strings images together - tesseract likes this better than single numbers
    merged_image = Image.new('RGB', (card_number_box_dimension_x*10,card_number_box_dimension_y))
    for i in range(0,card_number_box_dimension_x*10,card_number_box_dimension_x):
        merged_image.paste(card, (i,0))
    #merged_image.save("./images/images/inmergCard.png")
    value = image_to_string(merged_image)
    try:
        a = value[0]
        b = value[1]
        if a == '1' and b == '0':
            value = 10
        if a == '0':
            value = "Q"
        if a == 'T':
            value = 10 #red tens
        else:
            value = value[0]
        if value == "":
            value = None
    except:
        pass
    #card.save("./images/images/card{0}.png".format(value))
    if value == "J":
        value = 11
    if value == "Q":
        value = 12
    if value == "K":
        value = 13
    if value == "A":
        value = 14
    if value == "G":
        print "GGGGGGGGGGGGGGGGGGGGGGGGG"
        return None
    if value:
        return int(value)
    else:
        return None
def parse_cards(table_region):
    card_boxes = [card_one_box,card_two_box,card_three_box,card_four_box,card_five_box]
    suit_boxes = [suit_one_box,suit_two_box,suit_three_box,suit_four_box,suit_five_box]
    all_cards = get_table_screenshot(table_region,cards_box,cards_relative_top_x,cards_relative_top_y)
    cards_array = []
    for card_box,suit_box in zip(card_boxes,suit_boxes):
        all_cards = get_table_screenshot(table_region,cards_box,cards_relative_top_x,cards_relative_top_y)
        card = get_table_cards(all_cards, card_box, card_number_box_dimension_x, card_number_box_dimension_y)
        suit = get_suits(all_cards, suit_box)
        if card:
            cards_array.append((card,suit))
    return cards_array

def click_fold(region):
    fold_button = pyautogui.locateOnScreen(image_path('./images/fold_button.png'), region=region)
    if fold_button:
        #Wait a Little then click fold
        time.sleep(.5)
        x = fold_button[0] + 5
        y = fold_button[1] + 5
        #Click Fold
        pyautogui.click(x=x,y=y)
        #Close Helpful advise for idiots
        pyautogui.click(x=x+130,y=y-120)
        print "Fold"
        return True
    return False

def click_check(region):
    check_button = pyautogui.locateOnScreen(image_path('./images/check_button.png'), region=region)
    time.sleep(.5)
    if check_button:
        x = check_button[0] + 5
        y = check_button[1] + 5
        pyautogui.click(x=x,y=y)
        print "Check"
        return False
    return True

def click_call(region):
    call_button = pyautogui.locateOnScreen(image_path('./images/call_button.png'), region=region)
    time.sleep(.5)
    if click_call:
        time.sleep(.5)
        x = call_button[0] + 5
        y = call_button[1] + 5
        pyautogui.click(x=x,y=y)
        print "Call"
        return False
    return True

def insert_into_db(hand_array):
    card_data.insert_cards(hand_array)


def calculate_percentile(hand_tupple, table_array):
    if hand_tupple[0] == None:
        return 0
    try:
        card1, suit1 = table_array[0]
        card2, suit2 = table_array[1]
        card3, suit3 = table_array[2]
        card4, suit4 = table_array[3]
        card5, suit5 = table_array[4]
    except:
        pass
    hole = [Card(hand_tupple[0][0],hand_tupple[0][1]), Card(hand_tupple[1][0],hand_tupple[1][1])]
    if len(table_array) == 0:
        board = []
    if len(table_array) == 3:
        board = [Card(card1, suit1),Card(card2, suit2),Card(card3, suit3)]
    if len(table_array) == 4:
        board = [Card(card1, suit1),Card(card2, suit2),Card(card3, suit3),Card(card4, suit4)]
    if len(table_array) == 5:
        board = [Card(card1, suit1),Card(card2, suit2),Card(card3, suit3),Card(card4, suit4),Card(card5, suit5)]
    score = HandEvaluator.evaluate_hand(hole, board)
    return score

def parse_following(table_region):
    fold_button = pyautogui.locateOnScreen(image_path('./images/fold_button.png'), region=table_region)
    if fold_button:
        hand = get_hand_cards(table_region)
        table = parse_cards(table_region)
        print "Hand cards:", hand 
        print "Table cards:", table

        score = calculate_percentile(hand, table)
        print score
        if score > 0.5:
            if click_check(table_region):
                click_call(table_region)
        else:
            if click_check(table_region):
                click_fold(table_region)
    milis = random.randrange(3000,5000,1)
    print "Waiting", milis
    time.sleep(float(milis/1000))
def text_gui():
    print "=========================================="
    sys.stdout.write("Parsing")
    time.sleep(.2)
    sys.stdout.write(".")
    time.sleep(.2)
    sys.stdout.write(".")
    time.sleep(.2)
    sys.stdout.write(".")
    time.sleep(.2)
    print ""

def main():
    for x in range (0,1000):
        table_region = get_table_region()
        try:
            text_gui()
            parse_following(table_region)
        except:
            time.sleep(2)
            traceback.print_exc()
if __name__ == '__main__':
    main()
