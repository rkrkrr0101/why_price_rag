import mysql.connector
from const.const_env import MYSQL_ID, MYSQL_KEY, MYSQL_URL

def update_hot_stocks(stock_list):
    """MySQL 데이터베이스의 급등주 목록을 업데이트합니다."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=MYSQL_ID,
            password=MYSQL_KEY,
            database="why_price"
        )
        cursor = conn.cursor()
        
        # 테이블이 없으면 생성
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hot_stock (
                id INT AUTO_INCREMENT PRIMARY KEY,
                stock_name VARCHAR(100) NOT NULL,
                stock_code VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 기존 데이터 비우기
        cursor.execute("TRUNCATE TABLE hot_stock")
        
        # 새 데이터 삽입
        for stock in stock_list:
            cursor.execute(
                "INSERT INTO hot_stock (stock_name, stock_code) VALUES (%s, %s)",
                (stock["name"], stock["code"])
            )
        
        conn.commit()
        print(f"{len(stock_list)}개의 급등주 정보가 MySQL에 업데이트되었습니다.")
        
    except Exception as e:
        print(f"MySQL 업데이트 오류: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def init_progress_table():
    """진행 상태를 저장할 테이블을 생성하거나 확인합니다."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=MYSQL_ID,
            password=MYSQL_KEY,
            database="why_price"
        )
        cursor = conn.cursor()
        
        # 진행 상태 테이블 생성
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processing_progress (
                id INT AUTO_INCREMENT PRIMARY KEY,
                stock_name VARCHAR(100) NOT NULL,
                news_url VARCHAR(512),
                is_processed BOOLEAN DEFAULT FALSE,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
    except Exception as e:
        print(f"진행 상태 테이블 초기화 오류: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def is_url_processed(stock_name, news_url):
    """URL이 이미 처리되었는지 확인합니다."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=MYSQL_ID,
            password=MYSQL_KEY,
            database="why_price"
        )
        cursor = conn.cursor()
        
        query = "SELECT is_processed FROM processing_progress WHERE stock_name = %s AND news_url = %s"
        cursor.execute(query, (stock_name, news_url))
        
        result = cursor.fetchone()
        
        if result:
            return result[0]
        return False
    except Exception as e:
        print(f"URL 진행 상태 확인 오류: {e}")
        return False
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def mark_url_processed(stock_name, news_url, is_processed=True):
    """URL의 처리 상태를 저장합니다."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=MYSQL_ID,
            password=MYSQL_KEY,
            database="why_price"
        )
        cursor = conn.cursor()
        
        # 이미 있는지 확인
        query = "SELECT id FROM processing_progress WHERE stock_name = %s AND news_url = %s"
        cursor.execute(query, (stock_name, news_url))
        
        result = cursor.fetchone()
        
        if result:
            # 기존 데이터 업데이트
            query = "UPDATE processing_progress SET is_processed = %s WHERE id = %s"
            cursor.execute(query, (is_processed, result[0]))
        else:
            # 새로운 데이터 삽입
            query = "INSERT INTO processing_progress (stock_name, news_url, is_processed) VALUES (%s, %s, %s)"
            cursor.execute(query, (stock_name, news_url, is_processed))
        
        conn.commit()
    except Exception as e:
        print(f"URL 진행 상태 저장 오류: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close() 