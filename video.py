import math

import cv2
import numpy as np

#cap = cv2.VideoCapture("http://172.16.66.97:4747/video")
cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()

    try:
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        height, width = gray_img.shape
        mask = np.zeros((height, width), np.uint8)

        blur = cv2.blur(gray_img, (5, 5))

        ret, th = cv2.threshold(blur, 65, 255, cv2.THRESH_BINARY)

        edges = cv2.Canny(th, 100, 200)

        circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, 1.2, 100)

        circ = cv2.circle(mask, (int(circles[0][0][0]), int(circles[0][0][1])), int(circles[0][0][2]), (255, 255, 255),
                          thickness=-1)

        masked_data = cv2.bitwise_and(frame, frame, mask=mask)

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
            lined = cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            """for points in lines:
                # Extracted points nested in the list
                x1, y1, x2, y2 = points[0]
                # Draw the lines joing the points
                # On the original image
                lined = cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # Maintain a simples lookup list for points
                lines_list.append([(x1, y1), (x2, y2)])"""

            lined = cv2.line(lined, (int(circles[0][0][0]), int(circles[0][0][1])),
                             (int(circles[0][0][0]), int(circles[0][0][1]) - 100), (0, 0, 255), 2)

            m1 = int((y2-y1)/(x2-x1))
            m2 = int(((int(circles[0][0][1]) - 100)-(int(circles[0][0][1])))/((int(circles[0][0][0]))-(int(circles[0][0][0]))))
            tana = abs((m2-m1)/(1+(m1*m2)))
            a = math.degrees(math.atan(tana))
            val = (100*a)/360
            print(val)


            cv2.imshow("frame", lined)

        else:
            cv2.imshow("frame", edged)

    except:
        continue



    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()