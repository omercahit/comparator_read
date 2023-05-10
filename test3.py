import cv2
import numpy as np
import math

def angle3pt(a, b, c):
    """Counterclockwise angle in degrees by turning from a to c around b
        Returns a float between 0.0 and 360.0"""
    ang = math.degrees(
        math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

imgname = "sample9"

img = cv2.imread(imgname+".jpg")
img_copy = img

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

height, width = gray_img.shape
mask = np.zeros((height, width), np.uint8)

blur = cv2.blur(gray_img, (5, 5))

ret, th = cv2.threshold(blur, 65, 255, cv2.THRESH_BINARY)

edges = cv2.Canny(th, 100, 200)

circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, 1.2, 100)

xc = int(circles[0][0][0])
yc = int(circles[0][0][1])
rc = int(circles[0][0][2])

circ = cv2.circle(mask, (xc, yc), rc, (255, 255, 255),
                  thickness=-1)

masked_data = cv2.bitwise_and(img, img, mask=mask)

gray2 = cv2.cvtColor(masked_data, cv2.COLOR_BGR2GRAY)
ret2, th2 = cv2.threshold(gray2, 100, 255, cv2.THRESH_BINARY)

edged = cv2.Canny(th2, 100, 200)

lines_list = []

# lines = cv2.HoughLines(edged, 3, np.pi/180, 100)

lines = cv2.HoughLinesP(
    edged,  # Input edge image
    1,  # Distance resolution in pixels
    np.pi / 180,  # Angle resolution in radians
    threshold=80,  # Min number of votes for valid line
    minLineLength=5,  # Min allowed length of line
    maxLineGap=15  # Max allowed gap between line for joining them
)

if lines is not None:
    x1, y1, x2, y2 = lines[0][0]
    lined = cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    d1 = ((x1-xc)**2 + (y1-yc)**2)**0.5
    d2 = ((x2-xc)**2 + (y2-yc)**2)**0.5

    if d1 > d2:
        needle_x = x1
        needle_y = y1
    else:
        needle_x = x2
        needle_y = y2

    """for points in lines:
        # Extracted points nested in the list
        x1, y1, x2, y2 = points[0]
        # Draw the lines joing the points
        # On the original image
        lined = cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # Maintain a simples lookup list for points
        lines_list.append([(x1, y1), (x2, y2)])"""

    lined = cv2.line(lined, (xc, yc), (needle_x, needle_y), (0, 0, 255), 2)
    lined = cv2.line(lined, (xc, yc), (xc, yc-100), (255, 0, 0), 2)

    m = abs(((needle_y-yc)/(needle_x-xc)))
    print(m, xc, yc)

    print("alpha", math.degrees(math.atan(m)))

    if needle_x < xc and needle_y < yc:
        a = 270 + math.degrees(math.atan(m))
    elif needle_x > xc and needle_y > yc:
        a = 90 + math.degrees(math.atan(m))
    elif needle_x < xc and needle_y > yc:
        a = 270 - math.degrees(math.atan(m))
    elif needle_x > xc and needle_y < yc:
        a = 90 - math.degrees(math.atan(m))

    #a = angle3pt(xc, int(circles[0][0][1]) - 100),(x2,y2),(x1,y1))

    val = (100*a)/360
    print("ang",a)
    print("val",val)

    lined = cv2.circle(lined, (needle_x, needle_y), 7, (0,0,255),-1)

    lined = cv2.putText(lined, str(round(val,2)), (xc+50,yc-180), cv2.FONT_HERSHEY_SIMPLEX,
                   2, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow("frame", lined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite(imgname+"_result.jpg", lined)

else:
    cv2.imshow("frame", edged)
    cv2.waitKey(0)
    cv2.destroyAllWindows()