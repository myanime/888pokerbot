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

from helper_methods.check_card import check_card
from helper_methods.get_hand_cards import get_hand_cards

#Database Connection
connection = pymongo.MongoClient("mongodb://localhost")
database = connection.poker
card_data = CardDAO(database)

#Table Window Dimenstions
table_dimensions_x = 800
table_dimensions_y = 570

#Cards relative to table window
cards_x = 264
cards_y = 173

my_hand_x = 219
my_hand_y = 347

#Distance Between Cards
dbc = 54 

#Card Box Dimensions
cards_box = (0,0,240,40)
number_box_dimension_x = 15#14
number_box_dimension_y = 22#21
card_one_box = (0,0,number_box_dimension_x,number_box_dimension_y)
card_two_box = (dbc*1,0,dbc*1+number_box_dimension_x,number_box_dimension_y)
card_three_box = (dbc*2,0,dbc*2+number_box_dimension_x,number_box_dimension_y)
card_four_box = (dbc*3,0,dbc*3+number_box_dimension_x,number_box_dimension_y)
card_five_box = (dbc*4,0,dbc*4+number_box_dimension_x,number_box_dimension_y)

'''
#Card Box Dimensions
cards_box_hand = (0,0,240,40)
number_box_dimension_x_hand = 15
number_box_dimension_y_hand = 20
card_one_box_hand = (0,0,number_box_dimension_x_hand,number_box_dimension_y_hand)
card_two_box_hand = (dbc*1,0,dbc*1+number_box_dimension_x_hand,number_box_dimension_y_hand)
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
    region = pyautogui.locateOnScreen(image_path('./poker_window.png'), region=(0,0,500,500))
    if region is None:
        raise Exception('Could not find game on screen. Is the game visible?')
    topLeftX = region[0] # left
    topLeftY = region[1] # top
    table_region = (topLeftX, topLeftY, topLeftX + table_dimensions_x, topLeftY + table_dimensions_y) # the game screen is always 800 x 570
    #print 'Table region found: {0}'.format(table_region)
    return table_region

def get_area_screenshot(table_region, number_box_dimension_x, number_box_dimension_y, area_box):
    topLeftX = table_region[0]
    topLeftY = table_region[1]
    x = topLeftX + number_box_dimension_x
    y = topLeftY + area_y
    area = pyautogui.screenshot(region=(x,y,x+area_box[2],y+area_box[3]))
    area_cut = area.crop(box=area_box)
    area_cut.save("./images/card_values_screenshot.png")
    return area_cut

def get_table_cards(all_cards, card_box, card_box_x, card_box_y):
    #To Black and White
    #all_cards = Image.open("./images/myHand3.png")
    card = all_cards.crop(box=card_box).convert('1')
    #card.save("./images/inCard.png")
    #Strings images together - tesseract likes this better than single numbers
    merged_image = Image.new('RGB', (card_box_x*10,card_box_y))
    for i in range(0,card_box_x*10,card_box_x):
        merged_image.paste(card, (i,0))
    merged_image.save("./images/inmergCard.png")
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
    except:
        pass
    #card.save("./images/card{0}.png".format(value))
    return value

def get_suits(all_cards, suit_box):
    suit = all_cards.crop(box=suit_box)
    suit_array = numpy.array(suit)
    suit_array_sum = suit_array.sum()
    if suit_array_sum < 100000:
        return None
    if suit_array_sum > 128000 and suit_array_sum < 135000:
        return "S"
    if suit_array_sum > 135000 and suit_array_sum < 140000:
        return "C"
    if suit_array_sum > 150000 and suit_array_sum < 155000:
        return "H"
    if suit_array_sum > 160000 and suit_array_sum < 165000:
        return "D"
    #suit.save("./images/suit.png")

def get_table_cards(table_region):
    card_boxes = [card_one_box,card_two_box,card_three_box,card_four_box,card_five_box]
    suit_boxes = [suit_one_box,suit_two_box,suit_three_box,suit_four_box,suit_five_box]

    for suit_box,card_box in zip(card_boxes,suit_boxes):
        all_cards = get_area_screenshot(table_region, cards_x, cards_y, cards_box)
        get_table_cards(all_cards, card_box, card_box_x, card_box_y)
        get_suits(all_cards, suit_box)
        
    

def click_fold(region):
    fold_button = pyautogui.locateOnScreen(image_path('./fold_button.png'), region=region)
    if fold_button:
        #Wait a Little then click fold
        time.sleep(.5)
        x = fold_button[0] + 5
        y = fold_button[1] + 5
        #Click Fold
        pyautogui.click(x=x,y=y)
        #Close Helpful advise for idiots
        pyautogui.click(x=x+130,y=y-120)
        return True
    return False
    
def insert_into_db(hand_array):
    card_data.insert_cards(hand_array)

def parse_following(table_region):
    print get_hand_cards(table_region)
    print get_table_cards(table_region)
    click_fold(table_region)
    time.sleep(5)

def main():
    for x in range (0,1000):
        table_region = get_table_region()
        parse_following(table_region)

if __name__ == '__main__':
    main()
