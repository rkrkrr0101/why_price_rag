import requests
from const.const_env import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET

def search_naver_news(stock_name, limit=5):
    """네이버 API를 사용하여 주식 관련 최신 뉴스를 검색합니다."""
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {
        "query": stock_name,
        "display": limit,
        "sort": "date"  # 최신순으로 정렬
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"네이버 뉴스 API 요청 실패: {response.status_code}, {response.text}")
        return []
    
    news_list = []
    try:
        items = response.json()["items"]
        for item in items:
            # HTML 태그 제거
            title = item["title"].replace("<b>", "").replace("</b>", "")
            title = title.replace("&quot;", "\"").replace("&amp;", "&")
            
            # 네이버 뉴스 결과에서 원본 링크 추출
            original_link = item["originallink"] if item["originallink"] else item["link"]
            
            # 요약 텍스트에서 HTML 태그 제거
            description = item.get("description", "")
            description = description.replace("<b>", "").replace("</b>", "")
            description = description.replace("&quot;", "\"").replace("&amp;", "&")
            
            news_list.append({
                "title": title,
                "link": original_link,
                "date": item["pubDate"],
                "description": description
            })
    except Exception as e:
        print(f"네이버 뉴스 파싱 오류: {e}")
    
    return news_list 