# IAIA_Project2_Robot Byeong-Gi(Airhockey Robot)

**2023.06.13.15:13 TUE**

**Handong Global University, School of Mechanical and Control Engineering, 2023-1 Industrial AI & Automation**

Proffesor | Young-Keun Kim

21800064 | 김동민

21800805 | 황승언

21801017 | 김은찬

![image](https://user-images.githubusercontent.com/84533279/173822161-78baf6a8-6bdf-46b9-a990-63b9ed181984.png)

## 1. Introduction

이 Respository는 한동대학교 2023년 1학기에 진행된 Industrial AI & Automation 수업의 기말 프로젝트인, **Robot Byeong-Gi (Airhockey Robot)** 에 대한  **Tutorial**  이 포함되어 있습니다.

Automation 프로젝트는 Indy-10(Neuromeka)의 6축 협동로봇팔을 제어하여 특정 임무를 수행하는 시나리오를 구성하며 로봇팔 제어 경험을 학습하기 위함과 저학년 학생들에게 로봇 체험을 통해 긍정적인 경험을 선사하여 기계제어공학부의 홍보를 목적으로 한다.

우리는 **"참여성"**, **"실현가능성"** 을 중점으로 프로젝트 주제를 선정하였다. 이에 **에어하키로봇**이 참가자가 쉽게 게임을 진행 할 수 있으며, 협동로봇으로 구현할 수 있을것이라 판단하였다.

영상처리 기법으로 물체의 이동경로를 예측하여, 예측 위치로 로봇팔을 이동시켜 물체를막아내는 것을 기본 목적으로 정하였다.



## 1) Hardware

**Co-Robot**
* Indy-10

Indy-10 로봇 팔은 산업용 로봇 팔 중 하나로, 다양한 작업을 수행하는데 사용되는 로봇 팔이다. 이 로봇 팔은 산업 자동화 분야에서 널리 활용되며, 높은 정밀성과 성능을 제공한다.
Indy-10 로봇 팔은 다관절 구조를 가지고 있어 다양한 자세와 움직임을 구현할 수 있다. 이로 인해 복잡한 작업이나 다양한 위치에 대한 접근이 가능하며, 작업 공간 내에서의 유연성을 제공한다.

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/35fa5e27-5bc3-4d0f-a8c8-6290a74c6d2e)



**Grippers**
* Vacuum

Vacuum Gripper는 골이 먹힌 Flag에서 Puck을 줍는 동작에서 사용된다. 제공된 "indy_driver demo_grip.py" 코드를 간단히 수정하여 Vacuum Gripper를 사용할 수 있다.


**AirHockey Table**

에어하키 테이블로는 11번가에서 판매하는 30만원대의 제품을 구매하여 사용하였다. 카메라로 Puck의 이동경로를 예측 및 통신하여 로봇팔을 제어하는 과정에서 딜레이가 생기는 환경을 고려하여 중대형 크기의 제품을 선정하였다. 또한, 접이식으로써 보관 및 이동에도 용이하다는 장점이 있다.


![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/4e3ffd42-2178-48a4-9c35-9f479365e358)

**URL** : https://www.11st.co.kr/products/5729217404?NaPm=ct=lhk3yb9k|ci=01f4068eac4029dc1c366ec30dee720cb879cad5|tr=slct|sn=17703|hk=6d9d370784625290fee06e082f7238cd3c822bf0&utm_term=&utm_campaign=%B3%D7%C0%CC%B9%F6pc_%B0%A1%B0%DD%BA%F1%B1%B3%B1%E2%BA%BB&utm_source=%B3%D7%C0%CC%B9%F6_PC_PCS&utm_medium=%B0%A1%B0%DD%BA%F1%B1%B3

**Camera**
* Logitech Brio

**End-Effector**
* 3d Printed Airhocket Paddle

로봇팔의 브라켓 크기를 실측하여 이에 맞게 모델링을 진행하였다. 하키채를 "Paddle"이라고 하는데, 로봇팔의 느린 움직임을 보완하기 위해 기본적인 Paddle에 비해 비교적 큰 크기로 모델링을 하였다.

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/556c4dad-de95-46b4-a35b-26ed7ac3c39c)



**참고사항**
에어하키의 공 이름을 **PUCK**이라고 한다.


