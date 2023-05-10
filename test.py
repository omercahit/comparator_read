import cv2

img = cv2.imread("s18.jpg")

scale_percent = 20  # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)

# resize image
resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

cv2.imshow("resized", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("s18.jpg",resized)