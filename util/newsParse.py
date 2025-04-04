from newspaper import Article
from util.memoryUtil import memory_monitor

def get_parsed_article(url):
    memory_monitor("기사 파싱 전")
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        # 기사 텍스트가 비어있는 경우 처리
        article_text = article.text.strip()
        if not article_text:
            print(f"주의: 기사 텍스트가 비어 있습니다. 원본 URL: {url}")
            article_text = "기사 내용을 추출할 수 없습니다."
        
        # 필요한 정보만 추출하여 딕셔너리로 반환
        result = {
            "title": article.title,
            "text": article_text
        }
        
        memory_monitor("기사 파싱 후")
        return result
    
    except Exception as e:
        print(f"기사 파싱 오류: {e}")
        return {
            "title": "파싱 실패",
            "text": "기사를 파싱하는 도중 오류가 발생했습니다."
        }