# 급등주 뉴스 RAG 시스템

이 프로젝트는 한국투자증권 API를 통해 거래량 상위 주식(급등주)을 찾고, 해당 주식에 관한 최신 뉴스를 네이버 뉴스 API로 가져온 후, OpenAI 임베딩 모델을 사용하여 벡터화하는 RAG(Retrieval-Augmented Generation) 시스템입니다.

## 기능

1. 한국투자증권 API를 통해 거래량 상위 주식 정보를 가져옵니다.
2. 가져온 급등주 목록을 MySQL 데이터베이스에 저장합니다.
3. 각 급등주에 대해 네이버 뉴스 API를 사용하여 최신 뉴스를 검색합니다.
4. 뉴스 기사를 newspaper3k를 사용하여 파싱하고, 내용을 일정 길이로 분할합니다.
5. 분할된 텍스트 청크를 OpenAI 임베딩 모델을 사용하여 벡터화합니다.
6. 벡터화된 데이터를 ChromaDB에 저장하여 검색 가능한 벡터 데이터베이스를 구축합니다.

## 설치 방법

### 필수 패키지 설치

```bash
pip install python-dotenv newspaper3k lxml_html_clean mysql-connector-python chromadb openai requests pandas
```

### 환경 설정

1. `.env` 파일에 다음과 같은 API 키와 데이터베이스 접속 정보를 설정합니다:

```
OPENAPI_KEY=your_openai_api_key
KOREA_INV_KEY=your_korea_investment_api_key
KOREA_INV_SECRET=your_korea_investment_api_secret
NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_client_secret
MYSQL_ID=your_mysql_username
MYSQL_KEY=your_mysql_password
MYSQL_URL=jdbc:mysql://localhost:3306/your_database_name?serverTimezone=Asia/Seoul
```

2. MySQL 데이터베이스 `why_price`를 생성합니다.

## 사용 방법

```bash
python main.py
```

## 프로세스 설명

1. 한국투자증권 API에서 토큰을 얻습니다.
2. 거래량 상위 주식 목록을 가져와 MySQL에 저장합니다.
3. ChromaDB를 초기화합니다.
4. 각 급등주마다 네이버 뉴스 API로 최신 뉴스를 검색합니다.
5. 각 뉴스 기사에 대해:
   - 뉴스 URL이 이미 ChromaDB에 저장되어 있는지 확인합니다.
   - newspaper3k로 뉴스 본문을 파싱합니다.
   - 본문을 1000자 단위로 오버랩 100자를 적용하여 분할합니다.
   - 각 청크에 뉴스 발행일을 추가합니다.
   - OpenAI 임베딩 모델로 벡터화하여 ChromaDB에 저장합니다.

## 벡터 데이터 구조

ChromaDB에 저장되는 각 벡터 데이터는 다음 정보를 포함합니다:

- 임베딩: 텍스트 청크의 벡터 표현
- 본문 청크: 뉴스 본문의 일부분
- 기사 작성일: 뉴스가 발행된 날짜
- DB 레코드 추가 날짜: 벡터가 DB에 저장된 시간
- 제목: 뉴스 기사의 제목
- 주식명: 관련된 주식의 이름
- 뉴스 원본 링크: 원본 뉴스 기사의 URL 