import picamera.array
import picamera
import time
import cv2

class Camera:
    def __init__(self, previewWidth, previewHeight, captureWidth, captureHeight, frameRate, brightness, rotation, textSize):
        self._previewWidth = previewWidth
        self._previewHeight = previewHeight
        self._captureWidth = captureWidth
        self._captureHeight = captureHeight
        self._frameRate = frameRate
        self._brightness = brightness
        self._rotation = rotation
        self._textSize = textSize

        self.setupCamera(self._previewWidth, self._previewHeight, self._frameRate, self._brightness, self._rotation, self._textSize)

    def startPreview(self):
        self._camera.start_preview()
        time.sleep(1) # allow some time for the camera to calibrate

    def stopPreview(self):
        self._camera.stop_preview()

    def setText(self, text):
        self._camera.annotate_text = text

    def setupCamera(self, width, height, frameRate, brightness, rotation, textSize):
        self._camera = picamera.PiCamera()
        self._camera.resolution = (width, height)
        self._camera.framerate = frameRate
        self._camera.brightness = brightness
        #camera.contrast = 8
        #self._camera.video_stabilization = True
        self._exposure_mode = 'auto'
        self._camera.rotation = rotation
        self._rawCapture = picamera.array.PiRGBArray(self._camera, size=(width,height))
        self._camera.annotate_text_size = textSize

    def capture(self):
        # close and re-open the camera with the capture resolution
        self._camera.close()
        self.setupCamera(self._captureWidth, self._captureHeight, self._frameRate, self._brightness, self._rotation, self._textSize)
        self.setText("")
       ## time.sleep(1) # allow some time for the camera to calibrate

        # take the image
        self._camera.capture(self._rawCapture, 'rgb', use_video_port=False)
        img = self._rawCapture.array
        
        # close and re-open the camera with the preview resolution
        self._camera.close()
        self.setupCamera(self._previewWidth, self._previewHeight, self._frameRate, self._brightness, self._rotation, self._textSize)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img
         
    #def __del__(self): 
        #self._camera.release() # todo clean up


""" Old OpenCV camera code
# make sure camera is enabled on pi
#subprocess.call(["sudo", "modprobe",  "bcm2835-v4l2"])
class Camera:
    def __init__(self, width, height, fps, brightness):
        self._backend = backend
        if self._backend == Backend.OPENCV:
            self._camera = cv2.VideoCapture(0)
            self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self._camera.set(cv2.CAP_PROP_FPS, fps)
            self._camera.set(cv2.CAP_PROP_BRIGHTNESS, brightness / 100)

    def capture(self):
        ret_val, image = self._camera.read()
        return image

    def __del__(self): 
        self._camera.release()
"""        
