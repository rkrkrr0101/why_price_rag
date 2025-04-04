from util.memoryUtil import memory_monitor
from api.kor_inv.getApiToken import get_korea_investment_token
from api.kor_inv.getHotStocks import get_hotStocks
from db.mysql_handler import update_hot_stocks, init_progress_table
from db.vector_db import init_chroma_db
from processor.stock_processor import process_single_stock
import const.const_env
# 메인함수
def main():
    """메인 실행 함수"""
    print("급등주 뉴스 RAG 시스템 시작...")
    memory_monitor("시작")
    
    # 1. 한국투자증권 API로 급등주 검색
    print("한국투자증권 API 토큰 요청 중...")
    token = get_korea_investment_token()
    
    print("거래량 상위 주식 검색 중...")
    hot_stocks = get_hotStocks(token, limit=10)  # 상위 10개 처리
    
    if not hot_stocks:
        print("급등주 목록을 가져오지 못했습니다.")
        return
    
    print(f"{len(hot_stocks)}개의 급등주를 찾았습니다.")
    memory_monitor("급등주 검색 완료")
    
    # 2. MySQL에 급등주 목록 저장
    update_hot_stocks(hot_stocks)
    
    # 진행 상태 테이블 초기화
    init_progress_table()
    memory_monitor("DB 초기화 완료")
    
    # 3. ChromaDB 초기화
    try:
        print("ChromaDB 초기화 중...")
        client, collection = init_chroma_db()
        memory_monitor("ChromaDB 초기화 완료")
    except Exception as e:
        print(f"ChromaDB 초기화 오류: {e}")
        print("ChromaDB가 설치되어 있지 않은 것 같습니다. 먼저 설치해주세요: pip install chromadb")
        return
    
    # 4. 각 급등주에 대한 뉴스 검색 및 벡터 저장 (하나씩 순차적으로 처리)
    total_processed = 0
    total_stocks = len(hot_stocks)
    
    for stock_index, stock in enumerate(hot_stocks):
        processed = process_single_stock(stock_index, total_stocks, stock, collection)
        total_processed += processed
        memory_monitor(f"주식 {stock_index+1} 완료")
    
    print(f"\n작업 완료: 총 {total_processed}개 뉴스 기사를 처리했습니다.")
    memory_monitor("종료")

if __name__ == "__main__":
    main() 
    