import requests
import json
from const.const_env import KOREA_INV_KEY, KOREA_INV_SECRET


def get_korea_investment_token():
    """한국투자증권 API 접근 토큰을 얻습니다."""
    url = "https://openapi.koreainvestment.com:9443/oauth2/tokenP"
    headers = {
        "content-type": "application/json"
    }
    body = {
        "grant_type": "client_credentials",
        "appkey": KOREA_INV_KEY,
        "appsecret": KOREA_INV_SECRET
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(body))
    return response.json()["access_token"]