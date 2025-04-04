import unittest
from util.text_processing import split_text_chunks

class TestTextProcessing(unittest.TestCase):
    """텍스트 처리 유틸리티 함수에 대한 테스트 클래스"""
    
    def test_split_text_chunks_empty_text(self):
        """빈 텍스트에 대한 테스트"""
        chunks = list(split_text_chunks(""))
        self.assertEqual(len(chunks), 0, "빈 텍스트는 청크가 생성되지 않아야 합니다.")
    
    def test_split_text_chunks_short_text(self):
        """짧은 텍스트에 대한 테스트 (최대 길이보다 짧은 경우)"""
        text = "이것은 짧은 텍스트입니다."
        max_length = 100
        chunks = list(split_text_chunks(text, max_length))
        
        self.assertEqual(len(chunks), 1, "최대 길이보다 짧은 텍스트는 하나의 청크만 생성되어야 합니다.")
        self.assertEqual(chunks[0], text, "생성된 청크는 원본 텍스트와 동일해야 합니다.")
    
    def test_split_text_chunks_long_text(self):
        """긴 텍스트에 대한 테스트 (여러 청크로 분할되는 경우)"""
        # 100자 단위로 숫자가 포함된 텍스트 생성
        text = ""
        for i in range(10):
            text += f"{i}0 " + "가나다라마바사아자차카타파하 " * 4 + "\n"
        
        max_length = 100
        overlap = 20
        chunks = list(split_text_chunks(text, max_length, overlap))
        
        self.assertGreater(len(chunks), 1, "긴 텍스트는 여러 개의 청크로 분할되어야 합니다.")
        
        # 모든 청크를 연결하면 원본 텍스트의 모든 내용이 포함되어야 함
        # (중복 부분을 고려해야 함)
        combined_text = ""
        for chunk in chunks:
            # 첫 번째 청크는 그대로 사용
            if not combined_text:
                combined_text = chunk
            else:
                # 이후 청크는 중복되는 부분(overlap)을 제외하고 추가
                # 간단한 테스트를 위해 문자열 연결만 확인
                combined_text += chunk
        
        # 모든 숫자가 결합된 텍스트에 포함되어 있는지 확인
        for i in range(10):
            self.assertIn(f"{i}0", combined_text, f"숫자 {i}0이 결합된 텍스트에 포함되어 있어야 합니다.")
    
    def test_split_text_chunks_word_boundary(self):
        """단어 경계에서 분할되는지 테스트"""
        text = "첫 번째 문장입니다. 두 번째 문장입니다. 세 번째 문장입니다. 네 번째 문장입니다."
        max_length = 20
        overlap = 5
        
        chunks = list(split_text_chunks(text, max_length, overlap))
        
        for chunk in chunks:
            # 각 청크의 시작과 끝이 단어 중간에서 끊기지 않았는지 확인
            # (공백으로 시작하거나 끝나지 않아야 함)
            self.assertFalse(chunk.startswith(" "), "청크가 공백으로 시작하면 안됩니다.")
            self.assertFalse(chunk.endswith(" "), "청크가 공백으로 끝나면 안됩니다.")
    
    def test_split_text_chunks_overlap(self):
        """중복(overlap) 부분이 제대로 처리되는지 테스트"""
        text = "A" * 50 + "B" * 50 + "C" * 50
        max_length = 60
        overlap = 10
        
        chunks = list(split_text_chunks(text, max_length, overlap))
        
        self.assertEqual(len(chunks), 4, "텍스트가 4개의 청크로 분할되어야 합니다.")
        
        # 첫 번째 청크의 끝부분과 두 번째 청크의 시작 부분이 겹치는지 확인
        if len(chunks) >= 2:
            self.assertTrue(chunks[0].endswith("A" * overlap) or chunks[0].endswith("B" * overlap),
                            "첫 번째 청크의 끝부분이 다음 청크와 중복되어야 합니다.")
            
            self.assertTrue(chunks[1].startswith("A" * overlap) or chunks[1].startswith("B" * overlap),
                           "두 번째 청크의 시작 부분이 이전 청크와 중복되어야 합니다.")

if __name__ == '__main__':
    unittest.main() 