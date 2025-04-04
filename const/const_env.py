import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 한국투자증권 API 인증 정보
KOREA_INV_KEY = os.getenv("KOREA_INV_KEY")
KOREA_INV_SECRET = os.getenv("KOREA_INV_SECRET")

# 네이버 API 인증 정보
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

# OpenAI API 인증 정보
OPENAI_KEY = os.getenv("OPENAPI_KEY")

# MySQL 연결 정보
MYSQL_ID = os.getenv("MYSQL_ID")
MYSQL_KEY = os.getenv("MYSQL_KEY")
MYSQL_URL = os.getenv("MYSQL_URL")

# ChromaDB 연결 정보
CHROMA_URL = os.getenv("CHROMA_URL")
CHROMA_PORT = os.getenv("CHROMA_PORT")

