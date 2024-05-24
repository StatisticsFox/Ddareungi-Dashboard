import subprocess

def run_producer():
    """producer.py를 백그라운드에서 실행하고 로그를 파일로 저장합니다."""
    """  스크립트 실행 중 발생하는 모든 표준 출력과 표준 오류 메시지가 /src/kafka-producer/producer.log 파일에 기록 """
    command = "nohup python /src/kafka-producer/producer.py > /src/kafka-producer/producer.log 2>&1 &"
    subprocess.run(command, shell=True, check=True)

if __name__ == '__main__':
    run_producer()

