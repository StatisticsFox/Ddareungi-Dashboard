# Core Pkgs
import requests
import json
import time
from kafka import KafkaProducer
from datetime import datetime

# environment setting
# Kafka 설정 하기
topicName = "bike-station-info"
producer = KafkaProducer(bootstrap_servers=['kafka_node1:9092', 'kafka_node2:9092', 'kafka_node3:9092'],
value_serializer=lambda x: json.dumps(x).encode("utf-8"))

# api 불러오는 함수

  

# API 키 읽기
with open("api_key.bin", "r", encoding="UTF-8") as api_key_file:
	api_key = api_key_file.read().strip()

  

# 무한 루프를 돌면서 실시간으로 데이터를 가져와 Kafka에 전송
while True:
	try:
	# 따릉이 API 호출
		bike_stations = [] # 초기화
		for start_index in range(1, 2001, 1000): # 1부터 2000까지, 1000개 단위로 요청
			end_index = start_index + 999
			response = request_seoul_api(api_key, start_index, end_index)
			if response.status_code == 200:
				bike_stations.extend(response.json()["rentBikeStatus"]["row"])
	
		for station in bike_stations:
			# 필요한 정보 추출
			data = {
				"rackTotCnt": station["rackTotCnt"],
				"stationName": station["stationName"],
				"parkingBikeTotCnt": station["parkingBikeTotCnt"],
				"shared": station["shared"],
				"stationLatitude": station["stationLatitude"],
				"stationLongitude": station["stationLongitude"],
				"stationId": station["stationId"],
				"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			}

			# Kafka에 데이터 전송
			producer.send(topicName, value=data)
			producer.flush() # 메시지 전송 완료
			print(f"Sent data to Kafka: {data}")
	

		# 대기시간
		time.sleep(60)
	
	except Exception as e:
		print(f"Error: {e}")
