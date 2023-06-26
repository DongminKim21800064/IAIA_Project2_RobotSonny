# Robot Sonny Tutorial


1. IAIA 깃허브에서 파일 다운 후 "catkin_ws" 파일 생성

2. IAIA 깃허브 튜토리얼에 따라 아래 코드 실행
  - 실행 후, catkin_ws / src에 파일 생성 확인
##### Create a ROS Workspace

```bash
$ mkdir -p ~/catkin_ws/src
$ cd ~/catkin_ws/
$ catkin_make
```

3. "airhockey"파일을 다운 받고 catkin_ws / src 파일 안에 압축 해제.

4. "airhockey.sh"파일을 다운 후 catkin_ws 파일에 넣기
  - 파일 주소 확인. 본인 환경에 맞게 주소 수정
  - 연결하는 Indy-10 IP 수정
  
  ```bash
  # Run the Python script
  python3 /home/"본인 주소"/catkin_ws/src/indy_driver/src/indy_set_velocity.py
  ```

### 실행

```bash

./airhockey.sh

```


### 코드 실행 에러 해결 방법

1. 몇몇 패키지가 미설치시, 아래 코드를 참고하여 설치할 수 있다. 
``` bash
sudo apt install ros-noetic-industrial-robot-client
sudo apt install ros-noetic-moveit-visual-tools
sudo apt install ros-noetic-moveit-commander
```
2. Permission Denied Error
   - Deny된 py 형식의 파일에 마우스 우측클릭 --> Properties --> permission 허용에 관한 박스 on
     

### 에어하키 하드웨어 세팅 방법

1. 테이블 세팅
   1-1. 직접교시를 통해 Indy-10 로봇을 기준 위치로 이동시킨다. ( ex.[0, 0, tau/4, 0, tau/4, 0])
   1-2. 로봇의 중심과 테이블의 중심위치를 맞춘다.
   1-3. 전자각도기를 이용하여 테이블의 기울기를 0도에 가깝게 맞춘다. -> 이는 퍽 예측경로 정확도와 밀접한 연관이 있다.
   1-4. 테이블이 기울어져 있을경우, 테이블 다리에 적당한 물체를 두어 수평을 맞춘다.

2. 퍽 Segmentation
   2-1. 파란계열의 퍽을 테이블 위에 올려두고, 퍽의 영역을 드래그로 지정한다.
   2-2. 의도치 않게 퍽이 움직였을 때, 자동으로 예상경로가 생성되어 로봇이 작동할 수 있다. 이러한 경우에는 영상에 퍽이 안나오도록 가린 채로, 슈팅라인 바깥으로 이동시키면 된다.

3. 로봇 세팅
   3-1. 로봇 기준 우측, 중앙, 좌측 위치를 지정해주어야 한다. 패들이 테이블에 너무 밀착될 경우, 로봇팔 이동 시 테이블과 함께 카메라가 흔들리게되므로 적절한 거리를 잘 찾아야 한다.
   3-2. 골이 먹힌 상황에서의 로봇 위치 선정 시, 로봇이 이동하면서 테이블과 부딫이지 않게 안전한 위치로 세팅해야 한다.

   
### 게임 진행 시 유의사항

**!! CAUTION !!**
**이 프로젝트는 승부차기를 목적으로 설계되었습니다.**

1. 퍽은 슈팅 라인 뒷쪽 박스 안에 위치한 상태에서 쳐야 로봇의 정확성이 높아진다.

2. 퍽을 너무 강하게 칠 경우, 카메라의 프레임이 퍽의 속도를 따라가지 못해 경로 예측이 부정확해진다. 적절한 속도로 게임을 진행해야 한다.

3. 골을 넣었을 경우, 해당 상황을 인식하기 위해 로봇에게 잠시 시간이 필요하다. 
