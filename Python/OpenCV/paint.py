import cv2
import numpy as np

# 흰색 배경 생성 (512x512)
canvas = np.full((512, 512, 3), 255, dtype=np.uint8)
drawing = False

def mouse_callback(event, x, y, flags, param):
    global drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True       
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(canvas, (x,y), 4, (0, 0, 0), -1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

'''
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :
        if flags == cv2.EVENT_FLAG_LBUTTON :
            cv2.circle(canvas, (x, y), 3, (0, 0, 0), -1)
'''

while True:
    cv2.imshow('Canvas', canvas)
    cv2.setMouseCallback('Canvas',mouse_callback)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
       canvas[:] = 255
        
    elif key == ord('q') or key == 27:
        break

cv2.destroyAllWindows()