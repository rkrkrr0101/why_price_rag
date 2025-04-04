from const.const_env import KOREA_INV_KEY, KOREA_INV_SECRET
import requests

# 거래량 상위 주식 조회
def get_hotStocks(token, limit=50):
    """거래량 상위 주식 목록을 가져옵니다."""
    url = "https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/quotations/volume-rank"
    headers = {
        "Content-Type": "application/json", 
        "authorization": f"Bearer {token}",
        "appkey": KOREA_INV_KEY,
        "appsecret": KOREA_INV_SECRET,
        "tr_id": "FHPST01710000"
    }
    params = {
        "FID_COND_MRKT_DIV_CODE": "J",  # 시장구분코드(J:전체, 9:코스피, 8:코스닥)
        "FID_COND_SCR_DIV_CODE": "20171",  # 화면번호
        "FID_INPUT_ISCD": "",  # 조회종목코드
        "FID_DIV_CLS_CODE": "0",  # 분류구분코드(0:전체)
        "FID_BLNG_CLS_CODE": "0",  # 소속구분코드(0:전체)
        "FID_TRGT_CLS_CODE": "111",  # 대상구분코드(111:전체)
        "FID_TRGT_EXLS_CLS_CODE": "000",  # 대상제외구분코드(000:전체조회)
        "FID_INPUT_PRICE_1": "0",  # 입력가격1
        "FID_INPUT_PRICE_2": "0",  # 입력가격2
        "FID_VOL_CNT": "0",  # 거래량
        "FID_INPUT_DATE_1": "0"  # 입력일자
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"API 요청 실패: {response.status_code}, {response.text}")
        return []
    
    stock_list = []
    try:
        output = response.json()["output"]
        for item in output[:limit]:
            # 종목명과 코드만 추출
            stock_list.append({
                "name": item["hts_kor_isnm"],  # 종목명
                "code": item["mksc_shrn_iscd"]  # 종목코드
            })
    except Exception as e:
        print(f"데이터 파싱 오류: {e}")
    
    return stock_list