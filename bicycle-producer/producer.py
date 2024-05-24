# Core Pkgs
import requests
import json
import time
from kafka import KafkaProducer
from datetime import datetime

# environment setting
# Kafka 설정
topicName = "bike-station-info"
producer = KafkaProducer(bootstrap_servers=['kafka_node1:9092', 'kafka_node2:9092', 'kafka_node3:9092'],
value_serializer=lambda x: json.dumps(x).encode("utf-8"))

# 따릉이 API URL
def request_seoul_api(api_key, start_index, end_index):
	"""서울 열린 데이터 광장 API를 호출하여 따릉이 정보를 가져온다."""
	g_api_host = "http://openapi.seoul.go.kr:8088"
	g_type = "json"
	g_service = "bikeList"
	url = f"{g_api_host}/{api_key}/{g_type}/{g_service}/{start_index}/{end_index}/"
	return requests.get(url)


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
			print(f"Sent data to Kafka: {data}")
	

		# 대기시간
		time.sleep(60)
	
	except Exception as e:
		print(f"Error: {e}")