## 2) Software

* Ubuntu (Linux Environment)
* Python 3.x
* Given ROS Libraries

아래는 딥러닝을 위해 사용하고자했던 소프트웨어이다.
* Cuda 11.8
* Yolo V8


## 3) Flow Chart

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/facad01f-a214-4cc7-a382-84f436f15243)



![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/98dc770d-e2d1-4e78-859c-9b8fa5ae34dd)


1. Predict puck paths by analyzing positional changes across multiple frames based on the segmented puck’s center.

2. Determine the final path considering the angle of incidence with the wall.

3. Identify the point closest to the predicted path among multiple points in front of the goal.

4. Command the robot arm to move to the closest point on the path.

5. When a goal is scored, the robot is moved to pick up the puck using a Vacuum Gripper and then place it back on the table

## 2. Image Processing Part

- 아래의 과정을 진행하여, ROS상에서 영상처리를 실행할 수 있는 환경을 세팅 및 Puck 이동경로 추적을 진행하였다.

- 또한, 인터페이스 기능을 추가하여 좋은 외형을 구축하기 위해 노력했다.

   -Using OpenCV (Color Segmentaion)
https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/blob/main/OpenCV_color_segmentation.md

 
 
**딥러닝**

초기에는 딥러닝을 활용한 영상처리를 계획 하였으나, 이를 사용할 경우 연산량 증가로 인해 처리속도가 매우 느려져 딥러닝 파트를 프로젝트에서 제외 하였다.

- 딥러닝을 위한 ROS 상의 CUDA 설치법
https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/blob/main/CUDA_11.8_Installation.md

- Yolo v8 및 Open cv 카메라 세팅
https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/blob/main/Camera_yolo_OpenCV.md

## 3. Automation Part

- 키보드입력 Flag를 통해 로봇 팔 구동 (W/O 이미지 프로세싱)
https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/blob/main/Robot_Automation.md
- 로봇 구동 속도 향상 방법


## 4. 최종 코드 및 설명

## 5. Demonstration
[![Video Label](http://img.youtube.com/vi/lsEivK4yrS4/0.jpg)](http://img.youtube/lsEivK4yrS4)
https://youtu.be/lsEivK4yrS4 


## 6. Trouble Shooting

1) 로봇 동작 속도 Exceeding
   - ROS 상에서 동작 속도 향상을 위해 코드 수정을 진행하였으나, 구현하지 못했다.
   - Indy10 Neuromeka 사이트이 "Doc"에 들어가면, Indy10에 관련한 인터페이스 코드 설명이 있다.
   - Neuromeka Site : http://docs.neuromeka.com/3.0.0/kr/Python/section1/
   - IAIA Code URL : https://github.com/hyKangHGU/Industrial-AI-Automation_HGU/tree/main/indy_utils
   - "Indy10_set_velocity.py"에서 "set_joint_vel_level(#)  # 1 ~ 9"을 확인할 수 있다.
   - Indy10 로봇은 1부터 9까지의 속도 레벨이 존재하며, 9가 최대속도이다. 해당 코드를 수정하여 속도 조절이 가능하다.

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/5ce9a220-fd8b-42de-bea5-7519282c5ba8)



2) 로봇을 오래 사용할 경우 반응속도가 느려진다.
   - 정확한 이유를 알 수는 없지만, 로봇이 입력 위치와 실제 위치 오차를 줄이는 제어 과정에서 오류가 누적되어 연산시간이 늘어난 것이라 추측된다.
   - 알고리즘 상에서 로봇 동작을 멈추는 코드를 알맞지 않게 사용하면, 대기 시간이 길어져 동작 반응이 느려질 수 있다.

3) Puck 이동 이동경로 예측 상의 문제
   2-1) 기울어진 Table로 인한 입,반사각 Error
      - 에어하키 테이블의 경사로 인해, 예상했던 입,반사각과 다른 경로로 Puck이 이동하였다. 이에 테이블의 경사를 측정하여 거의 수평이 되도록 맞추는 작업을 진행했다.
      - 이를 통해 이동경로 정확성을 향상시킬 수 있었다.
   
  ![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/89f1925f-3892-4592-ba70-ac7ddae5146d)

## 7. Appendix

