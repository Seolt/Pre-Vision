import json
from logger_manager import setup_logger
import csv

# 로그 설정
logger = setup_logger(r'C:\VTAPImodules\log\hash_handler', r'C:\VTAPImodules\log\hash_handler.log')

PROCESSED_HASHES_FILE = r'C:\VTAPImodules\processed_hashes.json'

def read_hashes_from_csv():
    """CSV 파일에서 해시 값을 읽어온다."""
    csv_file = r"C:\VTAPImodules\dataset.csv"
    try:
        with open(csv_file, 'r', encoding='ISO-8859-1') as file:
            reader = csv.DictReader(file)
            hashes = [row['md5_hash'].strip() for row in reader]  # CSV에서 'md5_hash' 열 읽기
            logger.info(f"CSV 파일 {csv_file}에서 해시 값 로드 성공")
            return hashes
    except FileNotFoundError:
        logger.error(f"CSV 파일 {csv_file}을 찾을 수 없음")
        return []
    except Exception as e:
        logger.error(f"CSV 파일 읽기 중 오류 발생: {e}")
        return []

def load_processed_hashes():
    try:
        with open(PROCESSED_HASHES_FILE, 'r') as f:
            logger.info("처리된 해시 로드 성공")
            return json.load(f)
    except FileNotFoundError:
        logger.error("처리된 해시 파일을 찾을 수 없음")
        return []
    except json.JSONDecodeError:
        logger.error("처리된 해시 파일을 읽는 중 JSON 오류 발생")
        return []

def save_processed_hashes(processed_hashes):
    try:
        with open(PROCESSED_HASHES_FILE, 'w') as f:
            json.dump(processed_hashes, f)
            logger.info("처리된 해시 기록 저장 성공")
    except Exception as e:
        logger.error(f"처리된 해시 저장 중 오류 발생: {e}")
