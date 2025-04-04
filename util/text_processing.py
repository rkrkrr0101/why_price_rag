def split_text_chunks(text, max_length=1000, overlap=100):
    """
    메모리 효율성을 위해 제너레이터를 사용하여 텍스트 청크를 하나씩 생성합니다.
    
    Args:
        text: 분할할 텍스트
        max_length: 각 청크의 최대 길이
        overlap: 이웃한 청크 간 중복 문자 수
        
    Yields:
        각 텍스트 청크를 하나씩 생성
    """
    # 텍스트가 없거나, 길이가 너무 짧은 경우 바로 반환
    if not text or len(text) <= 0:
        return
        
    if len(text) <= max_length:
        yield text
        return
    
    # 현재 위치
    start = 0
    last_end = 0  # 마지막으로 처리한 끝 위치 (무한 루프 방지용)
    
    # 긴 텍스트를 순차적으로 처리
    while start < len(text):
        # 현재 청크의 끝 위치 계산
        end = min(start + max_length, len(text))
        
        # 단어 경계에서 분할
        if end < len(text):
            # 공백 찾기
            space_index = text.rfind(' ', start + max_length - overlap, end)
            if space_index > start:
                end = space_index + 1
        
        # 청크 생성
        chunk = text[start:end].strip()
        if chunk:  # 빈 청크는 건너뜀
            yield chunk
        
        # 무한 루프 방지: 진행이 없는 경우
        if end <= last_end:
            # 강제로 최소 1자 이상 진행
            start = last_end + 1
            if start >= len(text):
                break
        else:
            # 정상적인 진행
            last_end = end
            start = end - overlap
            if start < 0:
                start = 0 