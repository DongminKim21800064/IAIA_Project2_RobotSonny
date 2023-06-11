## ver 2023.05.20

## NVIDIA 그래픽하드 인식 확인

pci 업데이트를 진행하고 자신의 그래픽하드의 이름이 온전히 출력 되는지 확인해야함

우분투 그래픽 카드 GPU 이름 확인

```bash
lspci | grep -i VGA
```

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/8e9e36b1-548f-45fb-8f09-2ce13a9eba46)


자신이 알고 있는 그래픽 하드 이름이 나와야함 

만약 그냥 NVIDIA (자신이 모르는 이름)이 나오면 우분투에서 정확히 GPU를 인식하지 못한것임

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/0584c501-481b-4cce-81c7-2293c0075fc6)


다음 명령어를 입력해서 최신 pci로 업데이트를 진행함

```bash
sudo update-pciids
```

## CUDA 설치

### NVIDIA 설치한 거 전부 초기화

```bash
sudo apt-get purge nvidia*
sudo apt-get autoremove
sudo apt-get autoclean
sudo rm -rf /usr/local/cuda*
```

### **nouveau 비활성화**

```bash
sudo bash -c "echo blacklist nouveau > /etc/modprobe.d/blacklist-nvidia-nouveau.conf"
sudo bash -c "echo options nouveau modeset=0 >> /etc/modprobe.d/blacklist-nvidia-nouveau.conf"
```

위 명령어를 입력하고 다음 명령문을 입력해서 비활성화가 잘 되었는지 확인

```bash
cat /etc/modprobe.d/blacklist-nvidia-nouveau.conf
```

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/3a764b12-6379-401a-8f39-9e1ca1716a96)


### Key 추가

```bash
sudo wget -O /etc/apt/preferences.d/cuda-repository-pin-600 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
sudo add-apt-repository "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
```

### 자신의 컴퓨터에 맞는 driver list 확인

```bash
ubuntu-drivers devices
```

본인은 다음과 같이 출력됨

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/b217fe97-6ba8-4965-988f-c6b129069ba7)


### NVIDIA driver 설치

```bash
sudo apt-get install nvidia-driver-520
sudo apt-get install dkms nvidia-modprobe
sudo apt-get update
sudo apt-get upgrade
```

### 설치 완료 후 재부팅

```bash
sudo reboot now
```

### NVIDIA 그래픽 드라이버 확인

```bash
nvidia-smi
```

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/a2c5f19a-cce2-4b66-9200-4ba1fe720fa6)


### NVIDIA CUDA 링크

[CUDA Toolkit Archive](https://developer.nvidia.com/cuda-toolkit-archive)

본인은 오른쪽 상단에 11.8로 나와있어서 11.8로 진행함

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/0bab0e39-64be-42d5-990b-76bbc08e2c86)


```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda-repo-ubuntu2004-11-8-local_11.8.0-520.61.05-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2004-11-8-local_11.8.0-520.61.05-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2004-11-8-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda
```

### CUDA 설치 후

```bash
sudo apt update
sudo apt install build-essential
sudo apt-get install manpages-dev
```

### CUDA version 확인

```bash
ls /usr/local | grep cuda
```

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/a77ae071-df5b-4602-bb8b-74461c51c8ca)


### 환경변수 등록

만약 자신이 11.8 버전이 아니라면 아래의 11.8이라 적힌 부분을 자신의 버전에 맞춰서 변경하면 됨

```bash
sudo sh -c "echo 'export PATH=$PATH:/usr/local/cuda-11.8/bin'>> /etc/profile"
sudo sh -c "echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-11.8/lib64'>> /etc/profile"
sudo sh -c "echo 'export CUDARDIR=/usr/local/cuda-11.8'>> /etc/profile"
source /etc/profile
```

### nvcc version 확인

그냥 nvcc -V를 하면 cuda 정보가 나오지 않고 source /etc/profile 이걸 해야 나온다

```bash
nvcc -V
```

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/91e80f0d-d6a4-4737-ab0b-9fd1f78189e6)

### cuDNN 설치

cuDNN을 설치할 때 tensorflow GPU에 맞는 버전을 사용해야 한다 

현재는 cuDNN 8.6과 cuda 11.8을 가장 최신 버전으로 지원한다

https://www.tensorflow.org/install/source?hl=ko#linux

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/3ab4c50b-0de5-4c4b-b92b-dc7efb10b53c)

https://developer.nvidia.com/rdp/cudnn-download

로그인 필요

본인은 v8.6.0에서 **[Local Installer for Linux x86_64 (Tar)](https://developer.nvidia.com/downloads/compute/cudnn/secure/8.8.1/local_installers/11.8/cudnn-linux-x86_64-8.8.1.3_cuda11-archive.tar.xz/)** 이거를 다운

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/cf5544f6-7bb5-4584-9efe-9280a065bd8c)


### cuDNN 8.6.0 CUDA11.8 을 설치하는 경우

자신이 다운 받은 파일에 맞게 파일이름을 변경해야 한다

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/ddd9972c-a44f-4501-9355-5e64995e0be3)


```bash
cd Downloads/
tar -xf cudnn-linux-x86_64-8.6.0.163_cuda11-archive.tar.xz
sudo cp cudnn-linux-x86_64-8.6.0.163_cuda11-archive/include/* /usr/local/cuda-11.8/include
sudo cp cudnn-linux-x86_64-8.6.0.163_cuda11-archive/include/* /usr/local/cuda/include
sudo cp -P cudnn-linux-x86_64-8.6.0.163_cuda11-archive/lib/* /usr/local/cuda-11.8/lib64
sudo cp -P cudnn-linux-x86_64-8.6.0.163_cuda11-archive/lib/* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda-11.8/lib64/libcudnn*
sudo chmod a+r /usr/local/cuda/lib64/libcudnn*
cat /usr/local/cuda/include/cudnn_version.h | grep CUDNN_MAJOR -A 2
```

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/9b7813ab-e064-4694-a7bc-8c5c2ee764fa)


cuDNN 8.6.0 버전임

아래 이미지처럼 정확히 나와야 함

```bash
ldconfig -N -v $(sed 's/:/ /' <<< $LD_LIBRARY_PATH) 2>/dev/null | grep libcudnn
```

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/0e87e117-fc3c-40f2-92ba-1863a4207f83)


### Tensroflow 설치

만약 pip 설치 모듈이 없을 경우

```bash
sudo apt install python3-pip
```

이후 tensorflow 설치

```bash
pip3 install tensorflow
```

python  실행

```bash
python3
```

```python
import tensorflow as tf
tf.__version__
tf.config.list_physical_devices('GPU')
```

imrport tensorflow

![image](https://github.com/DongminKim21800064/IAIA_Project2_RobotSonny/assets/91419683/0fd3682a-c30d-44e8-a282-8f1f61aa8219)

### pytorch+cu118 설치

[PyTorch](https://pytorch.org/get-started/locally/)

나는 이거로 설치함 (이걸 추천)

```bash
pip install torch==2.0.0+cu118 torchvision==0.15.1+cu118 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cu118
```

or

```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### pytorch version 검사

python  실행

```python
python3
```

```python
import torch
torch.__version__
```

참고 문헌

https://teddylee777.github.io/linux/ubuntu2004-cuda-update/

https://davi06000.tistory.com/21

https://webnautes.tistory.com/1428

[https://jeo96.tistory.com/entry/Ubuntu-2004-CUDA-재설치](https://jeo96.tistory.com/entry/Ubuntu-2004-CUDA-%EC%9E%AC%EC%84%A4%EC%B9%98)

https://pytorch.org/get-started/locally/
