# Python 3.9 버전을 기반으로 이미지를 생성합니다.
FROM python:3.9-slim

# 작업 디렉토리를 설정합니다.
WORKDIR /usr/src/app

# 필요한 라이브러리를 설치합니다.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드를 컨테이너에 복사합니다.
COPY . .

# 컨테이너가 시작될 때 실행할 기본 명령어를 설정합니다. (초기에는 비워둡니다)
# CMD [ "python", "./main.py" ]