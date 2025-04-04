from util.memoryUtil import memory_monitor
from api.naver.news_search import search_naver_news
from db.vector_db import store_news_vectors

def process_single_stock(stock_index, total_stocks, stock, collection, news_limit=5):
    """단일 주식에 대한 모든 처리를 수행합니다."""
    print(f"\n[{stock_index+1}/{total_stocks}] '{stock['name']}' 관련 뉴스 검색 중...")
    memory_monitor(f"주식 처리 시작: {stock['name']}")
    
    try:
        # 뉴스 검색
        news_list = search_naver_news(stock['name'], limit=news_limit)  # 각 주식당 1개 뉴스만 처리
        memory_monitor("뉴스 검색 완료")
        
        if not news_list:
            print(f"{stock['name']}에 대한 뉴스를 찾지 못했습니다.")
            return 0
        
        print(f"{len(news_list)}개 뉴스 발견, 처리 중...")
        
        processed_count = 0
        for news_index, news in enumerate(news_list):
            print(f"  - 뉴스 [{news_index+1}/{len(news_list)}] 처리 중: {news['title']}")
            
            # 뉴스 URL에 문제가 없는지 확인
            if not news['link'] or len(news['link']) < 10:
                print(f"    - 유효하지 않은 URL: {news['link']}")
                continue
                
            # 뉴스 벡터 저장 시도
            try:
                result = store_news_vectors(collection, news, stock['name'])
                if result:
                    processed_count += 1
                    print(f"    - 뉴스 처리 성공: {news['title']}")
            except Exception as e:
                print(f"    - 뉴스 처리 중 오류 발생: {e}")
            
            memory_monitor(f"뉴스 {news_index+1} 처리 후")
        
        memory_monitor(f"주식 처리 완료: {stock['name']}")
        return processed_count
    
    except Exception as e:
        print(f"주식 처리 오류 ({stock['name']}): {e}")
        return 0
    finally:
        memory_monitor(f"주식 처리 종료: {stock['name']}") 