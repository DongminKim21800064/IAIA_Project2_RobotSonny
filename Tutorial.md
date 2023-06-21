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

3. "indy10_moveit_config.zip", "indy_driver.zip", "indy_utils.zip"을 catkin_ws / src 파일 안에 압축 해제.

4. "airhockey.sh"파일을 다운 후 catkin_ws 파일에 넣기
  - 파일 주소 확인. 본인 환경에 맞게 주소 수정
  - 연결하는 Indy-10 IP 수정
  
  ```bash
  # Run the Python script
  python3 /home/"본인 주소"/catkin_ws/src/indy_driver/src/indy_set_velocity.py
  ```

5. 
