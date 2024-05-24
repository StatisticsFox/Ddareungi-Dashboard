import subprocess

def run_producer():
    """ subprocess.run 함수의 check=True 옵션은 명령어 실행이 실패할 경우 CalledProcessError 예외를 발생시키므로 스크립트가 예외 처리"""
    command = "python /src/kafka-producer/producer.py"
    subprocess.run(command, shell=True, check=True)

if __name__ == '__main__':
    run_producer()

