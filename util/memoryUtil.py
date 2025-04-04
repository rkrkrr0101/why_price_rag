import psutil
import os

def get_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    memory_usage_mb = memory_info.rss / 1024 / 1024
    return memory_usage_mb

# 진행 함수에 메모리 모니터링 추가
def memory_monitor(message):
    memory_usage = get_memory_usage()
    print(f"메모리 사용량 ({message}): {memory_usage:.2f} MB")