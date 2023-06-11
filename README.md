# IAIA_Project2_RobotSonny(Airhockey Robot)

**2023.06.11. Sun**

**Handong Global University, School of Mechanical and Control Engineering, 2023-1 Industrial AI & Automation**

Proffesor | Young-Keun Kim

21800064 | 김동민

21800805 | 황승언

21801017 | 김은찬

![image](https://user-images.githubusercontent.com/84533279/173822161-78baf6a8-6bdf-46b9-a990-63b9ed181984.png)

## Introduction

이 Respository는 한동대학교 2023년 1학기에 진행된 Industrial AI & Automation 수업의 기말 프로젝트인, **Robot Sonny (Airhockey Robot)** 에 대한  **Tutorial**  이 포함되어 있습니다.

Automation 프로젝트는 Indy-10(Neuromeka)의 6축 협동로봇팔을 제어하여 특정 임무를 수행하는 시나리오를 구성하며 로봇팔 제어 경험을 학습하기 위함과 저학년 학생들에게 로봇 체험을 통해 긍정적인 경험을 선사하여 기계제어공학부의 홍보를 목적으로 한다.

우리는 **"참여성"**, **"실현가능성"** 을 중점으로 프로젝트 주제를 선정하였다. 이에 **에어하키로봇**이 참가자가 쉽게 게임을 진행 할 수 있으며, 협동로봇으로 구현할 수 있을것이라 판단하였다. 

### Hardware

**Co-Robot**
* Indy-10

**Grippers**
* Vacuum

**AirHockey Table**

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/4e3ffd42-2178-48a4-9c35-9f479365e358)

**URL** : https://www.11st.co.kr/products/5729217404?NaPm=ct=lhk3yb9k|ci=01f4068eac4029dc1c366ec30dee720cb879cad5|tr=slct|sn=17703|hk=6d9d370784625290fee06e082f7238cd3c822bf0&utm_term=&utm_campaign=%B3%D7%C0%CC%B9%F6pc_%B0%A1%B0%DD%BA%F1%B1%B3%B1%E2%BA%BB&utm_source=%B3%D7%C0%CC%B9%F6_PC_PCS&utm_medium=%B0%A1%B0%DD%BA%F1%B1%B3

**Camera**
* Logitech Brio

**End-Effector**
* 3d Printed Airhocket Paddle

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/556c4dad-de95-46b4-a35b-26ed7ac3c39c)



**참고사항**
에어하키의 공 이름을 **PUCK**이라고 한다.


### 1) Flow Chart

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/facad01f-a214-4cc7-a382-84f436f15243)



![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/98dc770d-e2d1-4e78-859c-9b8fa5ae34dd)


1. Predict puck paths by analyzing positional changes across multiple frames based on the segmented puck’s center.

2. Determine the final path considering the angle of incidence with the wall.

3. Identify the point closest to the predicted path among multiple points in front of the goal.

4. Command the robot arm to move to the closest point on the path.

5. When a goal is scored, the robot is moved to pick up the puck using a Vacuum Gripper and then place it back on the table



