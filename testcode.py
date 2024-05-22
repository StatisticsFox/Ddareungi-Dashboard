# 따릉이 API URL
import requests

def request_seoul_api(api_key, start_index, end_index):
    # API 요청 URL
    url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/bikeList/{start_index}/{end_index}/"
    try:
        print(f"Requesting URL: {url}")  # URL 로그 출력
        response = requests.get(url)
        print(f"Response: {response.status_code}")  # 응답 코드 로그 출력
        return response
    except Exception as e:
        print(f"Error occurred in request_seoul_api: {e}")
        return None

