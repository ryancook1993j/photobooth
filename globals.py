import os
import cv2
from PIL import ImageFont, ImageDraw, Image

WINDOW_W = 1640
WINDOW_H = 922

# capture and print resolution (match with aspect ratio of print, using 3:2 for 6x4 print)
#CAPTURE_W = 2560
#CAPTURE_H = 1440

CAPTURE_W = 2592
CAPTURE_H = 1728

OUTPUT_PATH = str(os.getcwd()) + "/photos/"

COUNTDOWN_TIME = 5
COUNTDOWN_SIZE = 6
COUNTDOWN_THICKNESS = 5
COUNTDOWN_OVERLAY_X = WINDOW_W / 2
COUNTDOWN_OVERLAY_Y = (WINDOW_H / 2)
COUNTDOWN_OVERLAY_W = COUNTDOWN_OVERLAY_X + 200
COUNTDOWN_OVERLAY_H = COUNTDOWN_OVERLAY_Y + 200

CAPTURE_TEXT = "Press the Flashing button"
CAPTURE_TEXT2 = "below to take a photo!"
CAPTURE_TEXT3 = "You have " + str(COUNTDOWN_TIME) + " seconds to pose!"
CAPTURE_X = (CAPTURE_W / 2) - 50
CAPTURE_Y = (CAPTURE_H / 2) 
CAPTURE_SIZE = 3.5
CAPTURE_THICKNESS = 3

STARTOVER_TEXT = "Start Over"
STARTOVER_X = 50
STARTOVER_Y = CAPTURE_H - 130
STARTOVER_SIZE = 3
STARTOVER_THICKNESS = 3

PRINT_TEXT = "Print Photo!"
PRINT_TEXT_X = CAPTURE_W - 600
PRINT_TEXT_Y = CAPTURE_H - 130
PRINT_TEXT_SIZE = 3
PRINT_TEXT_THICKNESS = 3

arrow = cv2.imread('arrow.png', cv2.IMREAD_UNCHANGED)
arrow = cv2.resize(arrow, None, fx=0.4, fy=0.4)

BUTTON_CAPTURE = ord('c')
BUTTON_STARTOVER = ord('s')
BUTTON_PRINT = ord('p')
BUTTON_EXIT = ord('q')

COLOUR_WHITE = (255, 255, 255)
COLOUR_BLACK = (0, 0, 0)

FONT_NORMAL = cv2.FONT_HERSHEY_SIMPLEX
FONT_ITALIC = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
roboto_font = ImageFont.truetype("Roboto-Regular.ttf", 148)

POLAROID_STYLE = False
POLAROID_TEXT = "Laura & Martin Crossbasket Castle 25/07/2020"
