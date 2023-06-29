# **Using openCV (Color Segmentation)**

로봇팔이 에어 하키 게임을 하기 위해서는 빠른 처리 속도가 관건임.

따라서 딥러닝 영상 처리 사용하는 것이랑 OpenCV를 사용하는 것이랑 어느 것이 puck 인식 정확도가 더 높고 처리 속도가 빠른지 확인해 볼 필요가 있음.

아래는 openCV를 활용하여 진행하는 과정임.

### 카메라 영상 출력

```python
import cv2 as cv

# Open the specified camera.
cap = cv.VideoCapture(2)

# Set the resolution of the video capture
# (be aware that some values might not be supported by your camera)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    # Read frame by frame.
    ret, frame = cap.read()

    # If there is no frame read or if there is a problem, exit the loop.
    if not ret:
        print("Unable to capture video")
        break
    flip = cv.flip(frame, 1)
    
    # Display the read frame on the screen.
    cv.namedWindow('Video', cv.WINDOW_AUTOSIZE)
    cv.imshow('Video', flip)

    # Press 'q' to exit the loop.
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources that have been used.
cap.release()
cv.destroyAllWindows()
```

영상의 해상도를 변경 하기 전에는 처리 속도가 매우 느렸음. 때문에 해상도를 640*480으로 다운그레이드함.

### Puck Segmentation

```python
import cv2 as cv
import numpy as np
import time
import os

# Global Variables
drawing = False
ix, iy = -1, -1
fx, fy = -1, -1
frame_hsv = None
roi_hist = None
user_font = cv.FONT_HERSHEY_COMPLEX

previous_position = None
current_position = None
previous_velocity = None
moved_left_since_path = False

def select_roi(event, x, y, flags, param):
    global ix, iy, fx, fy, drawing, frame_hsv, roi_hist

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        fx, fy = x, y

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            fx, fy = x, y

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        fx, fy = x, y
        hsv_roi = frame_hsv[iy:fy, ix:fx]
        mask = cv.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)

cameraNumber = 2

video_path = 'E:/Grace_Praise/HGU/23년 1학기/IAIA/Final/hw_setting_after.mp4'
#cap = cv.VideoCapture(video_path)
cap = cv.VideoCapture(cameraNumber)
cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter.fourcc('M','J','P','G'))
cap.set(cv.CAP_PROP_FPS, 60.0) 

# Check if the video capture was successful
if not cap.isOpened():
    print("Unable to open video file")
    exit()

# Get frame width, height, and frames per second (fps)
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv.CAP_PROP_FPS))
print("Video properties - Width:", width, "Height:", height, "FPS:", fps)

# Create a window with the same size as the video frame
cv.namedWindow('Video', cv.WINDOW_NORMAL)
cv.resizeWindow('Video', width, height)

cv.setMouseCallback('Video', select_roi)

def predict_path():
    global previous_position, current_position, previous_velocity, moved_left_since_path

    velocity = None

    if contours:
        for cnt in contours:
            area = cv.contourArea(cnt)
            if 200 <= area <= 1000:
                x, y, w, h = cv.boundingRect(cnt)
                
                # Calculate the center of the bounding box
                center_x = x + w // 2
                center_y = y + h // 2
                current_position = (center_x, center_y)
                
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                if previous_position is not None:
                    velocity = (current_position[0] - previous_position[0], current_position[1] - previous_position[1])
                    if velocity[0] < 0:
                        moved_left_since_path = True
                    if previous_velocity is not None and velocity[0] > 0 and moved_left_since_path:
                        # Extend the line to the boundary
                        if velocity[0] != 0:  # Avoid division by zero
                            # Calculate the slope of the line
                            slope = velocity[1] / velocity[0]
                            # Calculate the y-coordinate on the boundary for the line
                            boundary_y = int(previous_position[1] + slope*(rect_x2 - previous_position[0]))
                            cv.line(frame, previous_position, (rect_x2, boundary_y), (0, 0, 255), 3)
                            moved_left_since_path = False  # Reset the variable once the path has been drawn
                
                previous_position = current_position
                previous_velocity = velocity

while True:
    start_time = time.time()
    ret, frame = cap.read()

    if not ret:
        print("End of video")
        break

    #frame = cv.flip(frame, 1)
    frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    rect_x1 = 50
    rect_y1 = 100
    rect_x2 = width - 50
    rect_y2 = rect_y1 + int((rect_x2 - rect_x1) / 2.11)

    #cv.rectangle(frame, (rect_x1, rect_y1), (rect_x2, rect_y2), (153, 0, 204), 2)
    
    if drawing:
        cv.rectangle(frame, (ix, iy), (fx, fy), (255, 0, 0), 2)

    if roi_hist is not None:
        back_proj = cv.calcBackProject([frame_hsv], [0], roi_hist, [0, 180], 1)
        _, threshold = cv.threshold(back_proj, 1, 255, cv.THRESH_BINARY)
        contours, _ = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        predict_path()

    diff_time = time.time() - start_time

    if diff_time > 0:
        fps = 1 / diff_time

    cv.putText(frame, f'FPS: {fps:.2f}', (int(width/10), int(height/12)), user_font, 1, (100, 255, 0), 2)

    cv.imshow("Video", frame)

    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv.waitKey(0)

cap.release()
cv.destroyAllWindows()
```

