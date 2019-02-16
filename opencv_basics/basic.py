import cv2

img = cv2.imread("download.png", 1)
BW_img = cv2.imread("download.png", 0)

# print(img)
# print(BW_img)

# print(img.shape)
# print(BW_img.shape)

# Resize img to half of original size
img = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))

cv2.imshow("Window_name", img)
cv2.waitKey(0)
cv2.imshow("Window_name", BW_img)
cv2.waitKey(0)

cv2.destroyAllWindows()
