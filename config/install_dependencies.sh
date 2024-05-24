#!/bin/bash

# 경로 설정
PROJECT_DIR=./
VENV_DIR=$PROJECT_DIR/venv

# 가상 환경 디렉토리가 존재하지 않으면 생성
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

# 가상 환경 활성화
source $VENV_DIR/bin/activate

# 필요 패키지 설치
pip install -r $PROJECT_DIR/requirements.txt

echo "Dependencies installed."
