# -*- coding: utf-8 -*-
from tests import im_folder
import cv2
import os
import sys
import docdetect
import numpy as np
import urllib.request
from time import sleep
import threading
import time
current_milli_time = lambda: int(round(time.time() * 1000))
# url='http://172.16.50.57:8080/shot.jpg'
url='http://192.168.43.109:8080/shot.jpg'

video_path = os.path.join(im_folder, 'black.mp4')
video = cv2.VideoCapture(video_path)
cv2.startWindowThread()
cv2.namedWindow('output')
cv2.moveWindow('output', 500, 30)

model = sys.argv[2]
# print (model)
edge_detection = cv2.ximgproc.createStructuredEdgeDetection(model)
rects = None
milis = current_milli_time()
while True:
    imgResp=urllib.request.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    frame=cv2.imdecode(imgNp,-1)

    if current_milli_time() - milis > 500:
        # print ("hey...")
        milis = current_milli_time()
        rects = docdetect.process(frame, edge_detection)

    
    if rects:    
        frame1 = docdetect.draw(rects, frame)
    
        cv2.imshow('output', frame1)

    
    # cv2.imshow('output2', frame2)

    cv2.waitKey(1)
video.release()

# def printit():
#     threading.Timer(0.5, printit).start()
#     imgResp=urllib.request.urlopen(url)
#     imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
#     frame=cv2.imdecode(imgNp,-1)
#     rects = docdetect.process(frame, edge_detection)
#     frame = docdetect.draw(rects, frame)
#     cv2.imshow('output', frame)
#     cv2.waitKey(1)
# #   print ("Hello, World!")
# printit()
# video.release()
