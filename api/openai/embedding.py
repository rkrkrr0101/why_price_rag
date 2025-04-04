import openai
from const.const_env import OPENAI_KEY
from util.memoryUtil import memory_monitor

# OpenAI API 키 설정
openai.api_key = OPENAI_KEY

def get_embedding(text):
    """
    OpenAI API를 사용하여 텍스트의 임베딩 벡터를 얻습니다.
    """
    memory_monitor("임베딩 요청 전")
    try:
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        embedding = response['data'][0]['embedding']
        memory_monitor("임베딩 요청 후")
        return embedding
    except Exception as e:
        print(f"임베딩 생성 오류: {e}")
        return None 