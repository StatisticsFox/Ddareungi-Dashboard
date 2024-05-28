import json
import requests
from kafka import KafkaProducer
from confluent_kafka import Producer
import time
import os

# Kafka 서버 및 토픽 설정
# Kafka 브로커:포트
servers = ['kafka_node1:9092', 'kafka_node2:9092', 'kafka_node3:9092']
topic_name = 'bike-station-info' # 사용할 Kafka 토픽 이름

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
        start_idx (int): 시작 인덱스.
        end_idx (int): 종료 인덱스.
    
    Returns:
        dict: JSON 형식의 자전거 대여소 데이터.
    """
    api_server = f'http://openapi.seoul.go.kr:8088/{seoul_api_key}/json/bikeList/{start_index}/{end_index}' # .format(seoul_api_key, start_idx, end_idx)
    response = requests.get(api_server)
    data = json.loads(response.content)
    return data
    
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
    start_index = 1
    end_index = 1000
    message_count = 0
    while True:
        data = request_seoul_api(seoul_api_key, start_index, end_index)
        if not data['rentBikeStatus']['row']:
            break
            
        for station in data['rentBikeStatus']['row']:
            # 필요한 데이터 추출
            rack_tot_cnt = station['rackTotCnt']
            station_name = station['stationName']
            parking_bike_tot_cnt = station['parkingBikeTotCnt']
            shared = station['shared']
            station_latitude = station['stationLatitude']
            station_longitude = station['stationLongitude']
            station_id = station['stationId']

            # 데이터를 JSON 형식으로 변환
            message = {
                'rack_tot_cnt': rack_tot_cnt,
                'station_name': station_name,
                'parking_bike_tot_cnt': parking_bike_tot_cnt,
                'shared': shared,
                'station_latitude': station_latitude,
                'station_longitude': station_longitude,
                'station_id': station_id
            }
            json_data = json.dumps(message, ensure_ascii=False)

            # Kafka에 메시지 전송
            producer.produce(topic=topic_name,
                             key=str(station_id),
                             value=json_data.encode('utf-8'),
                             callback=delivery_report)
            producer.poll(0) # 이벤트 처리

            message_count += 1
            if message_count % 1000 == 0:
                print(f"{message_count} messages have been sent to Kafka.")

            # 전송한 데이터를 출력 (필요에 따라 주석 처리 가능)
            # print(f"Sent data to Kafka: {message}")

        start_index += 1000
        end_index += 1000
        time.sleep(30) # 30초마다 실행

    producer.flush() # 모든 메시지 전송 완료

def main():
    """
    메인 함수로, 자전거 대여소 데이터를 Kafka로 전송하는 작업을 시작합니다.
    """
    send_data()

if __name__ == "__main__":
    main()
