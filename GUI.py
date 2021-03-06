import numpy as np
import cv2
import time
from copy import deepcopy
from globals import *

def createFrameBlack():
    return np.zeros((WINDOW_H, WINDOW_W, 3), np.uint8)

def writeText(frame, text, x, y, font, size, thickness, colour):
    cv2.putText(frame, text, (int(x), int(y)), font, size, colour, thickness, cv2.LINE_AA)

def writeTextCentered(frame, text, font, size, thickness, colour):
    textsize = cv2.getTextSize(text, font, size, thickness)[0]

    # get coords based on boundary
    textX = (frame.shape[1] - textsize[0]) / 2
    textY = (frame.shape[0] + textsize[1]) / 2

    writeText(frame, text, textX, textY, font, size, thickness, colour)

def writeTextCenteredHorizontal(frame, text, y, font, size, thickness, colour):
    textsize = cv2.getTextSize(text, font, size, thickness)[0]

    # get coords based on boundary
    textX = (frame.shape[1] - textsize[0]) / 2
    
    writeText(frame, text, textX, y, font, size, thickness, colour)

def overlay_transparent(background, overlay, x, y):

    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

def overlayGraphicFrame(frame):
    overlay = cv2.imread('overlay.png', cv2.IMREAD_UNCHANGED)
    overlay_transparent(frame, overlay, 30, WINDOW_H - 120)

def overlayPolaroidFrame(frame):
    top = int(0.05 * frame.shape[0])  # shape[0] = rows
    bottom = int(0.15 * frame.shape[0])
    left = int(0.05 * frame.shape[1])  # shape[1] = cols
    right = left
    newf = cv2.copyMakeBorder(frame, top, bottom, left, right, cv2.BORDER_CONSTANT, None, COLOUR_WHITE)
    writeTextCenteredHorizontal(newf, "Rebecca & Harry   Mar Hall   22/09/2019", newf.shape[0] - 30, FONT_ITALIC, STARTOVER_SIZE, STARTOVER_THICKNESS, COLOUR_BLACK)
    return newf

def startScreen():
    pressButtonFrame = createFrameBlack()
    
    writeTextCenteredHorizontal(pressButtonFrame, CAPTURE_TEXT, CAPTURE_Y - 50, FONT_NORMAL, CAPTURE_SIZE, CAPTURE_THICKNESS, COLOUR_WHITE)
    writeTextCenteredHorizontal(pressButtonFrame, CAPTURE_TEXT2, CAPTURE_Y + 70, FONT_NORMAL, CAPTURE_SIZE, CAPTURE_THICKNESS, COLOUR_WHITE)
    writeTextCenteredHorizontal(pressButtonFrame, CAPTURE_TEXT3, CAPTURE_Y + 300, FONT_NORMAL, 2.5, CAPTURE_THICKNESS, COLOUR_WHITE)
    
    return pressButtonFrame

def printScreen():
    printScreenFrame = createFrameBlack()
    
    writeTextCenteredHorizontal(printScreenFrame, "Printing...", 200, FONT_NORMAL, CAPTURE_SIZE, CAPTURE_THICKNESS, COLOUR_WHITE)

    return printScreenFrame

def outputDisplay(image):
    print("outputDisplay")

    frame = deepcopy(image)
    frame = cv2.resize(frame, (1440, 900))
    
    x = 0
    y = WINDOW_H - 230
    w = WINDOW_W
    h = 300

    overlay = frame.copy()

    cv2.rectangle(overlay, (x, y), (x+w, y+h), COLOUR_BLACK, -1)
    alpha = 0.6
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # write start over and print text
    writeText(frame, STARTOVER_TEXT, STARTOVER_X, STARTOVER_Y, FONT_NORMAL, STARTOVER_SIZE, STARTOVER_THICKNESS, COLOUR_WHITE)
    writeText(frame, PRINT_TEXT, PRINT_TEXT_X, PRINT_TEXT_Y, FONT_NORMAL, PRINT_TEXT_SIZE, PRINT_TEXT_THICKNESS, COLOUR_WHITE)

    overlay_transparent(frame, arrow, STARTOVER_X + 150, STARTOVER_Y + 20)
    overlay_transparent(frame, arrow, PRINT_TEXT_X + 290, STARTOVER_Y + 20)

    cv2.imshow('Photobooth', frame)

def countdownDisplay(t, camera):
    print("countdownDisplay")
    oldTime = time.time()
    timeLeft = t
    img = 0
    while timeLeft > 0:
        currentTime = time.time()

        img = camera.capture()

        writeTextCentered(img, str(timeLeft), FONT_NORMAL, 4, 2, COLOUR_WHITE)
        cv2.imshow('Photobooth', img)
        cv2.waitKey(1)

        # 1 second has passed
        if currentTime - oldTime >= 1:
            print("preview countdown {0}s left".format(str(timeLeft)))
            timeLeft -= 1
            oldTime = time.time()

    img = camera.capture()
    return img