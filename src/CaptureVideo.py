import cv2
from threading import Thread


class CaptureVideo:

    def __init__(self, ip=0):
        self.video = cv2.VideoCapture(ip)
        self.success, self.image = self.video.read()
        if not self.success:
            return
        self.stop = False

    def start(self):
        Thread(target=self.update(), args=()).start()
        return self

    def update(self):
        while True:
            if self.stop:
                return
            self.success, self.image = self.video.read()

    def read(self):
        return self.video

    def stop(self):
        self.stop = True
