'''
Created on Oct 20, 2019

@author: yokouchiryouta
'''
# -*- coding: utf-8 -*-

import cv2, sys
import numpy as np

URL = "http://153.205.16.204:60222/?action=stream"
cap = cv2.VideoCapture(URL)

fps = 15
size = (314,240)

cap.set(3, size[0])  # Width
cap.set(4, size[1])  # Heigh
cap.set(5, fps)   # FPS

while(cap.isOpened()):
  ret, frame = cap.read()

  if type(frame).__module__ == np.__name__:
    cv2.imshow('Stream Video',frame)
  else:
    cv2.imshow('frame', 0)

  key = cv2.waitKey(1) & 0xff
  if key == ord('q'): break

cap.release()
cv2.destroyAllWindows()