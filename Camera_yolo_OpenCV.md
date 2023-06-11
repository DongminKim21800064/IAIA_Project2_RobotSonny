### Yolo v8 사용 방법

```bash
pip3 install ultralytics
```

### Pytorch gpu 확인

단 gpu를 사용하는 것을 확인하려면 아래 코드에서 다음과 같은 결과가 나와야 한다

```python
print(tf.__version__)
print(torch.__version__)
```

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/2bfb1c6c-2071-47cf-aa02-545ddc31c9d5)

**진행 될 Flow**

**수비**

1. segmentation 된 puck의 중점을 기준으로 여러 프레임에서의 위치 변화를 통해 경로 예측
2. 벽에 부딪히는 입사각을 통해 최종 경로 확인
3. 골대 앞의 여러 포인트 가운데서 예측 경로가 어떤 포인트와 제일 가까운지 파악
4. 경로와 제일 가까운 포인트로 로봇팔 움직이도록 명령

open cv 카메라 세팅 변경 방법

[비디오 읽기 - 속성 플래그 | 076923 Documentation](https://076923.github.io/docs/VideoCaptureProperties)

[Logitech Brio OpenCV Capture Settings](https://stackoverflow.com/questions/48327616/logitech-brio-opencv-capture-settings)

[Setting Camera Parameters in OpenCV/Python](https://stackoverflow.com/questions/11420748/setting-camera-parameters-in-opencv-python)