드래그한 영역의 색상대의 물체만 contour를 따고,  그 중 가장 큰 것만 바운딩 박스로 표시하였음.

실험 결과 **HoughCircle**은 환경 의존도가 너무 높아 사용하기 힘들 것으로 판단됨. 

프레임 사이의 잔상으로 인해 puck의 형태를 따는 것은 사용하기 어렵다고 판단.

Color segmentation으로 puck을 인지하는 것으로 결정

### Algorithm Flow

1. 경기장과 동일한 사이즈의 외곽 라인 만듦
2. color segmentation
3. puck이 이동할 때, 처음 위치와 나중 위치를 통해 slope 측정하고 이를 가지고 예상 경로 예측

### Path Prediction:

```python
import cv2 as cv
import numpy as np
import time

# Global Variables
drawing = False
ix, iy = -1, -1
fx, fy = -1, -1
frame_hsv = None
roi_hist = None
user_font = cv.FONT_HERSHEY_COMPLEX

previous_position = None
current_position = None
previous_velocity = None
moved_left_since_path = False
path_drawn_time = None  # Time when the path was drawn
path_line = None  # Path line coordinates
reflected_path_line = None  # Reflected path line coordinates

# select the hsv range using mouse
def select_roi(event, x, y, flags, param):
    global ix, iy, fx, fy, drawing, frame_hsv, roi_hist

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        fx, fy = x, y

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            fx, fy = x, y

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        fx, fy = x, y
        hsv_roi = frame_hsv[iy:fy, ix:fx]
        mask = cv.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)

# open camera
cameraNumber = 0
video_path = 'E:/Grace_Praise/HGU/23년 1학기/IAIA/Final/hw_setting_after.mp4'
#cap = cv.VideoCapture(video_path)
cap = cv.VideoCapture(cameraNumber) # window는 cv.CAP_DSHOW 추가 해줘야 함
fourcc = cv.VideoWriter.fourcc('M','J','P','G')
cap.set(cv.CAP_PROP_FOURCC, fourcc)
cap.set(cv.CAP_PROP_FPS, 60.0) 

# Check if the video capture was successful
if not cap.isOpened():
    print("Unable to open video file")
    exit()

# Get frame width, height, and frames per second (fps)
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv.CAP_PROP_FPS))
print("Video properties - Width:", width, "Height:", height, "FPS:", fps)

# Output video properties
output_width = width
output_height = height
output_fps = fps
output_filename = 'output.mp4'
# fourcc = cv.VideoWriter_fourcc(*'XVID')
output_video = cv.VideoWriter(output_filename, fourcc, output_fps, (output_width, output_height))

# Create a window with the same size as the video frame
cv.namedWindow('Video', cv.WINDOW_NORMAL)
cv.resizeWindow('Video', width, height)

cv.setMouseCallback('Video', select_roi)

def predict_path():
    global previous_position, current_position, previous_velocity, moved_left_since_path, path_drawn_time, path_line, reflected_path_line

    velocity = None
    # Set the movement threshold to x pixels
    movement_threshold = 10  
    
    # set roi in field  
    roi_x1 = line_x1
    roi_y1 = line_y1
    roi_x2 = line_x2
    roi_y2 = line_y2
      
    if contours:
        for cnt in contours:
            area = cv.contourArea(cnt)
            # filter outlier contours
            if 200 <= area <= 500:
                x, y, w, h = cv.boundingRect(cnt)
                # check object in roi
                if (roi_x1 <= x <= roi_x2) and (roi_y1 <= y <= roi_y2):  
                    
                    # Calculate the center of the bounding box
                    center_x = x + w // 2
                    center_y = y + h // 2
                    current_position = (center_x, center_y)
                    
                    cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    # predict the path when object is moving
                    if previous_position is not None:
                        velocity = (current_position[0] - previous_position[0], current_position[1] - previous_position[1])
                        if velocity[0] < 0:
                            moved_left_since_path = True
                        if velocity[0] > movement_threshold and moved_left_since_path:
                            
                            # Extend the line to the boundary
                            if velocity[0] == 0:  # If the object is not moving horizontally
                                boundary_x = previous_position[0]
                                boundary_y = roi_y1 if velocity[1] < 0 else roi_y2
                                reflected_slope = float('inf')
                                reflected_boundary_x = boundary_x
                                reflected_boundary_y = boundary_y
                            else:
                                slope = velocity[1] / velocity[0]
                                
                                # Calculate the x-coordinate on the boundary for the line
                                if slope == 0:  # If the slope is 0
                                    boundary_x = previous_position[0]
                                    boundary_y = previous_position[1]
                                else:
                                    if velocity[1] < 0:  # If the object is moving upwards
                                        boundary_x = previous_position[0] + (roi_y1 - previous_position[1]) / slope
                                    else:  # If the object is moving downwards
                                        boundary_x = previous_position[0] + (roi_y2 - previous_position[1]) / slope
                                    boundary_y = roi_y1 if velocity[1] < 0 else roi_y2
                                boundary_x = int(boundary_x)
                                boundary_y = int(boundary_y)

                                # Calculate the reflected path
                                if slope == 0:  # If the slope is 0
                                    reflected_slope = float('inf')
                                    reflected_boundary_x = boundary_x
                                    reflected_boundary_y = roi_y1 if velocity[1] < 0 else roi_y2
                                else:
                                    reflected_slope = -slope
                                    reflected_boundary_y = boundary_y + reflected_slope * (roi_x2 - boundary_x)
                                    reflected_boundary_x = boundary_x + (reflected_boundary_y - boundary_y) / reflected_slope

                                reflected_boundary_x = max(roi_x1, min(roi_x2, reflected_boundary_x))
                                reflected_boundary_y = max(roi_y1, min(roi_y2, reflected_boundary_y))

                                reflected_boundary_x = int(reflected_boundary_x)
                                reflected_boundary_y = int(reflected_boundary_y)

                                reflected_path_line = ((boundary_x, boundary_y), (reflected_boundary_x, reflected_boundary_y))

                                path_line = (previous_position, (boundary_x, boundary_y))  # Store path line coordinates
                                path_drawn_time = time.time()  # Update the path drawn time
                                moved_left_since_path = False  # Reset the variable once the path has been drawn

                                
                    previous_position = current_position
                    previous_velocity = velocity

line_x1 = 50
line_y1 = 90
line_x2 = width - 50
line_y2 = height - 110        
       
while True:
    start_time = time.time()
    ret, frame = cap.read()

    if not ret:
        print("End of video")
        break

    #frame = cv.flip(frame, 1)
    frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # boundary line
    cv.line(frame, (line_x1, line_y1), (line_x2, line_y1), (153, 0, 204), 2)
    cv.line(frame, (line_x1, line_y2), (line_x2, line_y2), (153, 0, 204), 2)
    
    if drawing:
        cv.rectangle(frame, (ix, iy), (fx, fy), (255, 0, 0), 2)

    if roi_hist is not None:
        back_proj = cv.calcBackProject([frame_hsv], [0], roi_hist, [0, 180], 1)
        _, threshold = cv.threshold(back_proj, 1, 255, cv.THRESH_BINARY)
        contours, _ = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        predict_path()
        
    if path_drawn_time and time.time() - path_drawn_time <= 1:  # If the path was drawn within the last 1 second
        cv.line(frame, *path_line, (152, 251, 152), 2)  # Draw the path line
        cv.line(frame, *reflected_path_line, (152, 251, 152), 2)  # Draw the path line

    diff_time = time.time() - start_time

    if diff_time > 0:
        fps = 1 / diff_time

    cv.putText(frame, f'FPS: {fps:.2f}', (int(width/10), int(height/12)), user_font, 1, (100, 255, 0), 2)

    cv.imshow("Video", frame)

    output_video.write(frame)
     
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv.waitKey(0)

cap.release()
output_video.release()
cv.destroyAllWindows()
```

