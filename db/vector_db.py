import datetime
import chromadb
from util.memoryUtil import memory_monitor
from util.text_processing import split_text_chunks
from api.openai.embedding import get_embedding
from util.newsParse import get_parsed_article
from db.mysql_handler import is_url_processed, mark_url_processed
from const.const_env import CHROMA_URL, CHROMA_PORT

def init_chroma_db():
    """ChromaDB 클라이언트를 초기화하고 콜렉션을 설정합니다."""
    # ChromaDB 클라이언트 초기화
    client = chromadb.HttpClient(host=CHROMA_URL, port=CHROMA_PORT)
    
    
    # 콜렉션 생성 또는 가져오기
    collection = client.get_or_create_collection(name="stock_news_vectors")
    
    return client, collection

def store_news_vectors(collection, news_data, stock_name,max_text_length=5000):
    """뉴스 데이터를 벡터화하여 ChromaDB에 저장합니다."""
    memory_monitor("함수 시작")
    
    # 이미 처리된 URL인지 확인
    if is_url_processed(stock_name, news_data["link"]):
        print(f"이미 처리된 URL: {news_data['link']}")
        return False
    
    # 기존 DB에 URL이 있는지 확인
    try:
        memory_monitor("DB 확인 전")
        existing_ids = [f"{news_data['link'].replace('/', '_').replace(':', '_')}_0"]
        existing_data = collection.get(ids=existing_ids, include=[])
        memory_monitor("DB 확인 후")
        
        if existing_data and len(existing_data["ids"]) > 0:
            print(f"이미 저장된 URL: {news_data['link']}")
            mark_url_processed(stock_name, news_data["link"])
            return False
    except Exception as e:
        print(f"URL 확인 오류: {e}")
        # 오류가 발생하더라도 계속 진행
    
    try:
        # 뉴스 기사 파싱
        memory_monitor("기사 파싱 시작")
        article_data = get_parsed_article(news_data["link"])
        publication_date = news_data["date"]
        memory_monitor("기사 파싱 완료")
        
        # 파싱한 기사에서 필요한 정보 추출
        article_title = article_data.get("title") or news_data["title"]
        article_text = article_data.get("text", "")
        
        print(f"기사 텍스트 길이: {len(article_text)} 문자")
        
        # 텍스트가 없으면 처리 중단
        if not article_text:
            print("기사 텍스트가 비어 있어 처리를 중단합니다.")
            return False
        
        # 메모리 절약을 위해 원본 텍스트 크기 제한 (너무 길면 앞부분만 사용)
        if len(article_text) > max_text_length:  # 5KB 제한
            print(f"주의: 텍스트가 너무 깁니다. 처음 5,000자만 사용합니다. (전체: {len(article_text)}자)")
            article_text = article_text[:5000]
        
        # 현재 시간 (벡터 저장 시간)
        now = datetime.datetime.now().isoformat()
        
        # 청크 분할 직접 처리 - 제너레이터 사용
        memory_monitor("청크 처리 시작")
        
        chunks_gen = split_text_chunks(article_text)
        
        # 텍스트수 /1000 만큼의 청크만 처리
        max_chunks = max_text_length//1000
        processed_chunks = 0
        
        for i, chunk in enumerate(chunks_gen):
            if i >= max_chunks:
                break  # 최대 청크 수 초과시 반복문 종료
                
            memory_monitor(f"청크 {i+1} 처리 전")
            processed_chunks += 1
            
            # 청크 앞에 발행일 추가
            chunk_with_date = f"발행일: {publication_date}\n\n{chunk}"
            
            # 임베딩 생성
            memory_monitor(f"임베딩 생성 전 (청크 {i+1})")
            embedding = get_embedding(chunk_with_date)
            memory_monitor(f"임베딩 생성 후 (청크 {i+1})")
            
            if embedding:
                # ChromaDB에 저장
                memory_monitor(f"ChromaDB 저장 전 (청크 {i+1})")
                collection.add(
                    embeddings=[embedding],
                    documents=[chunk_with_date],
                    metadatas=[{
                        "chunk": i,
                        "total_chunks": max_chunks,
                        "publication_date": publication_date,
                        "added_date": now,
                        "title": article_title,
                        "stock_name": stock_name,
                        "news_url": news_data["link"]
                    }],
                    ids=[f"{news_data['link'].replace('/', '_').replace(':', '_')}_{i}"]
                )
                memory_monitor(f"ChromaDB 저장 후 (청크 {i+1})")
            else:
                print(f"임베딩 생성 실패: 청크 {i}")
        
        print(f"총 {processed_chunks}개 청크 처리 완료")
        memory_monitor("모든 청크 처리 완료")
        
        # 처리 완료 표시
        mark_url_processed(stock_name, news_data["link"])
        
        print(f"저장 완료: {news_data['title']} ({processed_chunks} 청크)")
        memory_monitor("함수 종료")
        return True
    
    except Exception as e:
        print(f"뉴스 벡터 저장 오류: {e}")
        return False
    finally:
        memory_monitor("최종 처리 완료") 