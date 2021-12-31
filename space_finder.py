import cv2
import pickle
import matplotlib.pyplot as plt
# img = cv2.imread('carParkImg.png')

width, height = 134, 50

try:
    with open('parking_space', 'rb') as f:
        position = pickle.load(f)
except:
    position = []

def mouseclick(events, x,y, flags, param):
    if events == cv2.EVENT_LBUTTONDOWN:
        position.append((x, y))
        print(position)
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(position):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                position.pop(i)
    with open('parking_space', 'wb') as f:
        pickle.dump(position, f)

while True:
    img = cv2.imread('carParkImg.png')
    img = cv2.resize(img, (1366, 768))

    #TO FIND DIMENSIONS OF RECTANGLE
    # img = cv2.rectangle(img, (61, 105), (195, 156), (255, 0, 255), 2)
    # plt.imshow(img)
    # plt.show()
    #
    #TO DRAW RECTANGLE ON IMG USING MOUSECLICK
    for pos in position:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)


    cv2.imshow('IMG', img)
    cv2.setMouseCallback('IMG', mouseclick)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
