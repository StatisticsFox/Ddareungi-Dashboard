import json
import requests
from confluent_kafka import Producer
import time
from datetime import datetime
import os

# Kafka 서버 및 토픽 설정
# Kafka 브로커:포트
servers = ['kafka_node1:9092', 'kafka_node2:9092', 'kafka_node3:9092'] 
topicName = 'bike-station-info' # 사용할 Kafka 토픽 이름

# Kafka Producer 설정
conf = {'bootstrap.servers': ','.join(servers)}
producer = Producer(**conf)

# 환경 변수에서 API 키 불러오기
with open("/home/ubuntu/api_key.bin", "r", encoding="UTF-8") as api_key_file:
    seoul_api_key = api_key_file.read().strip()

def request_seoul_api(seoul_api_key, start_index, end_index):
    """
    주어진 시작 및 종료 인덱스 범위에서 서울시 자전거 대여소 데이터를 가져옵니다.
    
    Args:
        start_index (int): 시작 인덱스.
        end_index (int): 종료 인덱스.
    
    Returns:
        response: requests의 응답 객체.
    """
    api_server = f'http://openapi.seoul.go.kr:8088/{seoul_api_key}/json/bikeList/{start_index}/{end_index}'
    response = requests.get(api_server)
    return response

def delivery_report(err, msg):
    """
    메시지 전송 후 호출되는 콜백 함수. 메시지 전송 성공 여부를 출력합니다.
    
    Args:
        err (KafkaError): 메시지 전송 오류가 있는 경우.
        msg (Message): 전송된 메시지.
    """
    
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def send_data():
    """
    서울시 자전거 대여소 데이터를 페이지별로 가져와서 Kafka 토픽에 전송합니다.
    """
    # 무한 루프를 돌면서 실시간으로 데이터를 가져와 kafka에 전송
    while True:
        try:
            # 따릉이 API 호출
            bike_stations=[] # 따릉이 대여소 정보를 저장할 리스트
            for start_index in range(1, 2001, 1000): # 1부터 2000까지 1000개씩 가져옴
                end_index = start_index + 999
                response = request_seoul_api(seoul_api_key, start_index, end_index)
                if response.status_code == 200: 
                    bike_stations.extend(response.json()['rentBikeStatus']['row']) # API 호출 결과를 리스트에 추가

            for station in bike_stations:
                # 필요한 데이터 추출
                data = {
                    "rackTotCnt" : station['rackTotCnt'],
                    "stationName" : station['stationName'],
                    "parkingBikeTotCnt" : station['parkingBikeTotCnt'],
                    "shared" : station['shared'],
                    "stationLatitude" : station['stationLatitude'],
                    "stationLongitude": station['stationLongitude'],
                    "stationId" : station['stationId'],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                station_id = station['stationId']

                #json_data = json.dumps(message, ensure_ascii=False)
                # Kafka에 메시지 전송
                producer.produce(topic=topicName, 
                                key=str(station_id), 
                                value=json.dumps(data, ensure_ascii=False), 
                                callback=delivery_report) 
                producer.poll(1) # 메시지 전송을 위해 poll() 메서드 호출

                # 전송한 데이터를 출력
                print(f"Sent data to Kafka: {data}")
            
            # producer.flush() # Kafka Producer 종료
            # 30초 대기
            time.sleep(30) # 30초마다 실행

        except Exception as e:
            print(f"Error: {e}")

def main():
    """
    메인 함수로, 자전거 대여소 데이터를 Kafka로 전송하는 작업을 시작합니다.
    """
    send_data()

if __name__ == "__main__":
    main()
