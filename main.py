import cv2
import numpy as np

img = cv2.imread("s18.jpg")
img_copy = img

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

height, width = gray_img.shape
mask = np.zeros((height,width), np.uint8)

blur = cv2.blur(gray_img, (5,5))

ret, th = cv2.threshold(blur, 90, 255, cv2.THRESH_BINARY)

cv2.imshow("th", th)
cv2.waitKey(0)
cv2.destroyAllWindows()

edges = cv2.Canny(th, 100, 200)

circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, 1.2, 100)
print(circles)
circ = cv2.circle(mask, (int(circles[0][0][0]), int(circles[0][0][1])), int(circles[0][0][2]), (255,255,255), thickness=-1)

cv2.imshow("circ", circ)
cv2.waitKey(0)
cv2.destroyAllWindows()

#blur = cv2.blur(img, (5,5))
masked_data = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow("masked", masked_data)
cv2.waitKey(0)
cv2.destroyAllWindows()

gray2 = cv2.cvtColor(masked_data, cv2.COLOR_BGR2GRAY)
ret2, th2 = cv2.threshold(gray2, 90, 255, cv2.THRESH_BINARY)
#th2 = cv2.erode(th2,np.ones((7,7),np.uint8) ,iterations = 1)

cv2.imshow("th2", th2)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""contours = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
temp = 0
for i in range(1, len(contours)):
    if cv2.contourArea(contours[i]) > temp:
        temp = cv2.contourArea(contours[i])
        cnt = contours[i]
    print("area",cv2.contourArea(contours[i]), temp)
largest_areas = sorted(contours, key=cv2.contourArea)
#ind = contours.index(largest_areas[-2])
cntdraw = cv2.drawContours(img, largest_areas[-2], -1, (0,255,0), -1)
cv2.imshow("cntdraw", cntdraw)
cv2.waitKey(0)
cv2.destroyAllWindows()

line = cv2.fitLine(largest_areas[-2], cv2.DIST_L2, 0, 0.01, 0.01)
print(line)

linefitted = cv2.line(cntdraw,(int(line[0]), int(line[1])), (int(line[2]), int(line[3])), (255, 0, 0), 3)

cv2.imshow("edged", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(largest_areas[-2])"""


edged = cv2.Canny(th2, 100, 200)

cv2.imshow("edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

##############################################################

lines_list = []

#lines = cv2.HoughLines(edged, 3, np.pi/180, 100)

lines = cv2.HoughLinesP(
            edged, # Input edge image
            1, # Distance resolution in pixels
            np.pi/180, # Angle resolution in radians
            threshold=80, # Min number of votes for valid line
            minLineLength=5, # Min allowed length of line
            maxLineGap=15 # Max allowed gap between line for joining them
            )

print(lines)

for points in lines:
      # Extracted points nested in the list
    x1,y1,x2,y2=points[0]
    # Draw the lines joing the points
    # On the original image
    lined = cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    # Maintain a simples lookup list for points
    lines_list.append([(x1,y1),(x2,y2)])

print(lines_list)

cv2.imshow("img", lined)
cv2.waitKey(0)
cv2.destroyAllWindows()