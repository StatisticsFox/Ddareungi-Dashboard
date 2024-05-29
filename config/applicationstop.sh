#!/bin/bash

# 실행 중인 producer.py 프로세스를 찾아 종료
PIDS=$(pgrep -f producer.py)
if [ -z "$PIDS" ]; then
    echo "No producer.py process found."
else
    for PID in $PIDS; do
        kill $PID
        echo "Producer with PID $PID stopped."
    done
fi