puck이 잘 인식 되지 않던 문제가 있었다. 카메라 하드웨어를 고정했더니 잘 인식됨

[https://drive.google.com/file/d/1EP2UKZGSfHSzZ7Q-JjjErfvXq67jdKEN/view?usp=sharing](https://sendanywhe.re/BP3R00MU)

https://sendanywhe.re/BP3R00MU

수정일 : 

```python
import cv2 as cv
import numpy as np
import time

class VideoProcessor:
    def __init__(self, cameraNumber=0):
        self.drawing = False
        self.ix, self.iy = -1, -1
        self.fx, self.fy = -1, -1
        self.frame_hsv = None
        self.roi_hist = None
        self.user_font = cv.FONT_HERSHEY_COMPLEX

        self.previous_position = (0, 0)  # Initialize previous_position variable
        self.current_position = None
        self.previous_velocity = None
        self.move_right = False
        self.path_drawn_time = None
        self.path_line = None
        self.reflected_path_line = None
        self.extra_reflected_path_line = None
        self.slope = None
        self.previous_slope = None
        
        # slope calculate
        self.slope_list = [] 
        self.stored_position = None 
        self.flag = 0
        self.path_drawn = False
               
        cap = cv.VideoCapture(cameraNumber, cv.CAP_DSHOW)
        fourcc = cv.VideoWriter.fourcc('M','J','P','G')
        cap.set(cv.CAP_PROP_FOURCC, fourcc)
        cap.set(cv.CAP_PROP_FPS, 60.0) 
        cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0.75) 
        # cap.set(cv2.CAP_PROP_EXPOSURE, -11.0)
        print(cap.get(cv.CAP_PROP_EXPOSURE))

        if not cap.isOpened():
            print("Unable to open video file")
            
            exit()

        self.width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(cap.get(cv.CAP_PROP_FPS))
        print("Video properties - Width:", self.width, "Height:", self.height, "FPS:", self.fps)

        self.cap = cap

        self.output_width = self.width
        self.output_height = self.height
        self.output_fps = self.fps
        self.output_filename = 'output2.mp4'
        self.output_video = cv.VideoWriter(self.output_filename, fourcc, self.output_fps, (self.output_width, self.output_height))

        cv.namedWindow('Video', cv.WINDOW_NORMAL)
        cv.resizeWindow('Video', self.width, self.height)

        cv.setMouseCallback('Video', self.select_roi)

        #boundary
        self.line_x1 = 40
        self.line_y1 = 75
        self.line_x2 = self.width - 50
        self.line_y2 = self.height - 125        
       
    def select_roi(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y
            self.fx, self.fy = x, y
        elif event == cv.EVENT_MOUSEMOVE:
            if self.drawing == True:
                self.fx, self.fy = x, y
        elif event == cv.EVENT_LBUTTONUP:
            self.drawing = False
            self.fx, self.fy = x, y
            hsv_roi = self.frame_hsv[self.iy:self.fy, self.ix:self.fx]
            mask = cv.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
            self.roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
            cv.normalize(self.roi_hist, self.roi_hist, 0, 255, cv.NORM_MINMAX)
            
    def slope_avg(self, new_slope):
        # Append new_slope to the list
        if len(self.slope_list) <= 4:
            self.slope_list.append(new_slope)

        if len(self.slope_list) == 4:
            self.stored_position = self.current_position
            self.path_drawn = False  
            
        # Compute the average of the slopes
        self.slope = sum(self.slope_list) / len(self.slope_list)
        #print(str(len(self.slope_list)))
        #print(self.slope)
        
    def predict_path(self, contours):
        roi_x1 = self.line_x1
        roi_y1 = self.line_y1
        roi_x2 = self.line_x2
        roi_y2 = self.line_y2
        
        hit_border = None
        hit_border2 = None
        reflected_y2 = None
        
        if contours:
            for cnt in contours:
                area = cv.contourArea(cnt)
                # filter outlier contours
                if 200 <= area <= 400:
                    x, y, w, h = cv.boundingRect(cnt)
                    # check object in roi
                    if (roi_x1 <= x <= roi_x2) and (roi_y1 <= y <= roi_y2):  
                        
                        # Calculate the center of the bounding box
                        center_x = x + w // 2
                        center_y = y + h // 2
                        self.current_position = (center_x, center_y)

                        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        
                        x_move = self.current_position[0] - self.previous_position[0]
                        move_distance = float(np.sqrt((self.current_position[0] - self.previous_position[0])**2+(self.current_position[1] - self.previous_position[1])**2))
                        #print(f"x axis: {(self.current_position[0] - self.previous_position[0])} move dist: {(move_distance):.2f}")
                        
                        # Reset slope list and drawn paths if object moves left more than -3
                        if x_move < -3:
                            self.slope_list = []
                            self.path_line = None
                            self.reflected_path_line = None
                            self.path_drawn = False 
            
                        # If puck is moving to the right
                        if self.previous_position is not (0,0) and x_move >= 3 and move_distance >= 4.5:
                            self.puck_move = True
                            self.slope_avg((self.current_position[1] - self.previous_position[1]) / (self.current_position[0] - self.previous_position[0]))
                        else:
                            self.puck_move = False

                        #print("puck move flag: "+str(self.puck_move))
                        
                        # If puck is moving
                        if self.puck_move and len(self.slope_list) > 0 and not self.path_drawn: 
                            
                            if self.slope != 0 and self.slope < 0:
                                predicted_x = self.previous_position[0] + (roi_y1 - self.previous_position[1]) / self.slope 
                            elif self.slope != 0 and self.slope > 0:
                                predicted_x = self.previous_position[0] + (roi_y2 - self.previous_position[1]) / self.slope 
                            else:
                                predicted_x = self.previous_position[0]

                            # Ensure that predicted_x does not exceed the boundaries.
                            predicted_x = min(max(predicted_x, roi_x1), roi_x2)
                                
                            # Predicted path line (in boundary)
                            predicted_y1 = self.current_position[1] + self.slope * (roi_x1 - self.current_position[0])
                            predicted_y2 = self.current_position[1] + self.slope * (roi_x2 - self.current_position[0])
                            predicted_y1 = max(roi_y1, min(roi_y2, predicted_y1))
                            predicted_y2 = max(roi_y1, min(roi_y2, predicted_y2))

                            
                            # Remember the border (upper or lower) that was hit
                            hit_border = roi_y1 if predicted_y2 == roi_y1 else roi_y2
                            
                            if hit_border is not None and predicted_x != roi_x2:
                                reflected_x2 = roi_x2
                                reflected_y2 = hit_border - self.slope * 0.4 * (roi_x2 - self.current_position[0])

                                if reflected_y2 <= roi_y1:
                                    reflected_y2 = roi_y1
                                    if self.slope != 0:
                                        reflected_x2 = self.current_position[0] + (reflected_y2 - hit_border) / -self.slope * 1.4  # reflection
                                elif reflected_y2 >= roi_y2:
                                    reflected_y2 = roi_y2
                                    if self.slope != 0:
                                        reflected_x2 = self.current_position[0] + (reflected_y2 - hit_border) / -self.slope * 1.4 # reflection

                                #reflected_y2 = max(roi_y1, min(roi_y2, reflected_y2))
                                self.reflected_path_line = ((int(predicted_x), int(predicted_y2)), (int(reflected_x2), int(reflected_y2)))
                            else:
                                self.reflected_path_line = None
                            
                            # if reflected_y2 is not None:
                            #     hit_border2 = roi_y1 if reflected_y2 == roi_y1 else roi_y2

                            # if hit_border2 is not None and reflected_x2 != roi_x2:           
                            #     reflected_x3 = roi_x2
                            #     reflected_y3 = hit_border2 + self.slope * (roi_x2 - self.current_position[0])
                                
                                # if reflected_y3 >= roi_y1:
                                #     reflected_y3 = 
                                    
                                # elif reflected_y3 <= roi_y2:
                                #     reflected_y3 = 
                                   
                            #     self.extra_reflected_path_line = ((int(reflected_x2), int(reflected_y2)), (int(reflected_x3), int(reflected_y3)))
                            # else:
                            #     self.extra_reflected_path_line = None

                            self.path_line = ((self.current_position[0], self.current_position[1]), (int(predicted_x), int(predicted_y2)))
                            
                            self.path_drawn = True
                            
                        else:
                            # Reset paths
                            self.predicted_path = None
                            self.reflected_path = None
                            

                        self.previous_position = self.current_position
                        self.path_drawn_time = time.time()

    def goal(self):
        goal_x = self.line_x2
        goal_y1 = 0
        goal_y2 = self.height
        
        cv.line(frame, (goal_x, goal_y1), (goal_x, goal_y2), (0, 255, 0), 1)

    def decide_flag(self):
        roi_width = self.line_y2 - self.line_y1
        y_div = roi_width // 3
        
        robot_area1 = [int(self.width / 10 * 9), 0, self.width, self.line_y1 + y_div]
        robot_area2 = [int(self.width / 10 * 9), self.line_y1 + y_div, self.width, self.line_y1 + 2 * y_div]
        robot_area3 = [int(self.width / 10 * 9), self.line_y1 + 2 * y_div, self.width, self.height]
        
        cv.rectangle(frame, (robot_area1[0], robot_area1[1]), (robot_area1[2], robot_area1[3]), (255, 255, 255), 2)
        cv.rectangle(frame, (robot_area2[0], robot_area2[1]), (robot_area2[2], robot_area2[3]), (255, 255, 255), 2)
        cv.rectangle(frame, (robot_area3[0], robot_area3[1]), (robot_area3[2], robot_area3[3]), (255, 255, 255), 2)

        final_point = None
        
        if self.path_line is not None and self.reflected_path_line is None:
            final_point = self.path_line[1]  

        elif self.path_line is not None and self.reflected_path_line is not None:
            final_point = self.reflected_path_line[1]  

        elif self.path_line is not None and self.reflected_path_line is not None and self.extra_reflected_path_line is not None:
            
            final_point = self.extra_reflected_path_line[1]  

            
        if final_point:
            if robot_area1[1] <= final_point[1] <= robot_area1[3]:
                self.flag = 1
                cv.putText(frame, "Flag 1", (500,200), self.user_font, 0.7, (255, 255, 0), 2)
            elif robot_area2[1] <= final_point[1] <= robot_area2[3]:
                self.flag = 2
                cv.putText(frame, "Flag 2", (500,200), self.user_font, 0.7, (255, 255, 0), 2)
            elif robot_area3[1] <= final_point[1] <= robot_area3[3]:
                self.flag = 3
                cv.putText(frame, "Flag 3", (500,200), self.user_font, 0.7, (255, 255, 0), 2)
        else:
            # Set a default flag in case there is no path line or reflected path line
            self.flag = 2
                                               
    def process_video(self):
        while True:
            global frame
            start_time = time.time()
            ret, frame = self.cap.read()

            if not ret:
                print("End of video")
                break

            #frame = cv.flip(frame, 1)
            self.frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

            cv.line(frame, (self.line_x1, self.line_y1), (self.line_x2, self.line_y1), (153, 0, 204), 2)
            cv.line(frame, (self.line_x1, self.line_y2), (self.line_x2, self.line_y2), (153, 0, 204), 2)

            self.goal()

            self.decide_flag()
            if self.drawing:
                cv.rectangle(frame, (self.ix, self.iy), (self.fx, self.fy), (255, 0, 0), 2)

            if self.roi_hist is not None:
                back_proj = cv.calcBackProject([self.frame_hsv], [0], self.roi_hist, [0, 180], 1)
                _, threshold = cv.threshold(back_proj, 1, 255, cv.THRESH_BINARY)
                contours, _ = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

                self.predict_path(contours)
            
            if self.path_line is not None: 
                cv.line(frame, *self.path_line, (152, 251, 152), 2)
            if self.reflected_path_line is not None:
                cv.line(frame, *self.reflected_path_line, (152, 251, 152), 2)
            # if self.extra_reflected_path_line is not None:
            #     cv.line(frame, *self.extra_reflected_path_line, (152, 251, 152), 2)
            diff_time = time.time() - start_time

            if diff_time > 0:
                fps = 1 / diff_time

            cv.imshow("Video", frame)

            self.output_video.write(frame)
        
            key = cv.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                cv.waitKey(0)

        self.cap.release()
        self.output_video.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    processor = VideoProcessor()
    processor.process_video()
```


