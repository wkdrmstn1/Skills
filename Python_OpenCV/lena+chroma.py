import cv2
import numpy as np

lena = cv2.imread('lenna.png')
lena = cv2.resize(lena, (250,250))
src = cv2.imread('carrot.jpg')
src = cv2.resize(src, (250,250))

green_mask = cv2.inRange(src,(0,120,0), (100,255,100))      # 초록 배경만 누끼 따기
mask_fg = green_mask                                        # 초록색 부분만 하얗게 강조
mask_bg = cv2.bitwise_not(mask_fg)                          # 초록부분 reverse 

src_fg = cv2.bitwise_and(src,src,mask=mask_bg)              # 
lena_bg = cv2.bitwise_and(lena,lena,mask=mask_fg)           # 

result = src_fg + lena_bg

cv2.imshow("green_mask",green_mask)
cv2.imshow("mask_bg",mask_bg)
cv2.imshow("src_fg",src_fg)
cv2.imshow("lena_bg",lena_bg)
cv2.imshow("result",result)

cv2.waitKey()
cv2.destroyAllWindows()