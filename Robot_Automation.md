# Robot Automation
ver. 23.06.11

로봇 팔의 움직임을 제어하는 방법은 총 3가지가 있다

- **End-Point 절대 좌표계 제어**
    - End-point의 절대 좌표를 입력하여 로봇 팔의 위치를 제어하는 방법이다.
    - 이 방법은 큰 Risk 를 갖고 있다. 일정 위치 좌표를 입력하여 움직일 때 최종 좌표에는 잘 도달하지만, 그 과정이 Random 하여 프로젝트에 적합하지 않은 방법이다.
- **End-Point 상대 좌표계 제어**
    - End-point의 현재 좌표계에 대한 상대적인 좌표에 따라 움직인다.
    - 절대 좌표 제어와 마찬가지로 그 과정이 일정하지 않아, 프로젝트에 적절하지 않다.
- **Axis Angle 제어**
    - 로봇 팔의 6개 축에 대하여 각도 제어를 실행하는 방법으로써, 이상적인 경로대로 제어가 가능하다.
    - Axis Angle 제어에 유의해야 할 점은 다음과 같다. 실행 시, 1번 축(End-point에 가장 가까운 축)부터 6번 축 까지의 축 각도가 직렬적으로 행해진다. 따라서, 현재 축 각도에 대한 목표 축 각도에서 각도가 변화는 축이 최소화 되도록 알고리즘을 구성해야 한다.

위 3가지 제어 방법 중 **Axis Angle** 제어가 가장 적합하다고 판단하여 이를 바탕으로 설계를 진행하였다.

---

### 로봇 구동 전략

https://www.youtube.com/watch?v=I8OqLvxsO2A&t=334s

위 영상은 유명 유튜버의 영상에 등장하는 에어하키 퀀텀 로봇 키퍼이다. 이 로봇은 Indy_10로봇과 달리 작동 속도가 매우 빠르다는 특징이 있다. 

Robot Sonny 프로젝트를 진행하기 위해서는 느린 로봇의 움직임으로도 Puck을 효과적으로 막을 수 있어야 한다.

위 영상에서는 로봇이 Puck을 막음과 동시에 앞으로 밀어 공격적인 동작을 수행한다. 하지만, Indy10로봇에서 실험 한 결과, 앞으로 미는 동작이 매우 느려 퍽이 앞으로 나아가지 않는 문제점이 있었다. 따라서 Puck이 날아오는 위치를 예측하여 해당 위치에 도달하는 것을 목표로 하였다.

따라서 위치 Flag를 3개 정의 하여, 각각 Left, Right, Front 방면으로 날아오는 Puck을 막게 끔 설계하고자 한다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/d1ed9e9e-37cf-47d6-8ff1-c337ab523d7e/Untitled.png)

---

### Demo Code test

영상 처리 파트와 연동하여 진행 하기 전, Automation 파트를 독립적으로 진행하여 테스트해 보기 위해 아래와 같은 코드를 구현하였다.

Camera 파트의 경우 **Demo 2: Move with Camera**의 코드를 참고하여 만들었다.

영상처리 Flag를 키보드 입력 Flag로 대체하였다. 

키보드 입력 Flag를 msg로 송신하여 Automation 파트에서 받게 한다.

로봇이 테이블을 바라보는 기준으로, Flag1은 우측, Flag2는 정면, Flag3은 좌측에 대해 수비를 진행한다.  Flag4의 경우 골이 먹혔을 경우를 가정하며, 로봇 팔이 Puck을 담은 박스로 이동한 후 Vacuum Gripper를 이용해 Puck을 잡는 동작을 수행한다. 이후 Flag2의 위치로 이동하여 Puck을 Table 위로 놓는다. 

target_joints에 입력한 축의 각도는, 수업에서 제공되는 테블릿 어플리케이션 상에서 원하는 좌표로 이동 뒤 그 때의 각 축 각도를 옮겨 쓴 값이다.

camera

```python
import rospy
from sensor_msgs.msg import Image   # sensor_msgs 패키지로부터 Image 메시지 타입을 import
from cv_bridge import CvBridge, CvBridgeError     # cv_bridge 라이브러리 : OpenCV 이미지와 ROS 메시지 간의 변환 가능
import cv2 as cv                
import numpy as np
import os
import time
from airhockey.msg import flag_data

class Predict:

    def __init__(self):
        cap             = cv.VideoCapture(0)          # 카메라 연결을 위한 VideoCapture 객체 생성
        cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter.fourcc('M','J','P','G'))
        cap.set(cv.CAP_PROP_FPS, 60.0) 
        self.width      = cap.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height     = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.fps        = int(cap.get(cv.CAP_PROP_FPS))
        print('get cam fps: ', self.fps)
        self.user_font  = cv.FONT_HERSHEY_COMPLEX

        self.cap = cap

        self.pub_flag   = rospy.Publisher("robot_flag", flag_data, queue_size=10)
        self.flag       = flag_data()

    def run(self):

        rospy.init_node('detect', anonymous=True)  # 노드 이름 "camera_node"로 초기화
        rate = rospy.Rate(self.fps)                           # 루프 실행 주기 : 60hz

        while not rospy.is_shutdown():                  # ROS가 종료되지 않은 동안
            self.cur_time = time.time()	# 현재 시간을 
            self.prev_time = self.cur_time # use self.start_time instead of self.start_time_sub

            ret, frame = self.cap.read()                # 카메라로부터 이미지를 읽음
            if ret:                                     # 이미지가 정상적으로 읽혀진 경우
                try:

                    diff_time = time.time() - self.prev_time
                    fps = 0
                    if diff_time > 0:
                        fps = 1 / diff_time

                    cv.putText(frame, f'FPS : {fps:.2f}', (20, 90), self.user_font, 2,  (100, 255, 0), 2)
                    cv.imshow("Camera", frame)  # 변환된 이미지를 "Camera"라는 이름의 윈도우에 표시

                    key = cv.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
                    elif key == ord('s'):
                        cv.waitKey(0)
                    elif key == ord('1'):
                        self.flag.flag = 1
                        self.pub_flag.publish(self.flag)
                    elif key == ord('2'):
                        self.flag.flag = 2
                        self.pub_flag.publish(self.flag)
                    elif key == ord('3'):
                        self.flag.flag = 3
                        self.pub_flag.publish(self.flag)
                    elif key == ord('4'):
                        self.flag.flag = 4
                        self.pub_flag.publish(self.flag)

                        # 1ms 동안 키보드 입력 대기

                except:
                    print("Camera is Disconnected ...!")   

            rate.sleep()                                # 지정된 루프 실행 주기에 따라 대기  

if __name__ == '__main__':
    try:
        display = Predict()     # DisplayNode 클래스의 인스턴스 생성
        display.run()               # 노드 실행
    except rospy.ROSInterruptException:
        pass
```

