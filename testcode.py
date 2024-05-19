import os
import requests
import json
import time
from datetime import datetime


# 따릉이 API URL
def request_seoul_api(api_key, start_index, end_index):
    g_api_host = "http://openapi.seoul.go.kr:8088"
    g_type = "json"
    g_service = "bikeList"
    url = f"{g_api_host}/{api_key}/{g_type}/{g_service}/{start_index}/{end_index}/"
    return requests.get(url)
