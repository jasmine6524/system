import os
import sys
import time
import numpy as np
import cv2
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtGui import QImage, QPixmap, QWindow

from PyQt5.QtWidgets import *
from draft_layout_2 import Ui_MainWindow
from PIL import Image, ImageQt

import speech_recognition as sr
import pyttsx3 as pt
import mac_say
import pyttsx3 as pt
import time

class myWindow(QWidget, Ui_MainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        self.initUI()
        self.initArgs()
        self.initSlot()
        
        
    def initSlot(self):
        self.imageBtn.clicked.connect(self.selectImage)
        self.timer.timeout.connect(self.showFrame)
        # self.cameraOn.clicked.connect(self.openCamera)
        # self.cameraOff.clicked.connect(self.closeCamera)
        # self.captureImage.clicked.connect(self.capture)

    def initUI(self):
        self.win = QMainWindow()
        self.setupUi(self.win)

    def initArgs(self):
        self.timer = QTimer()
        self.cap = None
        self.flag  = False

    def show(self):
        self.win.show()
            

    def openCamera(self):
        self.cap = cv2.VideoCapture(0)#0是表示调用电脑自带的摄像头，1是表示调用外接摄像头
        self.timer.start(100)

    def showFrame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (591, 332))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1]*3, QImage.Format_RGB888)
            self.cameraArea.setPixmap(QPixmap.fromImage(frame))
        
    def capture(self):
        self.flag = True
        self.closeCamera()
        self.flag = False

    def closeCamera(self):
        self.timer.stop()
        #self.cap.release()
        if not self.flag:
            self.cameraArea.clear()
    
    def selectModel(self):
        '''
        function: 选择一个电脑上的网络模型
        '''
        fileName, fileType = QFileDialog.getOpenFileName(
            self,
            'select model',
            os.getcwd(),
            'Pth Files(*.pth)')
        
        if fileName == '':
            msg = QMessageBox.warning(self, 'Warning', 'Please select a model', QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.modelPath.setText(fileName)
        # os.path.abspath(os.path.dirname(os.getcwd()))
    
    def selectImage(self):
        '''
        function: 上传一张电脑上的图片
        '''
        imageName, imageType = QFileDialog.getOpenFileName(
            self,
            'select image',
            os.getcwd(),
            'Jpg Files(*.jpg);;Png Files(*.png)'
        )
        if imageName == '':
            msg = (QMessageBox.warning(self, 'Warning', 'Please select an image', QMessageBox.Ok, QMessageBox.Ok))
        else:
            self.imagePath.setText(imageName)
            self.showImage(imageName)
    
    def showImage(self, path):
        '''
        function: 根据图片的大小进行相应的调整来将一个图片完整的现实在display框里
        parameters: path = 路径
        '''
        img = Image.open(path)
        w, h = img.size
        if w > 421 and h < 301: #421是display的宽度，301是display的高度
            r = w / 421
            img = img.resize((421, int(h/r)), 4)
        elif h > 301 and w < 481:
            r = h / 301
            img = img.resize((int(w/r), 281), 4)
        elif h > 301 and w > 481:
            r = h / 301
            img = img.resize((int(w/r), 281), 4)
        img = ImageQt.toqpixmap(img)
        self.cameraArea.setPixmap(img)



def voiceControl(win):
    r = sr.Recognizer()
    print (sr.Microphone.list_microphone_names()[0])
    mic = sr.Microphone(device_index=0)
    mac_say.say('1, say open to open the camera, 2, say close to close the camera, 3, say capture to capture a frame')
    while True:
        #sp.say('input your command')
        mac_say.say("input your command")
        if input() == 'r':
            with mic as source:
                #r.adjust_for_ambient_noise(source)
                mac_say.say('ready to say your command')
                audio = r.listen(source)
                cmd = r.recognize_google(audio)
                print(cmd)
                if cmd == 'open':
                    mac_say.say('camera opened')
                    win.openCamera()
                elif cmd == 'close':
                    mac_say.say('camera closed')
                    win.closeCamera()
                elif cmd == 'capture':
                    mac_say.say('frame captured')
                    win.capture()
        else:
            break       

if __name__ == '__main__':
    app = QApplication(sys.argv) #application是底层, window在上面
    win = myWindow()
    win.show()
    voiceControl(win)
    app.exec_()
    sys.exit() #不断的重复