robot_ 0607

```python
#!/usr/bin/env python3
#-*- coding:utf-8 -*- 
import rospy
from tf.transformations import *
from math import tau
from move_group_python_interface import MoveGroupPythonInterface
from airhockey.msg import flag_data

class Indy10_Move_With_Camera():
    def __init__(self):

        self.indy10_interface           = MoveGroupPythonInterface(real=True, gripper="Vaccum")

        self.sub_object_info            = rospy.Subscriber("robot_flag", flag_data, self.detection_callback)

        # init_pose_joints = [0, 0, tau/4, 0, tau/4, 0]          # tau = 2 * pi
        # self.indy10_interface.go_to_joint_state(init_pose_joints)

        self.flag_recv_msg = False
        self.flag = 0
  
        print("Initialization is completed!")

    def detection_callback(self, data):
        # print(f"message received: {data.x}, {data.y}")
        self.flag_recv_msg = True
        self.flag = data.flag

    # Degree Converter
    deg = tau/360  # For example, entering 90*deg will output 90 degrees.
            
    # Joint 각도 선언
    target_joints_1 = [-10*deg, -11.23*deg, 120*deg,0*deg,-17.7*deg, 0*deg ]     # Flag1
    target_joints_2 = [0*deg, -11.23*deg, 120*deg,0*deg,-17.7*deg, 0*deg ]       # Flag2
    target_joints_3 = [10*deg, -11.23*deg, 120*deg,0*deg,-17.7*deg, 0*deg  ]     # Flag3
    target_joint_4_safe= [0*deg,-18.82*deg,79.01*deg,0*deg,119.15*deg,0*deg]     # @Flag4 --> Move safe loc
    target_joint_4_grip= [0*deg, -31.35*deg,135.52*deg, 0*deg, 64.98*deg, 0*deg] # @Flag4 --> Grip loc
            

    def run(self):
        while not rospy.is_shutdown():                  # ROS가 종료되지 않은 동안

            if self.flag_recv_msg:
                print(f"flag: {self.flag: d}")

                if self.flag == 1   :  ## Flag1에 대한 위치로 이동                            
                   self.indy10_interface.go_to_joint_state(target_joints_1)
                
                elif self.flag == 2 :  ## Flag2에 대한 위치로 이동                            
                   self.indy10_interface.go_to_joint_state(target_joints_2)
                
                elif self.flag == 3 :  ## Flag3에 대한 위치로 이동                            
                   self.indy10_interface.go_to_joint_state(target_joints_3)                    
                
                elif self.flag == 4 :  ## Goal 먹혔을 때의 로봇 동작
                    #input("============ Press the Enter ...")
                    self.indy10_interface.go_to_joint_state(target_joint_4_safe) # 테이블에 닿지 않는 안전한 위치로 로봇 팔 이동(For Grip)
                    self.indy10_interface.go_to_joint_state(target_joint_4_grip) # Grip할 위치로 이동
                    self.indy10_interface.grip_on()                              # Grip 실행
                    self.indy10_interface.go_to_joint_state(target_joint_4_safe) # 테이블에 닿지 않는 안전한 위치로 로봇 팔 이동(복귀)
                    self.indy10_interface.go_to_joint_state(target_joints_2)     # Flag2 위치로 이동
                    self.indy10_interface.grip_off()                             # Grip Off

                # target_pose_abs_xyz = [self.cmd_x, self.cmd_y, 0.54]

                # current_pose = self.indy10_interface.manipulator.get_current_pose().pose
                # current_quat = [current_pose.orientation.x, current_pose.orientation.y, current_pose.orientation.z, current_pose.orientation.w]
                # current_rpy = euler_from_quaternion(current_quat)
                # target_pose_abs_rpy = current_rpy
                
                # # self.msg_robot_state.move = 1
                # # self.pub_robot_state.publish(self.msg_robot_state)
                # self.indy10_interface.go_to_pose_abs(target_pose_abs_xyz, target_pose_abs_rpy)
                self.flag_recv_msg = False
                
                # self.msg_robot_state.move = 0
                # self.pub_robot_state.publish(self.msg_robot_state)

def main():
    try:
        
        Indy10 = Indy10_Move_With_Camera()
        Indy10.run()

    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
```

실행

```jsx
roscore
rosrun airhockey get_trajectory.py
roslaunch indy10_moveit_config moveit_planning_execution.launch robot_ip:=192.168.0.8
rosrun airhockey demo_move_with_camera.py
```

---
