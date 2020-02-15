import time
import cv2
import numpy as np
from enum import Enum
from copy import deepcopy
from globals import *

class Backend(Enum):
    OPENCV = 1
    PICAM = 2


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


class Camera:
    def __init__(self, backend, previewDuration):
        self._backend = backend
        self._previewDuration = previewDuration
        self._previewImage = "test"
        self._captureImage = "test"
        self._camera = cv2.VideoCapture(0)
        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)

    def previewCountdown(self):
        print("previewCountdown")

        oldTime = time.time()
        timeLeft = self._previewDuration
        while True:
            currentTime = time.time()

            ret_val, img = self._camera.read()

            writeTextCentered(img, str(timeLeft), FONT_NORMAL, 4, 2, COLOUR_WHITE)
            cv2.imshow('Photobooth', img)
            cv2.waitKey(1)
            img = createFrameBlack()

            # 1 second has passed
            if currentTime - oldTime >= 1:
                print("preview countdown {0}s left".format(str(timeLeft)))
                timeLeft -= 1
                oldTime = time.time()

            # countdown finished
            if timeLeft < 1:
                print("finished preview")
                self._previewImage = self._camera.read()
                return

    def getPreviewImage(self):
        return self._previewImage

    def capture(self):
        ret_val, self._captureImage = self._camera.read()
        return self._captureImage
        print("capture")

    def outputDisplay(self):
        frame = deepcopy(self._captureImage)
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

        print("outputDisplay")

        return frame

    def startScreen(self):
        pressButtonFrame = createFrameBlack()
        
        writeTextCenteredHorizontal(pressButtonFrame, CAPTURE_TEXT, CAPTURE_Y - 50, FONT_NORMAL, CAPTURE_SIZE, CAPTURE_THICKNESS, COLOUR_WHITE)
        writeTextCenteredHorizontal(pressButtonFrame, CAPTURE_TEXT2, CAPTURE_Y + 70, FONT_NORMAL, CAPTURE_SIZE, CAPTURE_THICKNESS, COLOUR_WHITE)
        writeTextCenteredHorizontal(pressButtonFrame, CAPTURE_TEXT3, CAPTURE_Y + 300, FONT_NORMAL, 2.5, CAPTURE_THICKNESS, COLOUR_WHITE)
        
        return pressButtonFrame

    def printScreen(self):
        printScreenFrame = createFrameBlack()
        
        writeTextCenteredHorizontal(printScreenFrame, "Printing...", 200, FONT_NORMAL, CAPTURE_SIZE, CAPTURE_THICKNESS, COLOUR_WHITE)

        return printScreenFrame