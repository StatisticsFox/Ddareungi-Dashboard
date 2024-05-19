import os
from testcode import request_seoul_api

# API 키 설정을 위한 환경 변수 설정
test_api_key=os.environ['API_KEY']

# 테스트를 위해 호출할 인덱스 설정
test_start_index = 1
test_end_index = 10  # 테스트를 위해 작은 범위로 설정
try:
    # 따릉이 API 호출 및 테스트
    response = request_seoul_api(test_api_key, test_start_index, test_end_index)
    if response.status_code == 200:
        # API 호출이 성공했을 때 반환된 데이터 출력
        print(response.json())
    else:
        print("Failed to fetch data from the API.")
except Exception as e:
    print(f"Error occurred during API call: {e}")