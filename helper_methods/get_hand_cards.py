import pyautogui
from PIL import Image
import time
import random
import numpy
from check_card import check_card

def get_hand_cards(table_region):
    topLeftX = table_region[0]
    topLeftY = table_region[1]
    
    card_one_offset_x = topLeftX + 218
    card_one_offset_y = topLeftY + 349
    final_x = card_one_offset_x + 45
    final_y = card_one_offset_y + 36
    area_box_one = (0,0,48,36)
    area_box_two = (54,0,102,36)
    hand_card_dimensions = (card_one_offset_x,card_one_offset_y,final_x,final_y)
    card_one_screenshot = pyautogui.screenshot(region=hand_card_dimensions)
    area_cut_one = card_one_screenshot.crop(box=area_box_one)
    area_cut_two = card_one_screenshot.crop(box=area_box_two)
    card_one_array = numpy.array(area_cut_one)
    card_two_array = numpy.array(area_cut_two)

    card_number_1 = check_card(card_one_array.sum())
    card_number_2 = check_card(card_two_array.sum())
    return card_number_1, card_number_2
    #area_cut_two.save("./images/card_two_screenshot.png")
