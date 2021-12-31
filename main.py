import cv2
import numpy as np
import  pickle

#VIDEO FEED
cap = cv2.VideoCapture('carPark.mp4')

#TRACKBARS
def empty(a):
    pass


cv2.namedWindow("Vals")
cv2.resizeWindow("Vals", 640, 240)
cv2.createTrackbar("Val1", "Vals", 25, 50, empty)
cv2.createTrackbar("Val2", "Vals", 16, 50, empty)
cv2.createTrackbar("Val3", "Vals", 5, 50, empty)
width, height = 134, 50

#LOAD PARKING SPACE POSITIONS
with open('parking_space', 'rb') as f:
    position = pickle.load(f)


def checkarkingspace(feed):
    space = 0

    for pos in position:
        x, y = pos
        imgcrop = feed[y:y + height, x:x + width]
        # cv2.imshow(str(x*y), imgcrop)
        count = cv2.countNonZero(imgcrop)
        cv2.putText(vid, str(count), (x, y + height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)

        if count < 1100:
            color = (0, 255, 0)
            thickness = 5
            space += 1
        else:
            color = (0, 0, 255)
            thickness = 2
        cv2.rectangle(vid, pos, (pos[0] + width, pos[1] + height), color, thickness)
    parked = len(position)
    text = f'{str(space)}/{str(parked)}'
    cv2.putText(vid, str(text), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), thickness=5)

while True:
    # VIDEO INPUT
    suc, vid = cap.read()
    vid = cv2.resize(vid, (1366, 768))


    ##MAKING VIDEO LOOP
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    gray = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 1)

    val1 = cv2.getTrackbarPos("Val1", "Vals")
    val2 = cv2.getTrackbarPos("Val2", "Vals")
    val3 = cv2.getTrackbarPos("Val3", "Vals")
    if val1 % 2 == 0: val1 += 1
    if val3 % 2 == 0: val3 += 1
    Thres = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, val1, val2)
    medianblur = cv2.medianBlur(Thres, val3)
    kernel = np.ones((3, 3), np.uint8)
    dilate = cv2.dilate(medianblur, kernel, iterations=1)

    checkarkingspace(dilate)


    #VIDEO OUTPUT
    cv2.imshow('VIDEO', vid)
    # cv2.imshow('VIDEO1', dilate)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break