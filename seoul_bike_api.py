import requests

def request_seoul_api(api_key, start_index, end_index):
	"""서울 열린 데이터 광장 API를 호출하여 따릉이 정보를 가져온다."""
	g_api_host = "http://openapi.seoul.go.kr:8088"
	g_type = "json"
	g_service = "bikeList"
	url = f"{g_api_host}/{api_key}/{g_type}/{g_service}/{start_index}/{end_index}/"
	return requests.get(url)