## 1. 프로젝트 구조

```
chat_with_danaka/
├── checkpoints_v2       # pre-trained model
├── gui/                 # GUI 관련 모듈
│   ├── __init__.py      
│   ├── openai_gui.py    # chatbot과 대화
│   ├── tts_gui.py       # GUI 클래스
├── modules/             # 기능별 모듈
│   ├── __init__.py      
│   ├── custom_openvoice.py    # TTS 처리 모듈
│   ├── audio_player.py  # 음성 재생 모듈
├── openvoice/           # openvoice 함수를 사용할 수 있는 모듈들
├── output/              # 생성된 TTS 음성 파일 저장 폴더
├── resources/           # 리소스 파일들 (예: 샘플 음성 파일)
├── main.py              # 프로그램의 진입점
└── requirements.txt     # 의존성 패키지 리스트
```

## 2. 환경 설정

우분투 22.04에서 개발되었습니다.

### 2.1 OpenVoice 관련 환경 설정

- 프로젝트 클론 및 의존성 패키지 설치

```bash
git clone https://github.com/SHIN-DONG-UK/chat_with_danaka.git
cd chat_with_danaka
pip install -r requirements.txt
```

- pre-trained model 다운로드

<a href="https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip">여기 누르쇼</a>

위 프로젝트 구조처럼 project 안에 압축을 풀어주면 됩니다.

### 2.2 Python 설치

우분투 22.04의 기본 Python 버전은 3.10입니다.

Python 3.9가 설치되어 있는지 확인하고, 없으면 설치해야 합니다.

### Python 3.9 설치:

```bash
sudo apt update
sudo apt install python3.9 python3.9-venv
```

- python3.9로 가상환경 만들기 위해서 python3.9-venv를 깔아야 함

### 설치 확인:

```bash
python3.9 --version
```

### 2.3 가상환경

- 가상환경 만들기

```bash
python3.9 -m venv [가상환경 이름]
```

- 가상환경 실행

```bash
source venv/bin/activate
```

### 2.4 CUDA 관련 설정

이거는 그냥 ubuntu 설치할 때 third-party 설정해서 깔았습니다.

만약 이렇게 깔지 않았으면 알아서 CUDA 관련 깔아야 합니다.

CUDA는 하드웨어 환경에 맞는 드라이브 버전 설치해야 함

그건 검색해서 알아서 하쇼

- CUDA 동작 확인

```bash
import torch
print(torch.cuda.is_available())
```

`True`라고 뜨면 됩니다



### 2.5 Melo TTS 설치

```bash
git clone https://github.com/myshell-ai/MeloTTS.git
cd MeloTTS
pip install -e .
python -m unidic download
```

### 2.6 tkinter 설치

```bash
sudo apt update
sudo apt install python3.9-tk
```

### 2.7 openai 설치

```bash
pip install openai==0.27.8
```

## 3. 각 모듈 설명

### 3.1 TTS 처리 모듈(custom_openvoice.py)

- `__init__()` : 생성자
    - model 경로 지정
    - wav 파일로 저장될 경로 지정
    - 언어 지정
    - cuda device 지정
- `set_model()` : TTS, tone converter 관련 선언
    - tone converter 지정
    - TTS 구현체 선언(melo TTS 사용)
    - pre-trained model 지정
- `get_reference_speaker()` : 목소리 톤을 따라할 음성 임베딩 로드
- `make_speech()`  : 실제 text를 음성으로 바꾸는 함수
    - `tts_to_file()` : text와 speaker_id(국가 코드 느낌? 아직 모름)입력하면 톤 입히는 작업 준비하는 단계로 넘어가는 듯
    - `tone_color_converter.convert()` : 얘가 톤을 바꿔줌

### 3.2 음성 재생 모듈(audio_player.py)

- 이건 그냥 pygame이라는 라이브러리 전형적인 사용법이라서 gpt 딸깍하면 됩니다

### 3.3 GUI 모듈(tts_gui.py)

![image](https://github.com/user-attachments/assets/1be874fc-30bb-483e-ba57-eef8684f9a5f)

- 다양한 reference 음성을 적용해 테스트 해볼 수 있는 프로그램입니다.

### 3.4 GUI 모듈2(openai_gui.py)

![image (1)](https://github.com/user-attachments/assets/5050ffa8-e3cf-49ff-a894-7a98be580a38)

- openai api로 gpt와 대화하는 프로그램입니다.
- Send하면 음성과 함께 텍스트가 출력됩니다

## 4. 프로그램 실행 방법
### 4.0 openai api key
![Screenshot from 2025-01-25 19-36-40](https://github.com/user-attachments/assets/4ca1fa53-65ca-42f2-b5b2-5b63c58c31ec)
- ./gui/openai_gui.py > 본인 key 넣으쇼

### 4.1 기본 실행

```bash
python main.py
```

### 4.2 gui 바꿔서 실행 방법

![image (3)](https://github.com/user-attachments/assets/a7c093b5-3551-481f-ba4b-a594c6fbaa53)

- 주석 바꾸면 됩니다.
